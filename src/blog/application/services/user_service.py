# -*- coding: utf-8 -*-

from email_validator import validate_email

from blog.domain.exceptions.user import UserNotFoundError, EmailSyntaxError
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

    async def create_user(self, data: User) -> User:
        """Создание пользователя.

        Args:
            data (dict): Данные для создания

        Returns:
            User: Созданный объект пользователя
        """
        await self._validate_email(data.email)

        user_id = await self._repo.add(data.__dict__)
        user = await self.get_user_by_id(str(user_id))
        return user

    async def update_user(self, user: User, update_data: User) -> User:
        """Обновление данных пользователя.

        Args:
            user (User): Объект пользователя
            update_data (dict): Данные для обновления

        Returns:
            User: Обновленный объект пользователя
        """
        from bson import ObjectId
        await self._validate_email(update_data.email)

        data = update_data.__dict__
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

    @staticmethod
    async def _validate_email(email: str) -> None:
        """Валидация email.

        Args:
            email (str): Email для валидации
        """
        try:
            validate_email(email)
        except Exception:
            raise EmailSyntaxError
