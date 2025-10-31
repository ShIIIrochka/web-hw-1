# -*- coding: utf-8 -*-

from uuid import UUID

from litestar.dto import DTOData

from src.domain.entities.post import Post
from src.domain.entities.user import User
from src.domain.exceptions.category import CategoryNotFoundError
from src.domain.exceptions.post import PostNotFoundError, PostPermissionError
from src.domain.repositories.post_repository import BasePostRepository


class PostService:
    """Сервис для работы с постами."""

    def __init__(
        self,
        repository: BasePostRepository,
    ) -> None:
        """Конструктор.

        Args:
            repository (BaseRepository): Репозиторий для работы с постами
        """
        self._repo = repository

    async def get_post_by_id(self, post_id: UUID) -> Post:
        """Получение поста по ID.

        Args:
            post_id (str): ID поста

        Returns:
            Post: Объект поста

        Raises:
            ValueError: Если пост не найден.
        """

        try:
            post = await self._repo.get_by_id(post_id)
        except ValueError:
            raise PostNotFoundError
        if post:
            return post
        else:
            raise PostNotFoundError

    async def get_posts_by_author(self, author_id: UUID) -> list[Post]:
        """Получение постов пользователя.

        Args:
            author_id (UUID): ID пользователя

        Returns:
            list[Post]: Список постов пользователя
        """

        posts = await self._repo.get_many({"author_id": author_id})
        return posts

    async def create_post(self, user: User, data: DTOData[Post]) -> Post:
        """Создание поста.

        Args:
            user (User): Автор поста
            data (dict): Данные для создания

        Returns:
            Post: Созданный объект поста
        """

        built = data.as_builtins()
        title = built.get("title")
        content = built.get("content")
        category_ids = built.get("categories")

        post = Post.create(user.id, title, content, category_ids)

        try:
            await self._repo.add(post)
        except ValueError:
            raise CategoryNotFoundError

        return post

    async def update_post(
        self, user: User, post: Post, update_data: DTOData[Post]
    ) -> Post:
        """Обновление данных поста.

        Args:
            user (User): Автор поста
            post (Post): Объект поста
            update_data (dict): Данные для обновления

        Raises:
            PostPermissionError: Если пользователь не является автором поста

        Returns:
            Post: Обновленный объект поста
        """
        if user.id != post.author_id:
            raise PostPermissionError

        updated_post = post.update(
            title=update_data.as_builtins()["title"],
            content=update_data.as_builtins()["content"],
            categories=update_data.as_builtins().get("category_ids"),
        )
        await self._repo.update(post.id, updated_post)
        return updated_post

    async def delete_post(self, user: User, post: Post) -> bool:
        """Удаление поста.

        Args:
            user (User): Автор поста
            post (Post): Объект поста

        Returns:
            bool: Статус удаления
        """

        if user.id != post.author_id:
            raise PostPermissionError

        return await self._repo.delete(post.id)
