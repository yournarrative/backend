import random
import time
from datetime import datetime
from typing import Dict, Any
import os, os.path
import errno

import yaml
from fastapi import UploadFile

from information_retrieval.utils.standard_logger import get_logger

logger = get_logger()


def load_env() -> Dict[str, str]:
    logger.debug("Loading env variables...")
    env = dict(os.environ)
    return env


def load_config_from_env(env: str) -> Dict[str, Any]:
    logger.debug(f"Loading config from env {env}...")
    env = env.replace('"', '')
    with open(f"resources/config/{env}/conf.yaml", "r") as config_file:
        config = yaml.safe_load(config_file)
    return config


def create_temp_directory():
    if not os.path.exists(os.getcwd() + "/tmp"):
        os.mkdir(os.getcwd() + "/tmp", mode=0o777)


def mkdir_p(path: str):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def safe_open_w(path: str, mode: str):
    ''' Open "path" for writing, creating any parent directories as needed.
    '''
    mkdir_p(os.path.dirname(path))
    return open(path, mode)


def write_upload_file_to_temp_file(file: UploadFile) -> str:
    filetype = file.filename.split(".")[-1]
    while True:
        new_file_name = random.randint(0, 9999999999999999)  # TODO: change to current date/time/milli timestamp as name
        filename = f"tmp/{new_file_name}.{filetype}"
        if not os.path.exists(filename):
            with safe_open_w(filename, "wb") as f:
                f.write(file.file.read())
            logger.debug(f"Successfully wrote upload file to {filename}")
            return filename


def write_bytes_file_to_temp_file(file_bytes: bytes, filename: str, rename: bool = False) -> str:
    logger.debug(f"Writing bytes file with name: {filename} to temp directory, rename={rename}...")
    filetype = filename.split(".")[-1]
    s3_key_path = '/'.join(filename.split("/")[:-1])

    if rename:
        formatted_datetime = datetime.now().strftime('%Y-%m-%d-%H:%M:%S:%f')
        temp_filename = f"tmp/{s3_key_path}/{formatted_datetime}.{filetype}"
    else:
        temp_filename = f"tmp/{s3_key_path}/{filename.split('/')[-1]}"
    logger.debug(f"New filename: {temp_filename}")

    try:
        if not os.path.exists(temp_filename):
            with safe_open_w(temp_filename, "wb") as f:
                f.write(file_bytes)
        logger.debug(f"Successfully wrote bytes file to {temp_filename}")
        return temp_filename
    except Exception as e:
        logger.error(f"Failed to write bytes file to {filename}: {e}")
        raise e


def cleanup_temp_file(filepath: str):
    if os.path.exists(filepath):
        os.remove(filepath)
        logger.debug(f"Successfully removed file {filepath}")
    else:
        logger.warning(f"File {filepath} does not exist")


def extract_audio(input_file: str, output_filetype: str) -> str:
    start_time = time.time()
    output_file = input_file.split(".")[0] + "." + output_filetype

    if not output_file.startswith("tmp/"):
        output_file = "tmp/" + output_file

    logger.debug(f"Extracting audio from {input_file} to {output_file}...")

    try:
        (
            ffmpeg
                .input(input_file)
                .output(
                    output_file,
                    format=output_filetype,
                    b='1M',
                    y='-y')
                .run()
        )
    except Exception as e:
        logger.error(f"Failed to extract {output_filetype} file from .webm file: {e}, stderr: {e.stderr}")
        raise e
    else:
        logger.debug(f"Successfully extracted .m4a file from .webm file, elapsed time: {str(time.time() - start_time)} seconds")
        return output_file
