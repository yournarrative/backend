import json

from marvin import ai_model
from pydantic import BaseModel, Field

from information_retrieval.api.v1.models.activity import Activity
from information_retrieval.core.logger import app_logger as logger

instructions = """ I will provide activities performed by someone at a certain organization. This could
be a company they work for, a school they attend, or simply on their own time. Each activity will have a title,
description, and status. I want you to provide a coherent summary, showcasing the cohesive themes and accomplishments
of the activities, as if advertising this person to a potential employer or school.

If there is not enough information to conclude anything meaningful, you must return a shorter or empty summary.

Here they are, as python dictionaries:

"""

DOC_LIMIT = 20


@ai_model(instructions=instructions)
class ActivitySummary(BaseModel):
    summary: str = Field(..., description="The 3 to 5 sentence summary of the given activities.")


def create_summary_from_activities_ai(activities: list[Activity]) -> str:
    if not activities:
        return ""

    activities = [a.dict() for a in activities][:DOC_LIMIT]

    formatted_docs: list[dict] = []
    for a in activities:
        f = {
            "title": a.get("title", ""),
            "description": a.get("description", ""),
            "status": a.get("status", ""),
        }
        formatted_docs.append(f)

    text = instructions + json.dumps(formatted_docs, indent=4)

    try:
        return ActivitySummary(text).summary
    except Exception as e:
        logger.error(f"Failed to create summary from given activities: {e}")
        raise e
