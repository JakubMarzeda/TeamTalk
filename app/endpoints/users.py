from fastapi import APIRouter, HTTPException, Depends
from ..schemas.user import UserSchema, GetUserSchema
from ..models.users import Users
from .auth import get_current_user, create_access_token

router = APIRouter(prefix="/users")

@router.get("/me", response_model=GetUserSchema)
async def get_current_user_data(current_user: Users = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return GetUserSchema(**current_user.to_dict())

@router.get("/{user_id}", response_model=GetUserSchema)
async def get_user(user_id: str, current_user: Users = Depends(get_current_user)):
    user = Users.objects(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return GetUserSchema(**user.to_dict())

@router.put("/{user_id}")
async def update_user(user_id: str, user: UserSchema, current_user: Users = Depends(get_current_user)):
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized to update this user")
    Users.objects(id=user_id).update(**user.dict())
    return {"message": "User updated"}

@router.delete("/{user_id}")
async def delete_user(user_id: str, current_user: Users = Depends(get_current_user)):
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized to delete this user")
    result = Users.objects(id=user_id).delete()
    if result == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
