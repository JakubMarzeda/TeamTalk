from pydantic import BaseModel
from typing import List

class GroupSchema(BaseModel):
    id: str
    name: str
    members: List[str]
    created_date: str
    updated_date: str