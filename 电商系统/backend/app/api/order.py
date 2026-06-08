from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.session import get_db
from app.models.order import Order, OrderItem
from app.models.cart import Cart
from app.models.product import Product
from app.models.user import User
from app.core.deps import get_current_user

router = APIRouter()


@router.post("/create")
async def create_order(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """下单（异步 + 事务）：
    1. 查询购物车 JOIN 商品
    2. 检查库存
    3. 计算总价
    4. 创建订单 + 订单明细
    5. 扣减库存
    6. 清空购物车
    7. 统一提交
    """
    # ── 1. 查购物车 ──
    result = await db.execute(
        select(Cart, Product)
        .join(Product, Cart.product_id == Product.id)
        .where(Cart.user_id == current_user.id)
    )
    carts = result.all()

    if not carts:
        raise HTTPException(status_code=400, detail="购物车为空")

    # ── 2. 检查库存 ──
    for cart, product in carts:
        if product.stock < cart.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"商品「{product.name}」库存不足（剩余 {product.stock}）",
            )

    # ── 3. 计算总价 ──
    total_price = sum(product.price * cart.quantity for cart, product in carts)

    # ── 4. 创建订单 ──
    order = Order(  # type: ignore[call-arg]
        user_id=current_user.id,
        total_price=total_price,
        status="已下单",
    )
    db.add(order)
    await db.flush()  # 拿到 order.id，但不提交

    # ── 5. 创建订单明细 + 扣库存 ──
    items = []
    for cart, product in carts:
        item = OrderItem(  # type: ignore[call-arg]
            order_id=order.id,
            product_id=product.id,
            quantity=cart.quantity,
            price=product.price,
        )
        db.add(item)
        product.stock -= cart.quantity  # type: ignore[assignment]
        items.append({
            "product_id": product.id,
            "name": product.name,
            "quantity": cart.quantity,
            "price": product.price,
        })

    # ── 6. 清空购物车 ──
    await db.execute(delete(Cart).where(Cart.user_id == current_user.id))

    # ── 7. 提交事务 ──
    await db.commit()

    return {
        "msg": "下单成功",
        "order_id": order.id,
        "total_price": total_price,
        "status": order.status,
        "items": items,
    }


@router.get("/")
async def get_orders(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """订单列表（异步 + 预加载关联，解决 N+1 问题）"""
    result = await db.execute(
        select(Order)
        .options(selectinload(Order.items))
        .where(Order.user_id == current_user.id)
        .order_by(Order.id.desc())
    )
    orders = result.scalars().unique().all()

    return [
        {
            "id": order.id,
            "total_price": order.total_price,
            "status": order.status,
            "items": [
                {
                    "product_id": item.product_id,
                    "quantity": item.quantity,
                    "price": item.price,
                }
                for item in order.items
            ],
        }
        for order in orders
    ]


@router.get("/{order_id}")
async def get_order_detail(
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """订单详情（异步 + JOIN 商品表）"""
    order_result = await db.execute(
        select(Order).where(
            Order.id == order_id,
            Order.user_id == current_user.id,
        )
    )
    order = order_result.scalar_one_or_none()

    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")

    # JOIN 商品表获取详情
    items_result = await db.execute(
        select(OrderItem, Product)
        .join(Product, OrderItem.product_id == Product.id)
        .where(OrderItem.order_id == order.id)
    )
    rows = items_result.all()

    return {
        "id": order.id,
        "total_price": order.total_price,
        "status": order.status,
        "items": [
            {
                "product_id": item.product_id,
                "name": product.name,
                "quantity": item.quantity,
                "price": item.price,
            }
            for item, product in rows
        ],
    }
