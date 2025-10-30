# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

from src.domain.entities.user import User


class BaseUserRepository(ABC):
    """Базовый репозиторий для работы с пользователями."""

    @abstractmethod
    async def add(self, data: User) -> str:
        """Добавление нового пользователя.

        Args:
            data (dict): Данные пользователя

        Returns:
            str: ID нового пользователя
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: str) -> User | None:
        """Получение пользователя по ID.

        Args:
            id (str): ID пользователя

        Returns:
            dict | None: Данные пользователя или None, если не найден
        """
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, query: dict) -> User | None:
        """Получение одного пользователя по запросу.

        Args:
            query (dict): Запрос для поиска пользователя

        Returns:
            dict | None: Данные пользователя или None, если не найден
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: str, data: User) -> User:
        """Обновление пользователя.

        Args:
            id (str): ID пользователя
            data (User): Данные для обновления

        Returns:
            User: Обновленный пользователь
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: str) -> bool:
        """Удаление пользователя по ID.

        Args:
            id (str): ID пользователя

        Returns:
            bool: Статус удаления
        """
        raise NotImplementedError
