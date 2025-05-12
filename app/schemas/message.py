from pydantic import BaseModel
from typing import Optional

class MessageSchema(BaseModel):
    id: str
    sender_id: str
    recipient_user_id: Optional[str] = None
    recipient_group_id: Optional[str] = None
    content: str
    sent_date: str
    updated_date: str