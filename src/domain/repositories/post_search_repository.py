# -*- coding: utf-8 -*-

from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.post import Post
from src.domain.value_objects.search import PostSearchResult


class BasePostSearchRepository(ABC):
    """Абстрактный репозиторий для поиска постов."""

    @abstractmethod
    async def search(
        self, query: str, limit: int = 10, offset: int = 0
    ) -> PostSearchResult:
        """Поиск постов по запросу.

        Args:
            query: Поисковый запрос
            limit: Количество результатов
            offset: Смещение для пагинации

        Returns:
            PostSearchResult с результатами поиска
        """
        raise NotImplementedError

    @abstractmethod
    async def index(self, post: Post) -> None:
        """Индексация поста.

        Args:
            post: Сущность поста для индексации
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, post: Post) -> None:
        """Обновление поста в индексе.

        Args:
            post: Сущность поста для обновления
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, post_id: UUID) -> None:
        """Удаление поста из индекса.

        Args:
            post_id: Идентификатор поста
        """
        raise NotImplementedError

    @abstractmethod
    async def bulk_index(self, posts: list[Post]) -> None:
        """Массовая индексация постов.

        Args:
            posts: Список постов для индексации
        """
        raise NotImplementedError
