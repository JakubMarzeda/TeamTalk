from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from ..models.users import Users
from ..schemas.user import UserSchema
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter()

async def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return Users.objects(id=user_id).first()
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

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
