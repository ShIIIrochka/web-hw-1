# -*- coding: utf-8 -*-

from bson import ObjectId

from blog.domain.entities.post import Post
from blog.domain.entities.user import User
from blog.infra.repositories.abc_repo import BaseRepository


class PostService:
    """Сервис для работы с постами."""

    def __init__(self, repository: BaseRepository) -> None:
        """Конструктор.

        Args:
            repository (BaseRepository): Репозиторий для работы с БД
        """
        self._repo = repository

    async def get_post_by_id(self, post_id: str) -> Post:
        """Получение поста по ID.

        Args:
            post_id (str): ID поста

        Returns:
            Post: Объект поста

        Raises:
            ValueError: Если пост не найден.
        """

        post = await self._repo.get_one({"_id": ObjectId(post_id)})
        if post:
            return Post.from_raw(post)
        else:
            raise ValueError("Post not found")

    async def create_post(self, user: User, data: dict) -> Post:
        """Создание поста.

        Args:
            user (User): Автор поста
            data (dict): Данные для создания

        Returns:
            Post: Созданный объект поста
        """
        post_id = await self._repo.add(
            Post.create(user, data["title"], data["content"])
        )
        post = await self.get_post_by_id(str(post_id))
        return post

    async def update_post(self, user: User, post: Post, data: dict) -> Post:
        """Обновление данных поста.

        Args:
            post (Post): Объект поста
            data (dict): Данные для обновления

        Raises:
            PermissionError: Если пользователь не является автором поста

        Returns:
            Post: Обновленный объект поста
        """

        if user.id != post.author_id:
            raise PermissionError(
                "You do not have permission to update this post"
            )

        data.pop("id", None)
        data.pop("_id", None)

        await self._repo.update({"_id": ObjectId(post.id)}, {"$set": data})
        updated_post = await self.get_post_by_id(str(post.id))
        return updated_post

    async def delete_post(self, user: User, post: Post) -> bool:
        """Удаление поста.

        Args:
            post (Post): Объект поста

        Returns:
            bool: Статус удаления
        """

        if user.id != post.author_id:
            raise PermissionError(
                "You do not have permission to delete this post"
            )

        return await self._repo.delete({"_id": ObjectId(post.id)})
