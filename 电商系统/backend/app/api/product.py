from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Query

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.product import ProductCreate
from app.schemas.product import ProductUpdate

from app.models.product import Product
from app.core.deps import require_admin

router = APIRouter(
    prefix="/products",
    tags=["商品模块"]
)


@router.post("/")
def create_product(
        product: ProductCreate,
        db: Session = Depends(get_db)
):

    new_product = Product(
        name=product.name,
        price=product.price,
        stock=product.stock,
        description=product.description,
        category=product.category,
        image=product.image
    )

    db.add(new_product)

    db.commit()

    return {
        "msg": "商品创建成功"
    }


@router.get("/")
def get_products(
        keyword: str = Query(default=None, description="搜索关键词（匹配商品名称）"),
        category: str = Query(default=None, description="分类筛选"),
        min_price: float = Query(default=None, description="最低价格"),
        max_price: float = Query(default=None, description="最高价格"),
        db: Session = Depends(get_db)
):
    query = db.query(Product)

    if keyword:
        query = query.filter(Product.name.ilike(f"%{keyword}%"))

    if category:
        query = query.filter(Product.category == category)

    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    products = query.all()

    return products


@router.get("/{product_id}")
def get_product(
        product_id: int,
        db: Session = Depends(get_db)
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="商品不存在"
        )

    return product


@router.put("/{product_id}")
def update_product(
        product_id: int,
        data: ProductUpdate,
        db: Session = Depends(get_db),
        _: Product = Depends(require_admin)
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="商品不存在"
        )

    update_data = data.dict(exclude_unset=True)

    for field, value in update_data.items():
        setattr(product, field, value)

    db.commit()

    return {
        "msg": "商品更新成功"
    }


@router.delete("/{product_id}")
def delete_product(
        product_id: int,
        db: Session = Depends(get_db),
        _: Product = Depends(require_admin)
):
    product = db.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="商品不存在"
        )

    db.delete(product)

    db.commit()

    return {
        "msg": "商品删除成功"
    }