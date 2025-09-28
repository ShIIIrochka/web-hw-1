# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any

from blog.infra.gateways.interfaces import DBGateway


class BaseRepository(ABC):
    """Базовый репозиторий для работы с БД."""

    def __init__(self, gateway: DBGateway) -> None:
        """Конструктор.

        Args:
            gateway (DBGateway): Гейт к бд.
        """
        self.__gw = gateway

    @abstractmethod
    async def add(self, data: dict[str, Any]) -> Any:
        """Добавление нового документа/таблицы.

        Returns:
            Any: ID нового объекта
        """
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, query: dict[str, Any]) -> dict[str, Any]:
        """Получение одного объекта."""
        raise NotImplementedError

    @abstractmethod
    async def get_many(
        self, query: dict[str, Any], limit: int
    ) -> list[dict[str, Any]]:
        """Получение нескольких объектов."""
        raise NotImplementedError

    @abstractmethod
    async def update(
        self, query: dict[str, Any], update_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Обновление объекта."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, query: dict[str, Any]) -> bool:
        """Удаление объекта."""
        raise NotImplementedError
