# -*- coding: utf-8 -*-

from __future__ import annotations

from src.domain.entities.post import Post
from src.domain.repositories.post_search_repository import (
    BasePostSearchRepository,
)


class PostSearchService:
    """Сервис для поиска постов через OpenSearch."""

    def __init__(
        self,
        search_repository: BasePostSearchRepository,
    ) -> None:
        """Конструктор.

        Args:
            search_repository: Репозиторий поиска
        """
        self._search_repo = search_repository

    async def search_posts(
        self, query: str, limit: int = 10, offset: int = 0
    ) -> list[Post]:
        """Поиск постов по запросу.

        Args:
            query: Поисковый запрос
            limit: Количество результатов
            offset: Смещение

        Returns:
            PostSearchResult с типизированными результатами
        """
        return await self._search_repo.search(query, limit, offset)
