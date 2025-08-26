from datetime import timedelta
from fastapi import APIRouter, HTTPException, status , Depends
from app.core.security import (verify_password, get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES)
from app.repositories.user_repo import UserRepository
from app.models.user_model import UserCreate, UserPublic 
from fastapi.security import HTTPBearer



auth_router = APIRouter(prefix="/auth", tags=["auth"])
repo = UserRepository()

@auth_router.post("/register", response_model=UserPublic, status_code=201)
def register(payload: UserCreate):

    if repo.get_by_username(payload.username):
    
        raise HTTPException(status_code=409, detail="Username already exists")
    
    uid = repo.create_user(payload.username, get_password_hash(payload.password))
    
    return UserPublic(id=uid, username=payload.username)

@auth_router.post("/login")

def login(payload: HTTPBearer = Depends(HTTPBearer())):
    token = payload.credentials
    try:
        decoded = create_access_token({"uid": token}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        user = repo.get_by_id(token)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        return {"access_token": decoded, "token_type": "bearer"}
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid credentials")