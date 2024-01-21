import boto3
from starlette.datastructures import State

from interview_analyzer.utils.standard_logger import get_logger

logger = get_logger()


async def create_s3_connector(state: State) -> boto3.resource:

    region = state.env.get("AWS_REGION")
    aws_access_key_id = state.env.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = state.env.get("AWS_SECRET_ACCESS_KEY")

    logger.debug(f"Creating S3 connector to region: {region} with access_key_id: "
                 f"{aws_access_key_id[:4]}...{aws_access_key_id[-4:]}")

    try:
        s3 = boto3.resource(
            service_name="s3",
            region_name=region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )
    except Exception as e:
        logger.error(f"Failed to create S3 connector: {e}")
        raise e
    else:
        logger.debug("S3 connector created.")
        return s3
