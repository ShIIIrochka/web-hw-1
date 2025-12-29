# -*- coding: utf-8 -*-

from __future__ import annotations

import json

from src.domain.entities.post import Post
from src.domain.repositories.post_search_repository import (
    BasePostSearchRepository,
)
from src.infra.providers.interfaces import CacheProvider


class PostSearchService:
    """Сервис для поиска постов через OpenSearch."""

    def __init__(
        self,
        search_repository: BasePostSearchRepository,
        cache_provider: CacheProvider,
        popularity_threshold: int = 10,
        cache_ttl: int = 300,
    ) -> None:
        """Конструктор.

        Args:
            search_repository: Репозиторий поиска
            cache_provider: Провайдер кеширования
            popularity_threshold: Порог популярности запроса для кеширования
            cache_ttl: TTL для кеша результатов поиска (в секундах)
        """
        self._search_repo = search_repository
        self._cache = cache_provider
        self._popularity_threshold = popularity_threshold
        self._cache_ttl = cache_ttl

    async def search_posts(
        self, query: str, limit: int = 10, offset: int = 0
    ) -> list[Post]:
        """Поиск постов по запросу с кешированием популярных запросов.

        Args:
            query (str): Поисковый запрос
            limit (int): Количество результатов
            offset (int): Смещение

        Returns:
            list[Posts]: Список постов, соответствующих запросу
        """
        normalized_query = self._normalize_query(query)
        cache_key = self._get_cache_key(normalized_query, limit, offset)
        count_key = self._get_count_key(normalized_query)

        cached_result = await self._cache.get(cache_key)
        if cached_result:
            posts_data = json.loads(cached_result)
            return [Post.from_row(post_data) for post_data in posts_data]

        query_count = await self._cache.incr(count_key)

        if query_count == 1:
            await self._cache.set(
                count_key, str(query_count), ttl=7 * 24 * 60 * 60
            )

        posts = await self._search_repo.search(query, limit, offset)

        if query_count >= self._popularity_threshold:
            posts_data = [post.to_row() for post in posts]
            await self._cache.set(
                cache_key, json.dumps(posts_data), ttl=self._cache_ttl
            )

        return posts

    @staticmethod
    def _normalize_query(query: str) -> str:
        """Нормализация поискового запроса.

        Args:
            query: Исходный поисковый запрос

        Returns:
            Нормализованный запрос
        """
        return query.lower().strip()

    @staticmethod
    def _get_cache_key(query: str, limit: int, offset: int) -> str:
        """Формирование ключа кеша.

        Args:
            query: Нормализованный поисковый запрос
            limit: Количество результатов
            offset: Смещение

        Returns:
            Ключ для кеширования
        """
        return f"search:query:{query}:limit:{limit}:offset:{offset}"

    @staticmethod
    def _get_count_key(query: str) -> str:
        """Формирование ключа счетчика запросов.

        Args:
            query: Нормализованный поисковый запрос

        Returns:
            Ключ для счетчика
        """
        return f"search:count:{query}"
