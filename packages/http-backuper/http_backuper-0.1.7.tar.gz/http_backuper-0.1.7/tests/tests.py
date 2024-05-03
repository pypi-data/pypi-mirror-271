import io
import os
import tarfile
import tempfile
from unittest.mock import ANY

import docker
import pytest

from http_backuper import job
from http_backuper.models import BackupSection, Source, Frequency, HttpMethod, GeneralSection


@pytest.fixture(scope="function")
def docker_container_with_file():
    docker_client = docker.from_env()
    test_file_path = "/test_file"
    container = docker_client.containers.run(
        "alpine", f'/bin/sh -c "echo test > {test_file_path}"', detach=True
    )

    # Yield container data
    yield {
        "name": container.name,
        "test_file_path": test_file_path,
    }

    # Clean up: Remove the test Docker container
    container.remove(force=True)


def test_e2e_backup_file_in_container(docker_container_with_file, mocker):
    # Setup backup and general configs
    backup_config = BackupSection(
        name="test",
        schedule=Frequency.DAY,
        sources=[
            Source(
                path=docker_container_with_file["test_file_path"],
                container_name=docker_container_with_file["name"],
            )
        ],
    )
    general_config = GeneralSection(
        host=f"http://localhost", http_verb=HttpMethod.POST, requests_properties={}
    )

    # Create a mock response for 'requests.post'
    mock_response = mocker.Mock(status_code=200)
    post_mock = mocker.patch("requests.post", return_value=mock_response)

    # Run the job
    job(backup_config, general_config)

    # Ensure post was called
    assert post_mock.call_count == 1

    # The backup data should be a tar file. Check that it contains the test file with the correct contents.
    post_mock.call_args.assert_called_once_with(ANY, files={"file": ANY})

    backup_data = post_mock.call_args[1]["files"]["file"]

    with tarfile.open(fileobj=io.BytesIO(backup_data), mode="r:gz") as tar:
        test_file = tar.extractfile(
            docker_container_with_file["test_file_path"].strip("/")
        )
        assert test_file.read().decode() == "test\n"


@pytest.fixture(scope="function")
def docker_container_with_folder():
    docker_client = docker.from_env()
    test_folder_path = "/test_folder"
    test_file1_path = "/test_folder/test_file1"
    test_file2_path = "/test_folder/test_file2"

    container = docker_client.containers.run(
        "alpine",
        f'/bin/sh -c "mkdir {test_folder_path}; echo test > {test_file1_path}; echo test > {test_file2_path}"',
        detach=True,
    )

    # Yield container data
    yield {
        "name": container.name,
        "test_folder_path": "/test_folder",
        "test_file1_path": "/test_folder/test_file1",
        "test_file2_path": "/test_folder/test_file2",
    }

    # Clean up: Remove the test Docker container
    container.remove(force=True)


def test_e2e_backup_folder_in_container(docker_container_with_folder, mocker):
    # Setup backup and general configs
    backup_config = BackupSection(
        name="test",
        schedule=Frequency.DAY,
        sources=[
            Source(
                path=docker_container_with_folder["test_folder_path"],
                container_name=docker_container_with_folder["name"],
            )
        ],
    )
    general_config = GeneralSection(
        host=f"http://localhost", http_verb=HttpMethod.POST, requests_properties={}
    )

    # Create a mock response for 'requests.post'
    mock_response = mocker.Mock(status_code=200)
    post_mock = mocker.patch("requests.post", return_value=mock_response)

    # Run the job
    job(backup_config, general_config)

    # Ensure post was called
    assert post_mock.called

    # The backup data should be a tar file. Check that it contains the test file with the correct contents.
    post_mock.call_args.assert_called_once_with(ANY, files={"file": ANY})

    backup_data = post_mock.call_args[1]["files"]["file"]

    with tarfile.open(fileobj=io.BytesIO(backup_data), mode="r:gz") as tar:
        test_file1 = tar.extractfile(
            docker_container_with_folder["test_file1_path"].strip("/")
        )
        test_file2 = tar.extractfile(
            docker_container_with_folder["test_file2_path"].strip("/")
        )
        assert test_file1.read().decode() == "test\n"
        assert test_file2.read().decode() == "test\n"


@pytest.fixture(scope="function")
def local_file():
    with tempfile.NamedTemporaryFile(delete=False) as f:
        f.write(b"test\n")
    yield f.name
    os.unlink(f.name)


def test_e2e_backup_local_file(local_file, mocker):
    # Setup backup and general configs
    backup_config = BackupSection(
        name="test", schedule=Frequency.DAY, sources=[Source(path=local_file)]
    )
    general_config = GeneralSection(
        host=f"http://localhost", http_verb=HttpMethod.POST, requests_properties={}
    )

    # Create a mock response for 'requests.post'
    mock_response = mocker.Mock(status_code=200)
    post_mock = mocker.patch("requests.post", return_value=mock_response)

    # Run the job
    job(backup_config, general_config)

    # Ensure post was called
    assert post_mock.called

    # The backup data should be a tar file. Check that it contains the test file with the correct contents.
    # post_mock.assert_called_once_with(ANY, files={'file': ANY})

    backup_data = post_mock.call_args[1]["files"]["file"]

    with tarfile.open(fileobj=io.BytesIO(backup_data), mode="r:gz") as tar:
        test_file = tar.extractfile(local_file.strip("/"))
        assert test_file.read().decode() == "test\n"


@pytest.fixture(scope="function")
def local_folder():
    with tempfile.TemporaryDirectory() as d:
        with open(os.path.join(d, "test_file1"), "w") as f:
            f.write("test\n")
        with open(os.path.join(d, "test_file2"), "w") as f:
            f.write("test\n")
        yield d


def test_e2e_backup_local_folder(local_folder, mocker):
    # Setup backup and general configs
    backup_config = BackupSection(
        name="test", schedule=Frequency.DAY, sources=[Source(path=local_folder)]
    )
    general_config = GeneralSection(
        host=f"http://localhost", http_verb=HttpMethod.POST, requests_properties={}
    )

    # Create a mock response for 'requests.post'
    mock_response = mocker.Mock(status_code=200)
    post_mock = mocker.patch("requests.post", return_value=mock_response)

    # Run the job
    job(backup_config, general_config)

    # Ensure post was called
    assert post_mock.called

    # The backup data should be a tar file. Check that it contains the test file with the correct contents.
    # post_mock.assert_called_once_with(ANY, files={'file': ANY})

    backup_data = post_mock.call_args[1]["files"]["file"]

    with tarfile.open(fileobj=io.BytesIO(backup_data), mode="r:gz") as tar:
        test_file1 = tar.extractfile(
            os.path.join(local_folder, "test_file1").strip("/")
        )
        test_file2 = tar.extractfile(
            os.path.join(local_folder, "test_file2").strip("/")
        )
        assert test_file1.read().decode() == "test\n"
        assert test_file2.read().decode() == "test\n"


@pytest.mark.parametrize(
    "frequency, timeout",
    (
        (Frequency.MINUTE, 60),
        (Frequency.HOUR, 60 * 60),
        (Frequency.DAY, 60 * 60 * 24),
        (Frequency.WEEK, 60 * 60 * 24 * 7),
    ),
)
def test_backup_with_healthcheck(local_file, mocker, frequency, timeout):
    backup_config = BackupSection(
        name="test", schedule=frequency, sources=[Source(path=local_file)]
    )
    general_config = GeneralSection(
        host=f"http://localhost",
        http_verb=HttpMethod.POST,
        requests_properties={},
        healthchecks_io_api_key="test",
    )

    mock_response = mocker.Mock(status_code=200)
    post_mock = mocker.patch("requests.post", return_value=mock_response)
    get_mock = mocker.patch("requests.get", return_value=mock_response)
    get_healthchecks_mock = mocker.patch(
        "healthchecks_io.client.Client.get_checks", return_value=[]
    )
    create_healthcheck_mock = mocker.patch("healthchecks_io.client.Client.create_check")
    create_healthcheck_mock.return_value.ping_url = "http://localhost/ping"

    job(backup_config, general_config)
    assert post_mock.call_count == 1
    assert get_healthchecks_mock.call_count == 1
    assert create_healthcheck_mock.call_count == 1
    create_check_request = create_healthcheck_mock.call_args[0][0]
    assert create_check_request.name == "test"
    assert create_check_request.timeout == timeout
    assert get_mock.call_count == 1
    get_mock.assert_called_once_with("http://localhost/ping")
