from fastapi import APIRouter, HTTPException, Depends
from ..schemas.user import UserSchema
from ..models.users import Users
from .auth import get_current_user, create_access_token

router = APIRouter()

@router.post("/auth/register")
async def register(user: UserSchema):
    new_user = Users(**user.dict())
    new_user.save()
    return {"message": "User registered", "user_id": str(new_user.id)}

@router.post("/auth/login")
async def login(email: str, password: str):
    user = Users.objects(email=email, password=password).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = await create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me")
async def get_current_user_data(current_user: Users = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return current_user

@router.get("/users/{user_id}")
async def get_user(user_id: str, current_user: Users = Depends(get_current_user)):
    user = Users.objects(id=user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}")
async def update_user(user_id: str, user: UserSchema, current_user: Users = Depends(get_current_user)):
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized to update this user")
    Users.objects(id=user_id).update(**user.dict())
    return {"message": "User updated"}

@router.delete("/users/{user_id}")
async def delete_user(user_id: str, current_user: Users = Depends(get_current_user)):
    if str(current_user.id) != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized to delete this user")
    result = Users.objects(id=user_id).delete()
    if result == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}
