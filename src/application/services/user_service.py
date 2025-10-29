# -*- coding: utf-8 -*-

from email_validator import validate_email
from litestar.dto import DTOData

from domain.repositories.user_repository import BaseUserRepository
from src.api.dto.users import CreateUserDTO
from src.domain.entities.user import User
from src.domain.exceptions.user import EmailSyntaxError, UserNotFoundError


class UserService:
    """Сервис для работы с пользователем."""

    def __init__(
        self,
        repository: BaseUserRepository,
    ) -> None:
        """Конструктор.

        Args:
            repository (BaseRepository): Репозиторий для работы с БД
        """
        self._repo = repository

    async def get_user(self, password: str, email: str) -> User:
        """Получение пользователя по логину.

        Args:
            user (LoginUserDTO): Данные для логина

        Returns:
            User: Объект пользователя

        Raises:
            UserNotFoundError: Если пользователь не найден.
        """
        found_user = await self._repo.get_one(
            {"password": password, "email": email}
        )
        if found_user:
            return found_user
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
        try:
            user = await self._repo.get_by_id(user_id)
        except ValueError:
            raise UserNotFoundError
        if user:
            return user
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
        await self._repo.add(user)
        return user

    async def update_user(self, user: User, update_data: DTOData[User]) -> User:
        """Обновление данных пользователя.

        Args:
            user (User): Объект пользователя
            update_data (DTOData[User]): Данные для обновления

        Raises:
            EmailSyntaxError: Если email некорректен

        Returns:
            User: Обновленный объект пользователя
        """

        email: str = update_data.as_builtins()["email"]
        login: str = update_data.as_builtins()["login"]
        await self._validate_email(email)

        updated_user: User = user.update(
            email=email,
            login=login,
        )
        try:
            await self._repo.update(updated_user.id, updated_user)
        except ValueError:
            raise UserNotFoundError
        return user

    async def delete_user(self, user_id: str) -> bool:
        """Удаление пользователя.

        Args:
            user_id (str): ID пользователя

        Returns:
            bool: Статус удаления
        """
        try:
            return await self._repo.delete(user_id)
        except ValueError:
            raise UserNotFoundError

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
