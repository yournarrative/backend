from typing import List, Optional

from pydantic import BaseModel
from pydantic import Field


class Activity(BaseModel):
    title: str = Field(..., description="The inferred title of this activity, summarizing what it's about.")
    description: str = Field(..., description="The description of this activity. What has the person said about it?")
    category: str = Field(..., description="The category of this activity. Choices are ['Skill', 'Achievement', 'Endorsement', 'Miscellaneous']")
    status: str = Field(..., description="The status of this activity. Choices are ['Not Started', 'In Progress', 'Completed', 'Archived']")


class ActivityWithID(Activity):
    id: str


class InsertActivitiesForUserRequest(BaseModel):
    user_id: str
    activities: List[Activity]


class GetActivitiesForUserRequest(BaseModel):
    user_id: str
    start_date: Optional[str]
    in_progress_only: Optional[bool] = False


class GetActivitiesForUserResponse(BaseModel):
    user_id: str
    activities: List[ActivityWithID]
