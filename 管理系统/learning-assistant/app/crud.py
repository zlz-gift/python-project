from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    try:
        return pwd_context.verify(plain, hashed)
    except:
        return False

def create_user(db: Session, username: str, password: str):
    hashed_password = get_password_hash(password)
    user = models.User(username=username, password=hashed_password)

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "username": user.username
    }

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()