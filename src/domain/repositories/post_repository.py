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
