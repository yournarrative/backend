from typing import List

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
