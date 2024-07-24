from marvin import ai_model
from pydantic import BaseModel

from information_retrieval.api.api_v1.model.activity import Activity
from information_retrieval.api.api_v1.model.checkin import CheckIn
from information_retrieval.utils.standard_logger import app_logger as logger

instructions = """
Infer activities from how the questions are answered.
If there are activities with vague titles or descriptions,
such as 'learned something' or 'did something' without specifics skills or experiences
included, do not include it as part of the final activity list.
"""


@ai_model(instructions=instructions)
class CheckInResponse(BaseModel):
    activities: list[Activity]


def create_activities_from_check_in_ai(check_in: CheckIn) -> list[Activity]:
    if check_in.dialogue is None:
        return []

    check_in.dialogue = map(lambda x: x.strip(), check_in.dialogue)

    if (not check_in.dialogue) or (not any(check_in.dialogue)):
        return []

    text = "\n".join(check_in.dialogue)
    if not text:
        return []

    try:
        return CheckInResponse(text).activities
    except Exception as e:
        logger.error(f"Failed to create activities from check-in - {e}")
        raise e
