from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud
from app.utils import create_access_token
from app import schemas
from app.deps import get_current_user
from app import models
router = APIRouter(prefix="/user")

@router.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):

    # 💥 先查是否存在
    exist = crud.get_user_by_username(db, user.username)

    if exist:
        return {"error": "用户名已存在"}

    return crud.create_user(db, user.username, user.password)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)):

    user = crud.get_user_by_username(db, form_data.username)

    if not user or not crud.verify_password(form_data.password, user.password):
        return {"error": "用户名或密码错误"}

    token = create_access_token({"sub": user.username})
    print("🔥 login函数被调用")
    return {
        "access_token": token,
        "token_type": "bearer"
    }

# 🔥 受保护接口
@router.get("/me")
def get_me(current_user: str = Depends(get_current_user)):
    return {"username": current_user}


@router.get("/list")
def get_user_list(db: Session = Depends(get_db)):
    users = db.query(models.User).all()

    return {
        "code": 0,
        "message": "success",
        "data": {
            "list": [
                {
                    "id": u.id,
                    "username": u.username
                }
                for u in users
            ],
            "total": len(users)
        }
    }

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        return {"error": "用户不存在"}

    db.delete(user)
    db.commit()

    return {"msg": "删除成功"}

from app.crud import get_password_hash
from sqlalchemy.exc import IntegrityError

@router.put("/{user_id}")
def update_user(user_id: int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()

    if not db_user:
        return {"error": "用户不存在"}

    # 💥 检查用户名是否重复（排除自己）
    exist = db.query(models.User).filter(
        models.User.username == user.username,
        models.User.id != user_id
    ).first()

    if exist:
        return {"error": "用户名已存在"}

    try:
        # 更新用户名
        db_user.username = user.username

        # 🔥 密码可选更新 + 必须加密
        if user.password:
            db_user.password = get_password_hash(user.password)

        db.commit()

    except IntegrityError:
        db.rollback()
        return {"error": "更新失败"}

    return {"msg": "更新成功"}