from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductUpdate
from app.models.product import Product
from app.core.deps import require_admin, get_current_user
from app.core.cache import (
    get_cache,
    cache_get,
    cache_set,
    cache_delete,
    cache_delete_pattern,
    CACHE_TTL_SHORT,
    CACHE_TTL_MEDIUM,
    CACHE_TTL_LONG,
)

from redis.asyncio import Redis
from typing import Optional

router = APIRouter(prefix="/products", tags=["商品模块"])


# ──────────────────────────────────────────────
# 辅助函数：构建商品列表缓存键
# ──────────────────────────────────────────────
def _product_list_key(
    keyword: Optional[str],
    category: Optional[str],
    min_price: Optional[float],
    max_price: Optional[float],
    page: int,
    page_size: int,
) -> str:
    return f"products:list:{keyword or '_'}:{category or '_'}:{min_price or '_'}:{max_price or '_'}:{page}:{page_size}"


# ──────────────────────────────────────────────
# POST /products/ — 创建商品（管理员）
# ──────────────────────────────────────────────
@router.post("/")
async def create_product(
    product: ProductCreate,
    db: AsyncSession = Depends(get_db),
    _: Product = Depends(require_admin),
    cache: Optional[Redis] = Depends(get_cache),
):
    new_product = Product(  # type: ignore[call-arg]
        name=product.name,
        price=product.price,
        stock=product.stock,
        description=product.description,
        category=product.category,
        image=product.image,
    )
    db.add(new_product)
    await db.commit()

    # 清除商品列表缓存和分类缓存
    await cache_delete_pattern(cache, "products:list:*")
    await cache_delete(cache, "products:categories")

    return {"msg": "商品创建成功", "id": new_product.id}


# ──────────────────────────────────────────────
# GET /products/ — 商品列表（搜索 + 分页 + Redis 缓存）
# ──────────────────────────────────────────────
@router.get("/")
async def get_products(
    keyword: str = Query(default=None, description="搜索关键词（匹配商品名称）"),
    category: str = Query(default=None, description="分类筛选"),
    min_price: float = Query(default=None, description="最低价格"),
    max_price: float = Query(default=None, description="最高价格"),
    page: int = Query(default=1, ge=1, description="页码"),
    page_size: int = Query(default=12, ge=1, le=100, description="每页数量"),
    db: AsyncSession = Depends(get_db),
    cache: Optional[Redis] = Depends(get_cache),
):
    """商品搜索列表 — 优先走 Redis 缓存，miss 时查数据库"""
    cache_key = _product_list_key(keyword, category, min_price, max_price, page, page_size)

    # ── 尝试从缓存读取 ──
    cached = await cache_get(cache, cache_key)
    if cached is not None:
        return cached

    # ── 缓存 miss → 查数据库 ──
    stmt = select(Product)

    if keyword:
        stmt = stmt.where(Product.name.ilike(f"%{keyword}%"))
    if category:
        stmt = stmt.where(Product.category == category)
    if min_price is not None:
        stmt = stmt.where(Product.price >= min_price)
    if max_price is not None:
        stmt = stmt.where(Product.price <= max_price)

    # 总数
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total_result = await db.execute(count_stmt)
    total = total_result.scalar_one()

    # 分页
    offset = (page - 1) * page_size
    result = await db.execute(stmt.offset(offset).limit(page_size))
    products = result.scalars().all()

    response = {
        "items": products,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size if total > 0 else 1,
    }

    # ── 写入缓存 ──
    await cache_set(cache, cache_key, response, ttl=CACHE_TTL_SHORT)

    return response


# ──────────────────────────────────────────────
# GET /products/categories — 分类列表（Redis 缓存）
# ──────────────────────────────────────────────
@router.get("/categories")
async def get_categories(
    db: AsyncSession = Depends(get_db),
    cache: Optional[Redis] = Depends(get_cache),
):
    """获取所有商品分类 — Redis 缓存 10 分钟"""
    cached = await cache_get(cache, "products:categories")
    if cached is not None:
        return cached

    result = await db.execute(select(Product.category).distinct())
    categories = [c[0] for c in result.all() if c[0]]

    await cache_set(cache, "products:categories", categories, ttl=CACHE_TTL_LONG)
    return categories


# ──────────────────────────────────────────────
# GET /products/{product_id} — 商品详情（Redis 缓存）
# ──────────────────────────────────────────────
@router.get("/{product_id}")
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    cache: Optional[Redis] = Depends(get_cache),
):
    """商品详情 — 优先读缓存"""
    cache_key = f"product:{product_id}"
    cached = await cache_get(cache, cache_key)
    if cached is not None:
        return cached

    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")

    await cache_set(cache, cache_key, product, ttl=CACHE_TTL_MEDIUM)
    return product


# ──────────────────────────────────────────────
# PUT /products/{product_id} — 更新商品（管理员）
# ──────────────────────────────────────────────
@router.put("/{product_id}")
async def update_product(
    product_id: int,
    data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    _: Product = Depends(require_admin),
    cache: Optional[Redis] = Depends(get_cache),
):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")

    update_data = data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)

    await db.commit()

    # 清除相关缓存
    await cache_delete(cache, f"product:{product_id}")
    await cache_delete_pattern(cache, "products:list:*")
    await cache_delete(cache, "products:categories")

    return {"msg": "商品更新成功"}


# ──────────────────────────────────────────────
# DELETE /products/{product_id} — 删除商品（管理员）
# ──────────────────────────────────────────────
@router.delete("/{product_id}")
async def delete_product(
    product_id: int,
    db: AsyncSession = Depends(get_db),
    _: Product = Depends(require_admin),
    cache: Optional[Redis] = Depends(get_cache),
):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()

    if not product:
        raise HTTPException(status_code=404, detail="商品不存在")

    await db.delete(product)
    await db.commit()

    # 清除相关缓存
    await cache_delete(cache, f"product:{product_id}")
    await cache_delete_pattern(cache, "products:list:*")
    await cache_delete(cache, "products:categories")

    return {"msg": "商品删除成功"}
