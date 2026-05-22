from pydantic import BaseModel
from typing import Optional

class UserRegister(BaseModel):
    username: str
    password: str
    nickname: str
    role: Optional[str] = "user"

class UserLogin(BaseModel):
    username: str
    password: str