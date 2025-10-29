# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from domain.entities.user import User


class BaseUserRepository(ABC):
    """Базовый репозиторий для работы с пользователями."""

    @abstractmethod
    async def add(self, data: User) -> str:
        """Добавление нового пользователя.

        Args:
            data (dict): Данные пользователя.

        Returns:
            str: ID нового пользователя.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: str) -> User | None:
        """Получение пользователя по ID.

        Args:
            id (str): ID пользователя.

        Returns:
            dict | None: Данные пользователя или None, если не найден.
        """
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, query: dict) -> User | None:
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: str, data: User) -> User:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: str) -> bool:
        raise NotImplementedError
