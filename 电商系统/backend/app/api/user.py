from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import UserRegister
from app.models.user import User
from app.core.security import hash_password
from fastapi import HTTPException
from app.core.deps import get_current_user
from app.schemas.user import UserLogin
from fastapi import Header
from app.core.security import (
    verify_password,
    create_access_token
)
router = APIRouter(
    tags=["用户"]
)

@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):

    new_user = User(
        username=user.username,
        password=hash_password(user.password),
        nickname=user.nickname,
        role=user.role
    )

    db.add(new_user)

    db.commit()

    return {
        "msg": "注册成功"
    }

@router.post("/login")
def login(
        user: UserLogin,
        db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.username == user.username
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=400,
            detail="用户不存在"
        )

    if not verify_password(
            user.password,
            db_user.password
    ):
        raise HTTPException(
            status_code=400,
            detail="密码错误"
        )

    token = create_access_token(
        {
            "user_id": db_user.id,
            "role": db_user.role
        }
    )

    return {
        "msg": "登录成功",
        "token": token
    }

@router.get("/userinfo")
def userinfo(

    current_user: User = Depends(
        get_current_user
    )
):

    return {

        "id": current_user.id,

        "username": current_user.username,

        "nickname": current_user.nickname,

        "role": current_user.role
    }