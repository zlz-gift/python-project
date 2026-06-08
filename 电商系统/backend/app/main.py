from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import engine, Base
from app.core.cache import init_redis, close_redis

# ── 显式导入所有模型，确保 metadata 注册 ──
from app.models.user import User       # noqa: F401
from app.models.product import Product  # noqa: F401
from app.models.cart import Cart        # noqa: F401
from app.models.order import Order      # noqa: F401

from app.api.user import router as user_router
from app.api.product import router as product_router
from app.api.cart import router as cart_router
from app.api.order import router as order_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # ── 启动时 ──
    # 创建数据库表（异步）
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # 初始化 Redis
    await init_redis()
    yield
    # ── 关闭时 ──
    await close_redis()
    await engine.dispose()


app = FastAPI(
    title="电商系统 API",
    description="基于 FastAPI 的全栈电商系统（异步 + Redis 缓存）",
    version="2.0.0",
    lifespan=lifespan,
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(user_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(order_router, prefix="/order", tags=["订单"])


@app.get("/")
async def root():
    return {"msg": "hello shop", "version": "2.0.0 (async + redis)"}
