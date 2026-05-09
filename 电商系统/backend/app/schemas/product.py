from pydantic import BaseModel


class ProductCreate(BaseModel):

    name: str

    price: float

    stock: int

    description: str

    image: str