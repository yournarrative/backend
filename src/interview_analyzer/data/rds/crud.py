import json

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text

from interview_analyzer.api.api_v1.interview.model import Interview
from interview_analyzer.utils.standard_logger import get_logger


logger = get_logger()


async def get_email_from_rds_using_interview_uuid(async_session: AsyncSession, interview_uuid: str) -> str:
    logger.debug(f"Getting email from interview id {interview_uuid}...")
    async with async_session as session:
        query = text(
            f"""
            SELECT email FROM users
            WHERE id = (SELECT user_id FROM interviews WHERE id = '{interview_uuid}')
            """
        )
        email_address = (await session.execute(query)).fetchall()[0][0]
        if email_address:
            logger.debug(f"Successfully got email address {email_address} from interview id {interview_uuid}")
        else:
            raise ValueError(f"Could not find email address for interview id {interview_uuid}")
    return email_address


async def get_interview_id_from_rds_using_s3_path(async_session: AsyncSession, s3_bucket: str, s3_key: str) -> str:
    logger.debug(f"Getting interview id from s3 path {s3_bucket}/{s3_key}...")
    user_id = s3_key.split("/")[0]  # user table 'id' field as uuid

    async with async_session as session:
        query = text(
            f"""
            SELECT id FROM interviews
            WHERE user_id = '{user_id}'
            ORDER BY created_on DESC
            LIMIT 1
            """
        )
        interview_id = (await session.execute(query)).fetchall()[0][0]
        logger.debug(f"Successfully got interview id: {interview_id} from s3 path {s3_bucket}/{s3_key}")
    return str(interview_id)


async def update_interview_with_interview_object(
        async_session: AsyncSession,
        interview_uuid: str,
        interview: Interview,
) -> None:
    logger.debug(f"Updating interview {interview_uuid} with transcript and enriched transcript...")
    async with async_session as session:
        query = text(
            f"""
            UPDATE interviews
            SET data = jsonb_set(data, '{{interview}}', '{json.dumps(interview.model_json_schema())}',
             true),
             processed = true
            WHERE id = '{interview_uuid}';
            """
        )
        try:
            await session.execute(query)
            await session.commit()
        except Exception as e:
            logger.error(f"Error updating interview {interview_uuid} with enriched transcript: {e}")
            await session.rollback()
            raise e
        else:
            logger.debug(f"Successfully updated interview {interview_uuid} with enriched transcript")
