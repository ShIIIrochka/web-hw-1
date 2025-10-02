# -*- coding: utf-8 -*-
from email_validator import validate_email

from blog.domain.exceptions.user import UserNotFoundError
from blog.domain.entities.user import User
from blog.domain.repositories.abc_repo import BaseRepository


class UserService:
    """Сервис для работы с пользователем."""

    def __init__(
        self,
        repository: BaseRepository,
    ) -> None:
        """Конструктор.

        Args:
            repository (BaseRepository): Репозиторий для работы с БД
        """
        self._repo = repository

    async def get_user_by_id(self, user_id: str) -> User:
        """Получение пользователя по ID.

        Args:
            user_id (str): ID пользователя

        Returns:
            User: Объект пользователя

        Raises:
            UserNotFoundError: Если пользователь не найден.
        """
        from bson import ObjectId

        user = await self._repo.get_one({"_id": ObjectId(user_id)})
        if user:
            return User.from_raw(user)
        else:
            raise UserNotFoundError

    async def create_user(self, data: dict) -> User:
        """Создание пользователя.

        Args:
            data (dict): Данные для создания

        Returns:
            User: Созданный объект пользователя
        """
        try:
            validate_email(data["email"])
        except Exception:
            raise ValueError

        user_id = await self._repo.add(data)
        user = await self.get_user_by_id(str(user_id))
        return user

    async def update_user(self, user: User, data: dict) -> User:
        """Обновление данных пользователя.

        Args:
            user (User): Объект пользователя
            data (dict): Данные для обновления

        Returns:
            User: Обновленный объект пользователя
        """
        from bson import ObjectId

        data.pop("_id", None)

        await self._repo.update({"_id": ObjectId(user.id)}, {"$set": data})
        updated_user = await self.get_user_by_id(str(user.id))
        return updated_user

    async def delete_user(self, user: User) -> bool:
        """Удаление пользователя.

        Args:
            user (User): Объект пользователя

        Returns:
            bool: Статус удаления
        """
        from bson import ObjectId

        return await self._repo.delete({"_id": ObjectId(user.id)})
