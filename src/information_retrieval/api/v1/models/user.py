from typing import Optional

from pydantic import BaseModel


class NarrativeUser(BaseModel):
    user_id: str
    email: Optional[str]
    bio: Optional[str]
    phone_number: Optional[str]
    current_organization: Optional[str]
    linkedin_profile_url: Optional[str]
    loom_url: Optional[str]


class GetUserProfileDataRequest(BaseModel):
    user_id: str


class GetUserProfileDataResponse(BaseModel):
    user_data: NarrativeUser


class UpdateUserProfileDataRequest(BaseModel):
    user_data: NarrativeUser


class GetAllOrganizationsForUserRequest(BaseModel):
    user_id: str


class GetAllOrganizationsForUserResponse(BaseModel):
    organizations: list[str]
