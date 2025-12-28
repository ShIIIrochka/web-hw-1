# -*- coding: utf-8 -*-

from uuid import UUID

from email_validator import validate_email
from litestar.dto import DTOData

from src.domain.entities.post import Post
from src.domain.entities.user import User
from src.domain.exceptions.user import EmailSyntaxError, UserNotFoundError
from src.domain.repositories.post_search_repository import (
    BasePostSearchRepository,
)
from src.domain.repositories.user_repository import BaseUserRepository
from src.domain.value_objects.cursor import Page


class UserService:
    """Сервис для работы с пользователем."""

    def __init__(
        self,
        repository: BaseUserRepository,
        search_repository: BasePostSearchRepository,
    ) -> None:
        """Конструктор.

        Args:
            repository (BaseRepository): Репозиторий для работы с БД
            search_repository (BaseSearchRepository): Репозиторий для поиска постов
        """
        self._repo = repository
        self._search_repo = search_repository

    async def get_user(self, data: DTOData[User]) -> User:
        """Получение пользователя по логину.

        Args:
            data (LoginUserDTO): Данные для логина

        Returns:
            User: Объект пользователя

        Raises:
            UserNotFoundError: Если пользователь не найден.
        """
        found_user = await self._repo.get_one(
            {
                "password": data.as_builtins()["password"],
                "email": data.as_builtins()["email"],
            }
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

    async def create_user(self, user: User) -> User:
        """Создание пользователя.

        Args:
            user (CreateUserDTO): Данные для создания пользователя

        Raises:
            EmailSyntaxError: Если email некорректен

        Returns:
            User: Созданный объект пользователя
        """
        await self._validate_email(user.email)

        user = User.create(
            email=user.email,
            login=user.login,
            password=user.password,
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

    async def delete_user(self, user_id: UUID) -> bool:
        """Удаление пользователя.

        Args:
            user_id (UUID): ID пользователя

        Returns:
            bool: Статус удаления
        """
        try:
            return await self._repo.delete(user_id)
        except ValueError:
            raise UserNotFoundError

    async def save_post(self, user_id: UUID, post_id: UUID) -> None:
        """Сохранение поста пользователем.

        Args:
            user_id (UUID): ID пользователя
            post_id (UUID): ID поста
        """
        await self._repo.save_post(user_id, post_id)

    async def unsave_post(self, user_id: UUID, post_id: UUID) -> None:
        """Удаление сохраненного поста пользователем.

        Args:
            user_id (UUID): ID пользователя
            post_id (UUID): ID поста
        """
        await self._repo.unsave_post(user_id, post_id)

    async def get_saved_posts(self, user_id: UUID) -> list[Post]:
        """Получение сохранённых постов пользователя.

        Args:
            user_id (UUID): ID пользователя

        Returns:
            list[User]: Список сохранённых постов
        """
        saved_posts = await self._repo.get_saved_posts(user_id)
        return saved_posts

    async def like_category(self, user_id: UUID, category_id: UUID) -> None:
        """Лайкнуть категорию пользователем.

        Args:
            user_id (UUID): ID пользователя
            category_id (UUID): ID категории
        """
        await self._repo.like_category(user_id, category_id)

    async def unlike_category(self, user_id: UUID, category_id: UUID) -> None:
        """Убрать лайк с категории пользователем.

        Args:
            user_id (UUID): ID пользователя
            category_id (UUID): ID категории
        """
        await self._repo.unlike_category(user_id, category_id)

    async def get_liked_categories(self, user_id: UUID) -> list[UUID]:
        """Получение списка лайкнутых категорий пользователя.

        Args:
            user_id (UUID): ID пользователя

        Returns:
            list[UUID]: Список ID лайкнутых категорий
        """
        return await self._repo.get_liked_categories(user_id)

    async def get_feed(
        self, user_id: UUID, cursor: UUID | None = None, limit: int = 10
    ) -> Page:
        """Получение персонализированной ленты для пользователя через OpenSearch.

        Args:
            user_id (UUID): ID пользователя
            cursor (UUID | None): Курсор для пагинации
            limit (int): Количество постов на странице

        Returns:
            Page: Страница с персонализированными постами
        """
        liked_categories = await self._repo.get_liked_categories(user_id)
        posts = await self._search_repo.feed(
            liked_categories=liked_categories,
            limit=limit + 1,
            cursor=cursor,
        )

        has_more = len(posts) > limit
        next_cursor = None
        if has_more:
            posts = posts[:limit]
            next_cursor = posts[-1].id if posts else None

        return Page(
            items=posts,
            next_cursor=next_cursor,
            has_more=has_more,
        )

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
