# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.comment import Comment


class BaseCommentRepository(ABC):
    """Абстрактный репозиторий для работы с комментариями."""

    @abstractmethod
    async def add(self, data: Comment) -> str:
        """Добавление комментария в БД.

        Args:
            data (Comment): Комментарий

        Returns:
            str: ID нового комментария
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, id: UUID) -> Comment | None:
        """Получение конкретного комментария из БД.

        Args:
            id (UUID): ID комментария

        Returns:
            Comment | None: Комментарий или None
        """
        raise NotImplementedError

    @abstractmethod
    async def get_by_post(self, post_id: UUID) -> list[Comment]:
        """Получение всех комментариев к посту.

        Args:
            post_id (UUID): ID поста

        Returns:
            list[Comment]: Список всех комментариев к посту (включая вложенные)
        """
        raise NotImplementedError

    @abstractmethod
    async def update(self, id: UUID, data: Comment) -> Comment:
        """Обновление комментария в БД.

        Args:
            id (UUID): ID комментария
            data (Comment): Обновленные данные

        Returns:
            Comment: Обновленный комментарий
        """
        raise NotImplementedError

    @abstractmethod
    async def delete(self, id: UUID) -> bool:
        """Удаление комментария из БД.

        Args:
            id (UUID): ID комментария

        Returns:
            bool: True если удален успешно
        """
        raise NotImplementedError
