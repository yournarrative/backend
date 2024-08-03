import json

from marvin import ai_model
from pydantic import BaseModel

from information_retrieval.api.v1.models.activity import Activity, ActivityWithID
from information_retrieval.core.logger import app_logger as logger

instructions = """
Take the details of an Activity in the form of a JSON object and update the fields
as necessary to reflect the new details.
"""


@ai_model(instructions=instructions)
class UpdateActivityResponse(BaseModel):
    activity: Activity


def update_activity_with_new_details_ai(activity_with_id: ActivityWithID, update: str) -> ActivityWithID:
    activity_dict = {
        "title": activity_with_id.title,
        "description": activity_with_id.description,
        "category": activity_with_id.category,
        "status": activity_with_id.status,
    }
    request_string = json.dumps(activity_dict) + "\n Update:\n" + update
    try:
        updated_activity: Activity = UpdateActivityResponse(request_string).activity
        return ActivityWithID(
            id=activity_with_id.id,
            title=updated_activity.title,
            description=updated_activity.description,
            category=updated_activity.category,
            status=updated_activity.status,
        )
    except Exception as e:
        logger.error(f"Failed to update activity with id {activity_with_id.id} - {e}")
        raise e
