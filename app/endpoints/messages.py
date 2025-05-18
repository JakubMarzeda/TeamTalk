from fastapi import APIRouter, Depends
from ..models.messages import Messages
from ..models.users import Users
from .auth import get_current_user

router = APIRouter(prefix="/messages")

@router.post("/private")
async def send_private_message(recipient_user_id: str, content: str, current_user: Users = Depends(get_current_user)):
    message = Messages(sender=current_user, recipient_user=recipient_user_id, content=content)
    message.save()
    return {"message": "Private message sent", "message_id": str(message.id)}

@router.post("/group")
async def send_group_message(recipient_group_id: str, content: str, current_user: Users = Depends(get_current_user)):
    message = Messages(sender=current_user, recipient_group=recipient_group_id, content=content)
    message.save()
    return {"message": "Group message sent", "message_id": str(message.id)}

@router.get("/private/{user_id}")
async def get_private_messages(user_id: str, current_user: Users = Depends(get_current_user)):
    messages = Messages.objects(sender=current_user, recipient_user=user_id) | Messages.objects(sender=user_id, recipient_user=current_user)
    return list(messages)

@router.get("/group/{group_id}")
async def get_group_messages(group_id: str):
    messages = Messages.objects(recipient_group=group_id)
    return list(messages)
