from typing import Optional

from pydantic import BaseModel, Field


class Activity(BaseModel):
    title: str = Field(..., description="The inferred title of this activity, summarizing what it's about.")
    description: str = Field(..., description="The description of this activity. What has the person said about it?")
    # TODO: Check if the AI returned value is actualy in one of these options for each field
    category: str = Field(
        ...,
        description="The category of this activity. "
        "Choices are ['Skill', 'Achievement', 'Endorsement', 'Miscellaneous']",
    )
    status: str = Field(
        ...,
        description="The status of this activity. "
        "Choices are ['Not Started', 'In Progress', 'Completed', 'Archived']",
    )
    organization: Optional[str] = Field(None, description="The Organization associated with this Activity, if any.")


class ActivityWithID(Activity):
    id: str


class UpdateActivityWithNewDetailsRequest(BaseModel):
    activity_id: str
    update: str


class UpdateActivityWithNewDetailsResponse(BaseModel):
    activity_with_id: ActivityWithID


class UpsertActivityRequest(BaseModel):
    activity_with_id: ActivityWithID


class CreateActivitiesFromCheckInRequest(BaseModel):
    dialogue: list[str]


class CreateActivitiesFromCheckInResponse(BaseModel):
    activities: list[Activity]


class InsertActivitiesForUserRequest(BaseModel):
    user_id: str
    activities: list[Activity]


class GetActivitiesRequest(BaseModel):
    user_id: str
    start_date: Optional[str] = None
    in_progress_only: Optional[bool] = False


class GetActivitiesResponse(BaseModel):
    user_id: str
    activities: list[ActivityWithID]


class DeleteActivitiesRequest(BaseModel):
    activity_id_list: list[str]
