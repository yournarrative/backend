from marvin import ai_model
from pydantic import BaseModel

from information_retrieval.api.v1.models.activity import Activity
from information_retrieval.core.logger import app_logger as logger

instructions = """
Infer activities from how the questions are answered.
If there are questions with vague answers,
such as 'learned something' or 'did something' without specifics skills or experiences
included mentioned, do not include it as part of the final activity list.

Also, ignore unintelligible, incomplete, or spam-like dialogue, such as repeated words or gibberish.

It is okay to return an empty list if no activities can be inferred from the dialogue.

It is better to be conservative with they activities that you infer from the dialogue,
than trying to infer too many activities.
"""


@ai_model(instructions=instructions)
class CheckInResponse(BaseModel):
    activities: list[Activity]


def create_activities_from_check_in_ai(dialogue: list[str]) -> list[Activity]:
    if dialogue is None:
        return []

    dialogue = map(lambda x: x.strip(), dialogue)

    if (not dialogue) or (not any(dialogue)):
        return []

    text = "\n".join(dialogue)
    if not text:
        return []

    try:
        return CheckInResponse(text).activities
    except Exception as e:
        logger.error(f"Failed to create activities from check-in dialogue: {e}")
        raise e
