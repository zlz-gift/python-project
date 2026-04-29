from sqlalchemy import Column, Integer, String
from app.database import Base
from app import models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True)
    email = Column(String(100))
    password = Column(String(100))