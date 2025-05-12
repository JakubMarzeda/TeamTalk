from fastapi import APIRouter, HTTPException
from ..models.groups import Groups
from ..schemas.group import GroupSchema

router = APIRouter()

@router.post("/groups/")
async def create_group(group: GroupSchema):
    new_group = Groups(**group.dict())
    new_group.save()
    return {"message": "Group created", "group_id": str(new_group.id)}

@router.get("/groups/")
async def list_groups():
    groups = Groups.objects()
    return list(groups)

@router.get("/groups/{group_id}")
async def get_group(group_id: str):
    group = Groups.objects(id=group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group

@router.put("/groups/{group_id}")
async def update_group(group_id: str, group: GroupSchema):
    Groups.objects(id=group_id).update(**group.dict())
    return {"message": "Group updated"}

@router.delete("/groups/{group_id}")
async def delete_group(group_id: str):
    result = Groups.objects(id=group_id).delete()
    if result == 0:
        raise HTTPException(status_code=404, detail="Group not found")
    return {"message": "Group deleted"}

@router.post("/groups/{group_id}/join")
async def join_group(group_id: str, user_id: str):
    group = Groups.objects(id=group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    group.members.append(user_id)
    group.save()
    return {"message": "User joined the group"}

@router.post("/groups/{group_id}/leave")
async def leave_group(group_id: str, user_id: str):
    group = Groups.objects(id=group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    group.members.remove(user_id)
    group.save()
    return {"message": "User left the group"}