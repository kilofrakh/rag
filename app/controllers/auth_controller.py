from datetime import timedelta
from fastapi import APIRouter, HTTPException
from fastapi.security import HTTPBearer
from app.core.security import (verify_password,get_password_hash,create_access_token,ACCESS_TOKEN_EXPIRE_MINUTES)
from app.repositories.user_repo import UserRepository
from app.models.user_model import UserCreate, UserLogin, UserPublic
from fastapi.responses import JSONResponse


auth_router = APIRouter(prefix="/auth", tags=["auth"])
repo = UserRepository()
security = HTTPBearer()



@auth_router.post("/register", response_model=UserPublic, status_code=201)
def register(payload: UserCreate):
    existing = repo.get_by_username(payload.username)
    if existing:
        raise HTTPException(status_code=409, detail="Username already exists")
    
    uid = repo.create_user(payload.username, get_password_hash(payload.password))
    return UserPublic(id=str(uid), username=payload.username)

@auth_router.post("/login")
def login(payload: UserLogin):
    user = repo.get_by_username(payload.username)
    if not user or not verify_password(payload.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"uid": str(user["_id"])}, 
        expires_delta=access_token_expires
    )
    
    headers = {"Authorization": f"Bearer {access_token}"}
    return JSONResponse(
        content={"access_token": access_token, "token_type": "bearer"},
        headers=headers
    )



