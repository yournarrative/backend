from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders

from starlette.datastructures import State
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import LETTER

from interview_analyzer.api.api_v1.interview.model import Interview
from interview_analyzer.utils.standard_logger import get_logger

logger = get_logger()


def send_report(email_to: str, filepath: str, state: State):
    logger.debug(f"Sending email to - {email_to}")

    email_from = state.env['EMAIL_ADDRESS']
    subject: str = "Your Ghosted Interview Report is Ready!"
    body: str = "Hello this is a test. Please find the attached report."

    # make a MIME object to define parts of the email
    msg = MIMEMultipart()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = subject

    # Attach the body of the message
    msg.attach(MIMEText(body, 'plain'))

    # Open the file in python as a binary
    logger.debug(f"Opening PDF to attach (filepath - {filepath})")
    with open(filepath, 'rb') as f:
        attachment_package = MIMEApplication(f.read(), _subtype="pdf")

    # Encode as base 64
    # attachment_package = MIMEBase('application', 'octet-stream')
    # msg.set_payload((attachment_package).read())
    # encoders.encode_base64(attachment_package)
    attachment_package.add_header('Content-Disposition', "attachment; filename= " + "GhostedReport.pdf")
    msg.attach(attachment_package)

    # Cast as string
    text = msg.as_string()
    try:
        logger.debug(f"Attempting to send email + pdf report to: {email_to}...")
        state.TIE_server.sendmail(email_from, email_to, text)
        logger.debug(f"Email successfully sent to - {email_to}")

    except Exception as e:
        logger.error(f"Email failed to send to - {email_to}: {e}")


def extract_content_from_interview(interview: Interview) -> str:
    return ""


def create_pdf(content: str, state: State) -> str:
    logger.debug("Creating PDF report...")
    current_datetime = datetime.now()
    current_datetime_string = current_datetime.strftime('%Y-%m-%d:%H:%M:%S.%f')[:-3]
    filepath = f"tmp/{current_datetime_string}.pdf"

    logger.debug(f"Assigned filepath: {filepath} to PDF")

    canvas = Canvas(filepath, pagesize=LETTER)
    canvas.drawString(72, 72, "This is a test report!")
    canvas.save()

    logger.debug(f"Saved PDF with filepath: {filepath}")

    # TODO: Look into a HTML template to fill, convert to pdf and save
    return filepath
