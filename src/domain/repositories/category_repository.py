# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from src.domain.entities.category import Category


class BaseCategoryRepository(ABC):
    """Базовый репозиторий для работы с категориями."""

    @abstractmethod
    async def add(self, data: Category) -> str:
        """Добавление нового документа/таблицы.

        Returns:
            Any: ID нового объекта
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: str) -> Category | None:
        """Получение одного объекта."""
        raise NotImplementedError

    @abstractmethod
    async def get_many(self, cursor: str | None, limit: int) -> list[Category]:
        """Получение нескольких объектов."""
        raise NotImplementedError
