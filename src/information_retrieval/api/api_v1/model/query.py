from typing import List, Optional

from pydantic import BaseModel


class Query(BaseModel):
    user_email: str
    query: str


class RAGResponse(BaseModel):
    user_email: str
    query: str
    response: str
    citations: List
    documents: List


class GetActivitiesForUser(BaseModel):
    user_id: str
    start_date: Optional[str]
    in_progress_only: Optional[bool] = False
