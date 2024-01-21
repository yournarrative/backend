import random
import os
from typing import Dict, Any

import yaml
from fastapi import UploadFile

from interview_analyzer.utils.standard_logger import get_logger

logger = get_logger()


def load_config_from_env(env: str) -> Dict[str, Any]:
    logger.debug(f"Loading config from env {env}...")
    with open(f"resources/config/{env}/conf.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)
    return config


def create_temp_directory():
    if not os.path.exists(os.getcwd() + "/tmp"):
        os.mkdir(os.getcwd() + "/tmp", mode=0o777)


def write_upload_file_to_temp_file(file: UploadFile) -> str:
    filetype = file.filename.split(".")[-1]
    while True:
        new_file_name = random.randint(0, 9999999999999999)  # TODO: change to current date/time/milli timestamp as name
        filename = f"tmp/{new_file_name}.{filetype}"
        if not os.path.exists(filename):
            with open(filename, "wb") as f:
                f.write(file.file.read())
            logger.debug(f"Successfully wrote upload file to {filename}")
            return filename


def write_bytes_file_to_temp_file(file_bytes: bytes, filename: str) -> str:
    filetype = filename.split(".")[-1]
    while True:
        new_file_name = random.randint(0, 9999999999999999)  # TODO: change to current date/time/milli timestamp as name
        filename = f"tmp/{new_file_name}.{filetype}"
        if not os.path.exists(filename):
            with open(filename, "wb") as f:
                f.write(file_bytes)
            logger.debug(f"Successfully wrote bytes file to {filename}")
            return filename


def cleanup_temp_file(filepath: str):
    if os.path.exists(filepath):
        os.remove(filepath)
        logger.debug(f"Successfully removed file {filepath}")
    else:
        logger.warning(f"File {filepath} does not exist")
