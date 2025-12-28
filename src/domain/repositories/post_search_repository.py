# -*- coding: utf-8 -*-

from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.post import Post


class BasePostSearchRepository(ABC):
    """Абстрактный репозиторий для поиска постов."""

    @abstractmethod
    async def search(
        self, query: str, limit: int = 10, offset: int = 0
    ) -> list[Post]:
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
    async def feed(
        self,
        liked_categories: list[UUID],
        saved_categories: list[UUID],
        limit: int = 10,
        cursor: UUID | None = None,
    ) -> list[Post]:
        """Персонализированный поиск постов - OpenSearch сам определяет релевантность.

        Args:
            liked_categories (list[UUID]): Список ID лайкнутых категорий
            saved_categories (list[UUID]): Список ID категорий из сохранённых постов
            limit (int): Количество результатов
            cursor (UUID | None): ID последнего поста для cursor пагинации

        Returns:
            list[Post]: Список постов, отсортированных по релевантности
        """
        raise NotImplementedError
