from marvin import ai_model
from pydantic import BaseModel

from information_retrieval.api.v1.models.activity import Activity
from information_retrieval.core.logger import app_logger as logger

instructions = """
I am going to provide some text content scraped from the PDF of a resume. It may be disorganized,
but I want you to take this text and parse it into a list of Activities.

Each separate bullet point from a job, skill, project, endorsement, accomplishment, etc... listed should
be treated as its own Activity. If there is a clear organization (company, school, etc...) associated with
an Activity, return that. If you are not sure, or if an Activity doesn't belong to a specific Organization,
for example - a skill the person learned, then use "None" as the Organization value.

Here is the text extracted from the Resume PDF:

"""


@ai_model(instructions=instructions)
class ResumeResponse(BaseModel):
    activities: list[Activity]


def create_activities_from_resume_ai(content: str) -> list[Activity]:
    if content is None:
        return []

    message = instructions + content
    try:
        return ResumeResponse(message).activities
    except Exception as e:
        logger.error(f"Failed to create activities from resume content: {e}")
        raise e
