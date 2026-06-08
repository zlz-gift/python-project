from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI 依赖注入：为每个请求提供一个异步数据库会话"""
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
