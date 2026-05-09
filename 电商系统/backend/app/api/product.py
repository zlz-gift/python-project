from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.db.session import get_db

from app.schemas.product import ProductCreate

from app.models.product import Product

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

        image=product.image
    )

    db.add(new_product)

    db.commit()

    return {
        "msg": "商品创建成功"
    }


@router.get("/")
def get_products(
        db: Session = Depends(get_db)
):

    products = db.query(Product).all()

    return products