from typing import Optional

from pydantic import BaseModel, Field
from pydantic.v1 import validator


class Activity(BaseModel):
    title: str = Field(..., description="The inferred title of this activity, summarizing what it's about.")
    description: str = Field(..., description="The description of this activity. What has the person said about it?")
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

    @validator("title", pre=True, always=True)
    def normalize_title(cls, value):
        if isinstance(value, str):
            return value.strip()[:100]
        return value

    @validator("description", pre=True, always=True)
    def normalize_description(cls, value):
        if isinstance(value, str):
            return value.strip()[:1000]
        return value

    @validator("category", pre=True, always=True)
    def verify_category(cls, value):
        choices = ["Skill", "Achievement", "Endorsement", "Miscellaneous"]
        if value in choices:
            return value
        else:
            return "Miscellaneous"

    @validator("status", pre=True, always=True)
    def verify_status(cls, value):
        choices = ["Not Started", "In Progress", "Completed", "Archived"]
        if value in choices:
            return value
        else:
            return "Completed"


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


class UserOrganizationData(BaseModel):
    summary: str
    activities: list[ActivityWithID]


class GetActivitiesForDisplayRequest(BaseModel):
    user_id: str
    include_summaries: bool = False


class GetActivitiesForDisplayResponse(BaseModel):
    user_organization_data_map: dict[str, UserOrganizationData]
