from typing import List

from pydantic import BaseModel


class Activity(BaseModel):
    title: str
    description: str
    category: str
    status: str


class UserActivities(BaseModel):
    user_id: str
    activities: List[Activity]
