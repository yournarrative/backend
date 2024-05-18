from typing import Optional, Dict, List

from pydantic import BaseModel

from information_retrieval.api.api_v1.model.activity import Activity


class BragDocUpdateRequest(BaseModel):
    user_id: str
    publish: bool
    url: Optional[str]


class BragDoc(BaseModel):
    user_id: str
    url: str
    published: bool
    brag_doc_id: Optional[str]
    activities_by_category: Optional[Dict[str, List[Activity]]] = None
