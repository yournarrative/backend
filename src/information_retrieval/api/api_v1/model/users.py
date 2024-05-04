from pydantic import BaseModel


class NarrativeUser(BaseModel):
    first_name: str
    last_name: str
    email: str
