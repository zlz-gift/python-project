from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.order import Order

router = APIRouter()


@router.post("/create")
def create_order(user_id: int, total_price: float, db: Session = Depends(get_db)):

    order = Order(
        user_id=user_id,
        total_price=total_price
    )

    db.add(order)
    db.commit()
    db.refresh(order)

    return {
        "msg": "创建订单成功",
        "order_id": order.id
    }