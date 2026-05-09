from fastapi import APIRouter
from fastapi import Depends
from app.models.product import Product
from sqlalchemy.orm import Session

from app.db.session import get_db

from app.models.cart import Cart

from app.models.user import User

from app.schemas.cart import CartCreate

from app.core.deps import get_current_user

router = APIRouter(
    prefix="/cart",
    tags=["购物车"]
)


@router.post("/")
def add_cart(

        data: CartCreate,

        db: Session = Depends(get_db),

        current_user: User = Depends(
            get_current_user
        )
):

    cart = Cart(

        user_id=current_user.id,

        product_id=data.product_id,

        quantity=data.quantity
    )

    db.add(cart)

    db.commit()

    return {
        "msg": "加入购物车成功"
    }

@router.get("/")
def get_cart(

        db: Session = Depends(get_db),

        current_user: User = Depends(
            get_current_user
        )
):

    carts = db.query(
        Cart,
        Product
    ).join(
        Product,
        Cart.product_id == Product.id
    ).filter(
        Cart.user_id == current_user.id
    ).all()

    result = []

    for cart, product in carts:

        result.append({

            "cart_id": cart.id,

            "product_id": product.id,

            "name": product.name,

            "price": product.price,

            "quantity": cart.quantity,

            "image": product.image
        })

    return result

@router.delete("/{cart_id}")
def delete_cart(

        cart_id: int,

        db: Session = Depends(get_db),

        current_user: User = Depends(
            get_current_user
        )
):

    cart = db.query(Cart).filter(

        Cart.id == cart_id,

        Cart.user_id == current_user.id

    ).first()

    if not cart:

        return {
            "msg": "购物车不存在"
        }

    db.delete(cart)

    db.commit()

    return {
        "msg": "删除成功"
    }