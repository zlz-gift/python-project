from typing import Optional

from pydantic import BaseModel


class ProductCreate(BaseModel):

    name: str

    price: float

    stock: int

    description: str

    category: str = ""

    image: str


class ProductUpdate(BaseModel):

    name: Optional[str] = None

    price: Optional[float] = None

    stock: Optional[int] = None

    description: Optional[str] = None

    category: Optional[str] = None

    image: Optional[str] = None