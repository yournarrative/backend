import random
import os

from fastapi import UploadFile

from interview_analyzer.utils.standard_logger import get_logger

logger = get_logger()


def write_to_temp_file(file: UploadFile) -> str:
    filetype = file.filename.split(".")[-1]
    while True:
        new_file_name = random.randint(0, 9999999999999999)
        filename = f"tmp/{new_file_name}.{filetype}"
        if not os.path.exists(filename):
            with open(filename, "wb") as f:
                f.write(file.file.read())
            logger.debug(f"Successfully wrote file to {filename}")
            return filename


def cleanup_temp_file(filepath: str):
    if os.path.exists(filepath):
        os.remove(filepath)
        logger.debug(f"Successfully removed file {filepath}")
    else:
        logger.warning(f"File {filepath} does not exist")
