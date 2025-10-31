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
        result = await self._model.create(**user_dict)
        return str(result.id)

    async def get_by_id(self, id: str) -> User | None:
        """Получение пользователя по ID."""
        try:
            user = await self._model.get(id=UUID(id))
            return await user.to_entity()
        except DoesNotExist:
            return None

    async def get_one(self, query: dict) -> User | None:
        """Получение одного пользователя по запросу."""
        user = await self._model.filter(**query).first()
        if not user:
            return None
        return await user.to_entity()

    async def update(self, user_id: UUID, data: User) -> User:
        """Обновление пользователя."""
        update_data = asdict(data)
        update_data.pop("id", None)

        await self._model.filter(id=user_id).update(**update_data)
        updated = await self._model.get_or_none(id=user_id)
        return await updated.to_entity() if updated else data

    async def delete(self, id: UUID) -> bool:
        """Удаление пользователя по ID."""
        deleted_count = await self._model.filter(id=id).delete()
        return deleted_count > 0
