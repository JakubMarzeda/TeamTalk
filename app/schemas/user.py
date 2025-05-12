from pydantic import BaseModel, EmailStr
from typing import List

class UserSchema(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: EmailStr
    groups: List[str]
    password: str