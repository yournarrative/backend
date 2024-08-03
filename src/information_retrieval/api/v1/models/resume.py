from pydantic import BaseModel

from information_retrieval.api.v1.models.activity import Activity


class ParseResumeAndReturnActivitiesRequest(BaseModel):
    user_id: str


class ParseResumeAndReturnActivitiesResponse(BaseModel):
    activities: list[Activity]
