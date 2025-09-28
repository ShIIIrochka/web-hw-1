# -*- coding: utf-8 -*-

import base64

from email_validator import validate_email
from email_validator.exceptions import EmailNotValidError
from jam.aio import Jam

from blog.application.exceptions.user import UserNotFoundError
from blog.domain.entities import User
from blog.infra.repositories.abc_repo import BaseRepository


class UserService:
    """Сервис для работы с пользователем."""

    def __init__(
        self,
        repository: BaseRepository,
        jam: Jam,
        debug: bool,
    ) -> None:
        """Конструктор.

        Args:
            repository (BaseRepository): Репозиторий для работы с БД
            jam (Jam): Инстанс Jam
            debug (bool): Режим работы приложения
        """
        self._repo = repository
        self._jam = jam
        self.debug = debug

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

    async def update_user(self, user: User, data: dict) -> User:
        """Обновление данных пользователя.

        Args:
            user (User): Объект пользователя
            data (dict): Данные для обновления

        Returns:
            User: Обновленный объект пользователя
        """
        from bson import ObjectId

        await self._repo.update({"_id": ObjectId(user.id)}, {"$set": data})
        updated_user = await self.get_user_by_id(str(user.id))
        return updated_user