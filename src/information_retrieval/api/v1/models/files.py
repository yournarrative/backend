from pydantic import BaseModel

from information_retrieval.api.v1.models.activity import Activity


class UploadResumeRequest(BaseModel):
    user_id: str


class GetResumeRequest(BaseModel):
    user_id: str


class ParseExistingResumeRequest(BaseModel):
    user_id: str


class ParseExistingResumeResponse(BaseModel):
    activities: list[Activity]


class UploadProfilePictureRequest(BaseModel):
    user_id: str


class GetProfilePictureRequest(BaseModel):
    user_id: str
