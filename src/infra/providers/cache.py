# -*- coding: utf-8 -*-

from __future__ import annotations

from redis.asyncio import Redis, from_url

from src.infra.providers.interfaces import CacheProvider


class RedisCacheProvider(CacheProvider):
    """Провайдер кэша на основе Redis."""

    def __init__(self, uri: str, default_ttl: int = 60) -> None:
        """Инициализация провайдера.

        Args:
            uri: URI подключения к Redis
            default_ttl: TTL по умолчанию в секундах
        """
        self._uri = uri
        self.default_ttl = default_ttl
        self._client: Redis | None = None

    async def init(self) -> None:
        """Инициализация подключения к Redis."""
        self._client = from_url(self._uri, decode_responses=True)

    async def close(self) -> None:
        """Закрытие подключения к Redis."""
        if self._client:
            await self._client.aclose()

    async def get(self, key: str) -> str | None:
        """Получение значения из кэша."""
        if not self._client:
            raise RuntimeError("Redis client not initialized")
        return await self._client.get(key)

    async def set(self, key: str, value: str, ttl: int | None = None) -> None:
        """Сохранение значения в кэш."""
        if not self._client:
            raise RuntimeError("Redis client not initialized")
        await self._client.set(key, value, ex=ttl or self.default_ttl)

    async def delete(self, key: str) -> None:
        """Удаление значения из кэша."""
        if not self._client:
            raise RuntimeError("Redis client not initialized")
        await self._client.delete(key)

    async def incr(self, key: str) -> int:
        """Инкремент значения."""
        if not self._client:
            raise RuntimeError("Redis client not initialized")
        return await self._client.incr(key)

    async def get_version(self, prefix: str) -> int:
        """Получение текущей версии кэша для префикса."""
        version_key = f"{prefix}:cache_version"
        version = await self.get(version_key)
        if version is None:
            await self.set(version_key, "1", ttl=None)
            return 1
        return int(version)
