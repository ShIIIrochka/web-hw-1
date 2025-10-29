# -*- coding: utf-8 -*-
from dataclasses import asdict

from bson.errors import InvalidId
from email_validator import validate_email

from api.dto.users import LoginUserDTO
from src.api.dto.users import CreateUserDTO
from src.domain.entities.user import User
from src.domain.exceptions.user import EmailSyntaxError, UserNotFoundError
from src.domain.repositories.abc_repo import BaseRepository


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

    async def get_user(self, user: LoginUserDTO) -> User:
        """Получение пользователя по логину.

        Args:
            user (LoginUserDTO): Данные для логина

        Returns:
            User: Объект пользователя

        Raises:
            UserNotFoundError: Если пользователь не найден.
        """
        found_user = await self._repo.get_one(
            {"password": user.password, "email": user.email}
        )
        if found_user:
            return User.from_raw(found_user)
        else:
            raise UserNotFoundError

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

        try:
            user = await self._repo.get_one({"_id": ObjectId(user_id)})
        except InvalidId:
            raise UserNotFoundError
        if user:
            return User.from_raw(user)
        else:
            raise UserNotFoundError

    async def create_user(self, user: CreateUserDTO) -> User:
        """Создание пользователя.

        Args:
            user (CreateUserDTO): Данные для создания пользователя

        Raises:
            EmailSyntaxError: Если email некорректен

        Returns:
            User: Созданный объект пользователя
        """
        await self._validate_email(user.email)  # type: ignore

        user = User.create(
            email=user.email,  # type: ignore
            login=user.login,  # type: ignore
            password=user.password,  # type: ignore
        )
        await self._repo.add(user.__dict__)
        return user

    async def update_user(self, user: User, email: str, login: str) -> User:
        """Обновление данных пользователя.

        Args:
            user (User): Объект пользователя
            email (str): Новый email
            login (str): Новый логин

        Raises:
            EmailSyntaxError: Если email некорректен

        Returns:
            User: Обновленный объект пользователя
        """
        from bson import ObjectId

        await self._validate_email(email)

        updated_user: User = user.update(
            email=email,
            login=login,
        )
        data = asdict(updated_user)
        data.pop("_id", None)

        await self._repo.update(
            {"_id": ObjectId(updated_user.id)}, {"$set": data}
        )
        return user

    async def delete_user(self, user_id: str) -> bool:
        """Удаление пользователя.

        Args:
            user_id (str): ID пользователя

        Returns:
            bool: Статус удаления
        """
        from bson import ObjectId

        return await self._repo.delete({"_id": ObjectId(user_id)})

    @staticmethod
    async def _validate_email(email: str) -> None:
        """Валидация email.

        Args:
            email (str): Email для валидации
        """
        try:
            validate_email(email, strict=False)
        except Exception:
            raise EmailSyntaxError
