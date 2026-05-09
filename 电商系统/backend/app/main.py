from fastapi import FastAPI
from app.db.database import engine, Base
from app.models.user import User
from app.api.user import router as user_router
from app.models.product import Product
from app.api.product import router as product_router
from fastapi.middleware.cors import CORSMiddleware
from app.models.cart import Cart
from app.api.cart import router as cart_router
from app.api.order import router as order_router
from app.models.order import Order
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(cart_router)
Base.metadata.create_all(bind=engine)
app.include_router(order_router, prefix="/order", tags=["订单"])
app.include_router(user_router)
app.include_router(product_router)

@app.get("/")
def root():
    return {"msg": "hello shop"}