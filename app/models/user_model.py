from typing import Optional
from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=128)

class UserLogin(BaseModel):
    username: str
    password: str


class UserPublic(BaseModel):
    id: str
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    sub: Optional[str] = None  
    uid: Optional[str] = None  
