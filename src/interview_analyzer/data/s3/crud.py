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
    logger.debug(f"Reading file {key} from S3 bucket {bucket_name}...")

    try:
        obj = s3.Object(bucket_name, key)
        file = obj.get()['Body'].read()
    except Exception as e:
        logger.error(f"Failed to read file from S3: {e}")
        raise e
    else:
        logger.debug(f"File {key} read from S3 bucket {bucket_name}.")
        return file
