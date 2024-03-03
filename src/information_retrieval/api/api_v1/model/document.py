from pydantic import BaseModel


class InsertDocument(BaseModel):
    user_email: str
    content: str
    question: str
    document_type: str


class RetrieveDocument(BaseModel):
    content: str
