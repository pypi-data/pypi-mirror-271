#!/usr/bin/env python3

import argparse
import getpass
import io
import logging
import os
import subprocess
import tarfile
import tempfile
import time
from datetime import timedelta
from functools import partial
from typing import Dict

import requests
import schedule
import yaml
from docker import DockerClient
from healthchecks_io import Client, CheckCreate
from pydantic import ValidationError

from http_backuper.models import Config, GeneralSection, BackupSection


def setup_logging():
    # Create a custom logger
    logger = logging.getLogger('http_backuper')

    # Set the threshold of logger to DEBUG
    logger.setLevel(logging.DEBUG)

    # Create handlers
    console_handler = logging.StreamHandler()

    # Set level of handlers
    console_handler.setLevel(logging.INFO)

    # Create formatters and add it to handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Add handlers to the logger
    logger.addHandler(console_handler)

    return logger

logger = setup_logging()


def load_config(path: str) -> Config:
    with open(path, "r") as f:
        config_data = yaml.safe_load(f)

    try:
        config =  Config(**config_data)
        logger.info(f"Successfully loaded configuration from {path}")
        return config
    except ValidationError as e:
        logger.error(f"Invalid configuration data: {e}")
        raise


def is_path(source: str) -> bool:
    return os.path.exists(source)


def add_path_to_tar(tar: tarfile.TarFile, source: str) -> None:
    tar.add(source)
    logger.info(f"Successfully added path {source} to tar file")


def add_container_path_to_tar(
    client: DockerClient, container_name: str, source: str, tar: tarfile.TarFile
):
    container = client.containers.get(container_name)
    # Create a temporary tar archive from the container's file/directory
    bits, stat = container.get_archive(source)

    with tempfile.NamedTemporaryFile() as temp_file:
        # Write bits to a temporary file
        for chunk in bits:
            temp_file.write(chunk)
        temp_file.flush()

        # Open the temp file as a tarfile
        with tarfile.open(temp_file.name, "r") as container_tar:
            # Add the files from the container tar to the final tar file
            for member in container_tar.getmembers():
                f = container_tar.extractfile(member)
                tarinfo = tarfile.TarInfo(name=member.name)
                tarinfo.size = member.size
                tar.addfile(tarinfo, fileobj=f)

    logger.info(
        f"Successfully added container {container_name} path {source} to tar file"
    )





def run_command_in_container(
    client: DockerClient,
    container_name: str,
    command: str,
    tar: tarfile.TarFile,
    filename: str,
):
    container = client.containers.get(container_name)
    exit_code, output = container.exec_run(command)
    if exit_code != 0:
        raise Exception(
            f"Command {command} failed in container {container_name} with exit code {exit_code}"
        )
    tarinfo = tarfile.TarInfo(name=filename)
    tarinfo.size = len(output)
    tar.addfile(tarinfo, io.BytesIO(output))
    logger.info(
        f"Successfully ran command {command} in container {container_name} with exit code {exit_code}"
    )


def run_command_on_host(
    command: str,
    tar: tarfile.TarFile,
    filename: str,
):
    completed_process = subprocess.run(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    if completed_process.returncode != 0:
        raise Exception(
            f"Command {command} failed on host with exit code {completed_process.returncode}"
        )
    tarinfo = tarfile.TarInfo(name=filename)
    tarinfo.size = len(completed_process.stdout)
    tar.addfile(tarinfo, io.BytesIO(completed_process.stdout))
    logger.info(f"Successfully ran command {command} on host")


def post_data(
    url: str,
    tar_stream: io.BytesIO,
    headers: Dict[str, str],
    name: str,
    file_field: str = "file",
) -> None:
    response = requests.post(
        url,
        files={file_field: (f"{name}.tar.gz", tar_stream.getvalue())},
        headers=headers,
    )
    if response.status_code != 200:
        raise Exception(f"Failed to POST data: {response.text}")
    logger.info(f"Successfully posted data to {url}")


def ping_healthcheck(name: str, api_key: str, timeout: int) -> None:
    # Ensure halthcheck.io check is created
    client = Client(api_key=api_key)
    all_checks = client.get_checks()
    checks = [c for c in all_checks if c.name == name]
    if checks:
        check = checks[0]
    else:
        check = client.create_check(CheckCreate(name=name, timeout=timeout))

    requests.get(check.ping_url)
    logger.info(f"Pinged healthcheck.io check {check.name}")


def job(backup_config: BackupSection, general_config: GeneralSection) -> None:
    logger.info(f"Starting backup {backup_config.name}")
    tar_stream = io.BytesIO()
    with tarfile.open(fileobj=tar_stream, mode="w:gz") as tar:
        for source in backup_config.sources:
            try:
                if source.path:
                    if source.container_name:
                        docker = DockerClient.from_env()
                        add_container_path_to_tar(
                            docker, source.container_name, source.path, tar
                        )
                    else:
                        add_path_to_tar(tar, source.path)
                elif source.command:
                    if source.container_name:
                        docker = DockerClient.from_env()
                        run_command_in_container(
                            client=docker,
                            container_name=source.container_name,
                            command=source.command,
                            tar=tar,
                            filename=source.name,
                        )
                    else:
                        run_command_on_host(
                            command=source.command,
                            tar=tar,
                            filename=source.name,
                        )
            except Exception as e:
                logger.error(f"Failed to backup source {source.name}: {e}")
                return

    tar_stream.seek(0)
    if rp := general_config.requests_properties:
        headers = rp.get("headers") or {}
    else:
        headers = {}

    post_data(
        url=general_config.url,
        tar_stream=tar_stream,
        headers=headers,
        name=backup_config.name,
        file_field=general_config.file_field_name,
    )
    if general_config.healthchecks_io_api_key:
        timeout = int(timedelta(**{backup_config.schedule: 1}).total_seconds())
        ping_healthcheck(
            backup_config.name, general_config.healthchecks_io_api_key, timeout=timeout
        )


def install_service():
    if getpass.getuser() != "root":
        logger.error("You need to run this script as root to install it as a service.")
        return

    service_content = f"""[Unit]
      Description=HttpBackuper service
      After=network.target

      [Service]
      ExecStart=/usr/bin/env python3 -u {os.path.realpath(__file__)} -I
      Restart=always

      [Install]
      WantedBy=multi-user.target
      """

    with open("/etc/systemd/system/http_backuper.service", "w") as f:
        f.write(service_content)

    subprocess.run(["cp", "-n", "./config.example.yml", "/etc/http_backuper/config.yml"])  # TODO fix this + mkdir
    subprocess.run(["systemctl", "daemon-reload"])
    subprocess.run(["systemctl", "enable", "http_backuper.service"])
    logger.info("Service installed and enabled.")
    return


def main():
    logger.info('HttpBackuper service startup')
    # Create a parser for the command-line arguments
    parser = argparse.ArgumentParser(description="Run the backup job.")
    parser.add_argument(
        "-c",
        "--config",
        type=str,
        help="Path to the config file.",
    )
    parser.add_argument(
        "-I",
        "--immediately",
        action="store_true",
        help="Run backups immidiately.",
    )
    parser.add_argument(
        "-i",
        "--install-service",
        action="store_true",
        help="Install this script as a Linux service.",
    )
    args = parser.parse_args()
    if args.install_service:
        install_service()
        exit(0)

    # Check if a config path was provided as an argument
    if args.config:
        config_path = args.config
    # If not, check if a config path was provided as an environment variable
    elif "CONFIG_PATH" in os.environ:
        config_path = os.environ["CONFIG_PATH"]
    # If not, use a default config path
    else:
        config_path = "/etc/http_backuper/config.yml"

    config = load_config(config_path)
    general_config = GeneralSection(**config.general.dict())

    for backup in config.backups:
        job_partial = partial(job, backup_config=backup, general_config=general_config)
        getattr(schedule.every(), backup.schedule).do(job_partial)
        if args.immediately or args.immediately:
            job_partial()

    while schedule.jobs:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()


# TODO add arguments:
# TODO better logging
# TODO fail tolerance
# TODO tests on commands
# TODO ensure no memory leaks
# TODO allow to run concrete backups by name from cli