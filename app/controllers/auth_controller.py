from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import (
    verify_password, get_password_hash, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
)
from app.repositories.user_repo import UserRepository
from app.models.user_model import UserCreate, Token, UserPublic
from app.core.security import oauth2_scheme  # ensures docs show "Authorize" correctly

router = APIRouter(prefix="/auth", tags=["auth"])
repo = UserRepository()

@router.post("/register", response_model=UserPublic, status_code=201)
def register(payload: UserCreate):
    if repo.get_by_username(payload.username):
        raise HTTPException(status_code=409, detail="Username already exists")
    uid = repo.create_user(payload.username, get_password_hash(payload.password))
    return {"id": uid, "username": payload.username}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = repo.get_by_username(form_data.username)
    if not user or not verify_password(form_data.password, user["password_hash"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": user["username"], "uid": str(user["_id"])},
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserPublic)
def me(token: str = Depends(oauth2_scheme)):
    # lighter /me — decode only
    from app.core.security import decode_token
    from app.repositories.user_repo import UserRepository
    try:
        payload = decode_token(token)
        uid = payload.get("uid")
        username = payload.get("sub")
        if not uid or not username:
            raise HTTPException(status_code=401, detail="Invalid token")
        # ensure user still exists
        user = UserRepository().get_by_id(uid)
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return {"id": uid, "username": username}
    except Exception:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
