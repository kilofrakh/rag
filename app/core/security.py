from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.repositories.user_repo import UserRepository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
user_repo = UserRepository()

SECRET_KEY = "your-secret"
ALGORITHM = "HS256"

async def get_current_user(token: str = Depends(oauth2_scheme)):
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        uid: str = payload.get("uid")
        if username is None or uid is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = user_repo.get_by_id(uid)
        if not user or user.get("username") != username:
            raise HTTPException(status_code=401, detail="User not found")
        return {"id": uid, "username": username}
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")   
def get_password_hash(password: str) -> str:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.hash(password)               


def verify_password(plain_password: str, hashed_password: str) -> bool:
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return pwd_context.verify(plain_password, hashed_password)          

def create_access_token(data: dict, expires_delta: int = None) -> str:
    from datetime import datetime, timedelta
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
ACCESS_TOKEN_EXPIRE_MINUTES = 30


