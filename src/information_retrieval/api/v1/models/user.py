from typing import Optional

from pydantic import BaseModel


class NarrativeUser(BaseModel):
    user_id: str
    email: Optional[str] = None
    bio: Optional[str] = None
    phone_number: Optional[str] = None
    current_organization: Optional[str] = None
    linkedin_profile_url: Optional[str] = None
    loom_url: Optional[str] = None
    resume_file_name: Optional[str] = None


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
