from starlette.datastructures import State

from interview_analyzer.api.api_v1.email.helpers import create_pdf, send_report, extract_content_from_interview
from interview_analyzer.api.api_v1.interview.model import Interview
from interview_analyzer.utils.standard_logger import get_logger


logger = get_logger()


async def send_email(interview: Interview, email_to: str, state: State):
    logger.info(f"Sending feedback email to {email_to}")
    content = extract_content_from_interview(interview)
    pdf_filepath = create_pdf(content, state)
    send_report(email_to=email_to, filepath=pdf_filepath, state=state)
