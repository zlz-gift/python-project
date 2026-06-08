from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.cart import Cart
from app.models.product import Product
from app.models.user import User
from app.schemas.cart import CartCreate, CartUpdate
from app.core.deps import get_current_user

router = APIRouter(prefix="/cart", tags=["购物车"])


@router.post("/")
async def add_cart(
    data: CartCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """加入购物车（异步）"""
    cart = Cart(  # type: ignore[call-arg]
        user_id=current_user.id,
        product_id=data.product_id,
        quantity=data.quantity,
    )
    db.add(cart)
    await db.commit()

    return {"msg": "加入购物车成功"}


@router.get("/")
async def get_cart(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """查看购物车 — JOIN 商品表获取详情（异步）"""
    result = await db.execute(
        select(Cart, Product)
        .join(Product, Cart.product_id == Product.id)
        .where(Cart.user_id == current_user.id)
    )
    rows = result.all()

    items = []
    for cart, product in rows:
        items.append({
            "cart_id": cart.id,
            "product_id": product.id,
            "name": product.name,
            "price": product.price,
            "quantity": cart.quantity,
            "image": product.image,
        })

    return items


@router.put("/{cart_id}")
async def update_cart(
    cart_id: int,
    data: CartUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """修改购物车商品数量（异步）"""
    result = await db.execute(
        select(Cart).where(Cart.id == cart_id, Cart.user_id == current_user.id)
    )
    cart = result.scalar_one_or_none()

    if not cart:
        raise HTTPException(status_code=404, detail="购物车不存在")

    cart.quantity = data.quantity  # type: ignore[assignment]
    await db.commit()

    return {"msg": "更新成功"}


@router.delete("/{cart_id}")
async def delete_cart(
    cart_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """删除购物车商品（异步）"""
    result = await db.execute(
        select(Cart).where(Cart.id == cart_id, Cart.user_id == current_user.id)
    )
    cart = result.scalar_one_or_none()

    if not cart:
        raise HTTPException(status_code=404, detail="购物车不存在")

    await db.delete(cart)
    await db.commit()

    return {"msg": "删除成功"}
