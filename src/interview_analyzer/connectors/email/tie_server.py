import smtplib
import ssl

from starlette.datastructures import State

from interview_analyzer.utils.standard_logger import get_logger


logger = get_logger()


async def create_tie_server(state: State) -> smtplib.SMTP:
    smtp_port = 587                 # Standard secure SMTP port
    smtp_server = "smtp.gmail.com"  # Google SMTP Server

    try:
        # Connect to the server
        logger.debug("Creating simple email context...")
        simple_email_context = ssl.create_default_context()

        logger.debug("Connecting to server...")
        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls(context=simple_email_context)

        email_from = state.env.get("EMAIL_ADDRESS")
        pwd = state.env.get("EMAIL_APP_PASSWORD")
        TIE_server.login(email_from, pwd)
        logger.debug(f"Connected to server using: {email_from}")
        return TIE_server

    except Exception as e:
        logger.debug(f"Failed to initialize SMTP server: {e}")
        raise e
