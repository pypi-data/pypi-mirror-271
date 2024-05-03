from setuptools import setup, find_packages

setup(
    name='http_backuper',
    version='0.1.7',
    url='https://github.com/djbios/http_backuper',
    author='djbios',
    author_email='dorandval@gmail.com',
    description='A simple backup solution',
    packages=find_packages(),
    install_requires=[
        'pydantic<2', 'requests', 'schedule', 'docker', 'healthchecks_io', 'PyYAML',
    ],
    entry_points={
        'console_scripts': [
            'http_backuper=http_backuper.backuper:main',
            'backuper=http_backuper.backuper:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
    ],
)
