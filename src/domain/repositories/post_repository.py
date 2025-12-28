# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.post import Post


class BasePostRepository(ABC):
    """Абстрактный репозиторий для работы с постами."""

    @abstractmethod
    async def add(self, data: Post) -> str:
        """Добавление документа в БД.

        Args:
            data (dict[str, Any]): Документ

        Returns:
            Any: ID нового документа
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Post | None:
        """Получение конкретного объекта из БД."""
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: UUID, data: Post) -> Post:
        """Обновление документа в БД."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """Удаление документа из БД."""
        raise NotImplementedError

    @abstractmethod
    async def get_many(
        self, query: dict, cursor: UUID | None = None, limit: int = 10
    ) -> list[Post]:
        """Получение N объектов из БД."""
        raise NotImplementedError

    @abstractmethod
    async def get_paginated(
        self, cursor_id: UUID | None, limit: int
    ) -> list[Post]:
        """Получение объектов с пагинацией."""
        raise NotImplementedError

    @abstractmethod
    async def get_posts_by_authors(
        self, author_ids: list[UUID], cursor_id: UUID | None, limit: int
    ) -> list[Post]:
        """Получение постов по списку авторов с пагинацией.

        Args:
            author_ids (list[UUID]): Список ID авторов
            cursor_id (UUID | None): ID курсора для пагинации
            limit (int): Количество постов

        Returns:
            list[Post]: Список постов
        """
        raise NotImplementedError
