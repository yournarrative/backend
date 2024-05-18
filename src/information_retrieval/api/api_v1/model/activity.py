from typing import List, Optional

from pydantic import BaseModel


class Activity(BaseModel):
    id: Optional[str]
    title: str
    description: str
    category: str
    status: str


class UserActivities(BaseModel):
    user_id: str
    activities: List[Activity]
