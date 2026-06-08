"""
Redis 缓存模块

提供：
- Redis 客户端生命周期管理
- FastAPI 依赖注入 get_cache()
- 商品相关缓存辅助函数
"""
import json
import logging
from typing import Optional, Any

import redis.asyncio as aioredis
from redis.asyncio import Redis

logger = logging.getLogger(__name__)

# ──────────────────────────────────────────────
# 全局 Redis 客户端
# ──────────────────────────────────────────────
_redis_client: Optional[Redis] = None

# 缓存过期时间（秒）
CACHE_TTL_SHORT = 60       # 商品列表（数据变化较快）
CACHE_TTL_MEDIUM = 300     # 商品详情（5 分钟）
CACHE_TTL_LONG = 600       # 分类列表（10 分钟，很少变化）


async def init_redis() -> None:
    """应用启动时调用，创建 Redis 连接池"""
    global _redis_client
    try:
        _redis_client = aioredis.from_url(
            "redis://localhost:6379",
            encoding="utf-8",
            decode_responses=True,
            max_connections=20,
        )
        await _redis_client.ping()
        logger.info("✅ Redis 连接成功")
    except Exception:
        logger.warning("⚠️ Redis 不可用，缓存功能将跳过（不影响核心业务）")
        _redis_client = None


async def close_redis() -> None:
    """应用关闭时调用，释放 Redis 连接"""
    global _redis_client
    if _redis_client:
        await _redis_client.close()
        _redis_client = None
        logger.info("Redis 连接已关闭")


async def get_cache() -> Optional[Redis]:
    """FastAPI 依赖注入：获取 Redis 客户端（可能为 None）"""
    return _redis_client


# ──────────────────────────────────────────────
# 辅助函数
# ──────────────────────────────────────────────

async def cache_get(cache: Optional[Redis], key: str) -> Optional[Any]:
    """从缓存获取 JSON 反序列化后的数据"""
    if cache is None:
        return None
    try:
        data = await cache.get(key)
        return json.loads(data) if data else None
    except Exception:
        return None


async def cache_set(
    cache: Optional[Redis], key: str, value: Any, ttl: int = CACHE_TTL_SHORT
) -> None:
    """将数据 JSON 序列化后写入缓存"""
    if cache is None:
        return
    try:
        await cache.setex(key, ttl, json.dumps(value, ensure_ascii=False))
    except Exception:
        pass


async def cache_delete(cache: Optional[Redis], key: str) -> None:
    """删除单个缓存键"""
    if cache is None:
        return
    try:
        await cache.delete(key)
    except Exception:
        pass


async def cache_delete_pattern(cache: Optional[Redis], pattern: str) -> None:
    """按模式批量删除缓存键（如 'products:*'）"""
    if cache is None:
        return
    try:
        cursor = 0
        while True:
            cursor, keys = await cache.scan(cursor, match=pattern, count=100)
            if keys:
                await cache.delete(*keys)
            if cursor == 0:
                break
    except Exception:
        pass
