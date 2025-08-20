from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
)
from app.repositories.user_repo import UserRepository
from app.models.user_model import UserCreate, Token, UserPublic
from app.deps import get_current_user
auth_router = APIRouter(prefix="/auth", tags=["auth"])
repo = UserRepository()

@auth_router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = repo.get_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": user["username"], "uid": str(user["_id"])},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}


@auth_router.post("/register", response_model=UserPublic, status_code=201)
def register(payload: UserCreate):
    existing = repo.get_by_username(payload.username)
    if existing:
        raise HTTPException(status_code=409, detail="Username already exists")
    uid = repo.create_user(payload.username, get_password_hash(payload.password))
    return {"id": uid, "username": payload.username}

