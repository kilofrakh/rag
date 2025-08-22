#app / deps
from fastapi import Depends, HTTPException, status
from jose import JWTError
from app.core.security import oauth2_scheme, decode_token
from app.repositories.user_repo import UserRepository
from app.models.user_model import TokenData

async def get_current_user(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    try:
        payload = decode_token(token)
        username: str = payload.get("sub")
        uid: str = payload.get("uid")
        if username is None or uid is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        repo = UserRepository()
        user = repo.get_by_id(uid)
        if not user or user.get("username") != username:
            raise HTTPException(status_code=401, detail="User not found")
        # return a minimal user object
        return {"id": uid, "username": username}
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
