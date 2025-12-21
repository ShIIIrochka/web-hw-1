# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.post import Post
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
    async def update(self, id: UUID, data: User) -> User:
        """Обновление пользователя.

        Args:
            id (UUID): ID пользователя
            data (User): Данные для обновления

        Returns:
            User: Обновленный пользователь
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """Удаление пользователя по ID.

        Args:
            id (UUID): ID пользователя

        Returns:
            bool: Статус удаления
        """
        raise NotImplementedError

    @abstractmethod
    async def save_post(self, user_id: UUID, post_id: UUID) -> None:
        """Сохранение поста пользователем.

        Args:
            user_id (UUID): ID пользователя
            post_id (UUID): ID поста
        """
        raise NotImplementedError

    @abstractmethod
    async def unsave_post(self, user_id: UUID, post_id: UUID) -> None:
        """Удаление сохраненного поста пользователем.

        Args:
            user_id (UUID): ID пользователя
            post_id (UUID): ID поста
        """
        raise NotImplementedError

    @abstractmethod
    async def get_saved_posts(self, user_id: UUID) -> list[Post]:
        """Получение сохранённых постов пользователя.

        Args:
            user_id (UUID): ID пользователя

        Returns:
            list[User]: Список сохранённых постов
        """
        raise NotImplementedError
