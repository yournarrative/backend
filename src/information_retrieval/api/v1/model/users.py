from pydantic import BaseModel


class NarrativeUser(BaseModel):
    user_id: str
    email: str


class GetUserDataRequest(BaseModel):
    user_id: str


class GetUserDataResponse(BaseModel):
    user_data: NarrativeUser
