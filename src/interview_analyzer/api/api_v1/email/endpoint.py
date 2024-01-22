from interview_analyzer.api.api_v1.interview.model import Interview
from interview_analyzer.utils.standard_logger import get_logger

logger = get_logger()


async def send_email(interview: Interview, to_email: str):
    logger.info(f"Sending feedback email to {to_email}")
    # send email
    pass
