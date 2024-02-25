import time
import sys

import boto3

from interview_analyzer.utils.standard_logger import get_logger

logger = get_logger()


def read_file_from_s3(s3: boto3.resource, bucket_name: str, key: str):
    """
    Read file from S3 bucket

    :param bucket_name: S3 bucket name
    :param key: s3 file key
    :return: file content
    """
    start_time = time.time()
    logger.debug(f"Reading file {key} from S3 bucket {bucket_name}...")
    try:
        obj = s3.Object(bucket_name, key)
        file = obj.get()['Body'].read()
    except Exception as e:
        logger.error(f"Failed to read file from S3: {e}")
        raise e
    else:
        logger.debug(f"File {key} read from S3 bucket {bucket_name}, size {sys.getsizeof(file)}, elapsed time: {time.time() - start_time} seconds")
        return file


def upload_file_to_s3(s3: boto3.resource, local_filepath: str, upload_key: str, bucket_name: str):
    """
    Upload a file to an S3 bucket

    :param file_path: Path to the file to upload
    :param bucket_name: Name of the S3 bucket
    :param object_name: S3 object name (if not specified, file_name will be used)
    :return: True if file was uploaded successfully, else False
    """
    logger.debug(f"Uploading file {local_filepath} to S3 bucket {bucket_name} as {upload_key}...")
    try:
        response = s3.meta.client.upload_file(local_filepath, bucket_name, upload_key)
        logger.debug(f"File {local_filepath} successfully uploaded to S3 bucket {bucket_name} as {upload_key}")
    except Exception as e:
        logger.error(f"Error uploading file {local_filepath} to S3 bucket {bucket_name} and key {upload_key}: {e}")
