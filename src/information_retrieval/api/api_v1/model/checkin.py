from typing import List

from pydantic import BaseModel


class CheckIn(BaseModel):
    dialogue: List[str]
