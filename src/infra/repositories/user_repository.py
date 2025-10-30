# -*- coding: utf-8 -*-

from dataclasses import asdict
from uuid import UUID

from tortoise.exceptions import DoesNotExist

from src.domain.entities.user import User
from src.domain.repositories.user_repository import BaseUserRepository
from src.infra.models import User as UserModel


class UserRepository(BaseUserRepository):
    """Реализация репозитория для работы с пользователями."""

    def __init__(self, model: type[UserModel] = UserModel) -> None:
        """Конструктор.

        Args:
            model (str): ORM модель
        """
        self._model = model

    async def add(self, data: User) -> str:
        """Добавление нового пользователя."""
        user_dict = asdict(data)
        user_dict.pop("id", None)
        user_dict.pop("posts", None)
        user_dict.pop("saved_posts", None)
        result = await self._model.create(**user_dict)
        return str(result.id)

    async def get_by_id(self, id: str) -> User | None:
        """Получение пользователя по ID."""
        try:
            user = await self._model.get(id=UUID(id))
            return await user.to_entity(include_posts=True)
        except DoesNotExist:
            return None

    async def get_one(self, query: dict) -> User | None:
        """Получение одного пользователя по запросу."""
        user = await self._model.filter(**query).first()
        if not user:
            return None
        return await user.to_entity(include_posts=True)

    async def update(self, user_id: str, data: User) -> User:
        """Обновление пользователя."""
        update_data = asdict(data)
        update_data.pop("id", None)
        update_data.pop("posts", None)
        update_data.pop("saved_posts", None)

        await self._model.filter(id=UUID(user_id)).update(**update_data)
        updated = await self._model.get_or_none(id=user_id)
        return await updated.to_entity(include_posts=True) if updated else data

    async def delete(self, id: str) -> bool:
        """Удаление пользователя по ID."""
        deleted_count = await self._model.filter(id=UUID(id)).delete()
        return deleted_count > 0
