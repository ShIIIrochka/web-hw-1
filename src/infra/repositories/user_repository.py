# -*- coding: utf-8 -*-

from dataclasses import asdict
from uuid import UUID

from tortoise.exceptions import DoesNotExist

from src.domain.entities.post import Post
from src.domain.entities.user import User
from src.domain.repositories.user_repository import BaseUserRepository
from src.infra.models.category import Category as CategoryModel
from src.infra.models.post import Post as PostModel
from src.infra.models.user import User as UserModel


class UserRepository(BaseUserRepository):
    """Реализация репозитория для работы с пользователями."""

    def __init__(
        self,
        model: type[UserModel] = UserModel,
        post_model: type[PostModel] = PostModel,
        category_model: type[CategoryModel] = CategoryModel,
    ) -> None:
        """Конструктор.

        Args:
            model (type[UserModel]): ORM модель
            post_model (type[PostModel]): ORM модель поста
            category_model (type[CategoryModel]): ORM модель категории
        """
        self._model = model
        self._post_model = post_model
        self._category_model = category_model

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

    async def save_post(self, user_id: UUID, post_id: UUID) -> None:
        """Сохранение поста пользователем."""
        user = await self._model.get(id=user_id)
        post = await self._post_model.get(id=post_id)
        await user.saved_posts.add(post)

    async def unsave_post(self, user_id: UUID, post_id: UUID) -> None:
        """Удаление сохраненного поста пользователем."""
        user = await self._model.get(id=user_id)
        post = await self._post_model.get(id=post_id)
        await user.saved_posts.remove(post)

    async def get_saved_posts(self, user_id: UUID) -> list[Post]:
        """Получение сохранённых постов пользователя.

        Args:
            user_id (UUID): ID пользователя

        Returns:
            list[User]: Список сохранённых постов
        """
        posts = await self._post_model.filter(saved_by__id=user_id).all()
        return [await post.to_entity() for post in posts]

    async def like_category(self, user_id: UUID, category_id: UUID) -> None:
        """Лайкнуть категорию пользователем.

        Args:
            user_id (UUID): ID пользователя
            category_id (UUID): ID категории
        """

        user = await self._model.get(id=user_id)
        category = await self._category_model.get(id=category_id)
        await user.liked_categories.add(category)

    async def unlike_category(self, user_id: UUID, category_id: UUID) -> None:
        """Убрать лайк с категории пользователем.

        Args:
            user_id (UUID): ID пользователя
            category_id (UUID): ID категории
        """

        user = await self._model.get(id=user_id)
        category = await self._category_model.get(id=category_id)
        await user.liked_categories.remove(category)

    async def get_liked_categories(self, user_id: UUID) -> list[UUID]:
        """Получение списка лайкнутых категорий пользователя.

        Args:
            user_id (UUID): ID пользователя

        Returns:
            list[UUID]: Список ID лайкнутых категорий
        """
        categories = await self._category_model.filter(
            liked_by__id=user_id
        ).all()
        return [category.id for category in categories]

    async def follow_user(self, follower_id: UUID, following_id: UUID) -> None:
        """Подписаться на пользователя.

        Args:
            follower_id (UUID): ID подписчика
            following_id (UUID): ID пользователя, на которого подписываются
        """
        follower = await self._model.get(id=follower_id)
        following = await self._model.get(id=following_id)
        await follower.following.add(following)

    async def unfollow_user(
        self, follower_id: UUID, following_id: UUID
    ) -> None:
        """Отписаться от пользователя.

        Args:
            follower_id (UUID): ID подписчика
            following_id (UUID): ID пользователя, от которого отписываются
        """
        follower = await self._model.get(id=follower_id)
        following = await self._model.get(id=following_id)
        await follower.following.remove(following)

    async def get_following_ids(self, user_id: UUID) -> list[UUID]:
        """Получение списка ID пользователей, на которых подписан пользователь.

        Args:
            user_id (UUID): ID пользователя

        Returns:
            list[UUID]: Список ID пользователей
        """
        user = await self._model.get(id=user_id)
        await user.fetch_related("following")
        return [following_user.id for following_user in user.following]
