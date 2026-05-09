from sqlalchemy import Column, Integer, String, ForeignKey, Float
from app.db.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))

    total_price = Column(Float)

    status = Column(String(20), default="待支付")
