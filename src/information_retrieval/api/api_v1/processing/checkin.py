from marvin import ai_model
from pydantic import BaseModel
from typing import List

from starlette.datastructures import State

from information_retrieval.api.api_v1.model.activity import Activity
from information_retrieval.api.api_v1.model.checkin import CheckIn


@ai_model(instructions="Infer activities from how the questions are answered.")
class CheckInResponse(BaseModel):
    activities: List[Activity]


def create_activities_from_check_in(check_in: CheckIn, state: State):
    text = '\n'.join(check_in.dialogue)
    response = CheckInResponse(text)
    return response
