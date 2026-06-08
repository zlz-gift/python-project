from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.user import UserRegister, UserLogin
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.core.deps import get_current_user

router = APIRouter(tags=["用户"])


@router.post("/register")
async def register(user: UserRegister, db: AsyncSession = Depends(get_db)):
    """用户注册（异步）"""
    # 检查用户名是否已存在
    result = await db.execute(select(User).where(User.username == user.username))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="用户名已存在")

    new_user = User(  # type: ignore[call-arg]
        username=user.username,
        password=hash_password(user.password),
        nickname=user.nickname,
        role=user.role,
    )
    db.add(new_user)
    await db.commit()

    return {"msg": "注册成功"}


@router.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    """用户登录（异步）"""
    result = await db.execute(select(User).where(User.username == user.username))
    db_user = result.scalar_one_or_none()

    if not db_user:
        raise HTTPException(status_code=400, detail="用户不存在")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="密码错误")

    token = create_access_token({
        "user_id": db_user.id,
        "role": db_user.role,
    })

    return {"msg": "登录成功", "token": token}


@router.get("/userinfo")
async def userinfo(current_user: User = Depends(get_current_user)):
    """获取当前用户信息（异步）"""
    return {
        "id": current_user.id,
        "username": current_user.username,
        "nickname": current_user.nickname,
        "role": current_user.role,
    }
