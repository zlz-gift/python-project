from pydantic import BaseModel


class UserRegister(BaseModel):
    username: str
    password: str
    nickname: str


class UserLogin(BaseModel):
    username: str
    password: str