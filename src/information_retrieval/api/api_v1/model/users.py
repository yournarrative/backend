from pydantic import BaseModel


class NarrativeUser(BaseModel):
    id: str
    email: str
