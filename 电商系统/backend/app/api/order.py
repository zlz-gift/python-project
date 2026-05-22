from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.order import Order, OrderItem
from app.models.cart import Cart
from app.models.product import Product
from app.models.user import User
from app.core.deps import get_current_user

router = APIRouter()


@router.post("/create")
def create_order(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    carts = db.query(Cart, Product).join(
        Product, Cart.product_id == Product.id
    ).filter(
        Cart.user_id == current_user.id
    ).all()

    if not carts:
        raise HTTPException(status_code=400, detail="购物车为空")

    for cart, product in carts:
        if product.stock < cart.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"商品「{product.name}」库存不足（剩余 {product.stock}）"
            )

    total_price = sum(product.price * cart.quantity for cart, product in carts)

    order = Order(
        user_id=current_user.id,
        total_price=total_price,
        status="已下单"
    )
    db.add(order)
    db.flush()

    items = []
    for cart, product in carts:
        item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=cart.quantity,
            price=product.price
        )
        db.add(item)
        product.stock -= cart.quantity
        items.append({
            "product_id": product.id,
            "name": product.name,
            "quantity": cart.quantity,
            "price": product.price
        })

    db.query(Cart).filter(
        Cart.user_id == current_user.id
    ).delete()

    db.commit()

    return {
        "msg": "下单成功",
        "order_id": order.id,
        "total_price": total_price,
        "status": order.status,
        "items": items
    }


@router.get("/")
def get_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    orders = db.query(Order).filter(
        Order.user_id == current_user.id
    ).order_by(Order.id.desc()).all()

    result = []
    for order in orders:
        items = db.query(OrderItem).filter(
            OrderItem.order_id == order.id
        ).all()

        result.append({
            "id": order.id,
            "total_price": order.total_price,
            "status": order.status,
            "items": [
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price": item.price
                }
                for item in items
            ]
        })

    return result


@router.get("/{order_id}")
def get_order_detail(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    items = db.query(OrderItem, Product).join(
        Product, OrderItem.product_id == Product.id
    ).filter(
        OrderItem.order_id == order.id
    ).all()

    return {
        "id": order.id,
        "total_price": order.total_price,
        "status": order.status,
        "items": [
            {
                "product_id": item.product_id,
                "name": product.name,
                "quantity": item.quantity,
                "price": item.price
            }
            for item, product in items
        ]
    }
