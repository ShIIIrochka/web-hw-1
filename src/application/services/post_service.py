# -*- coding: utf-8 -*-

from litestar.dto import DTOData

from src.domain.entities.post import Post
from src.domain.entities.user import User
from src.domain.exceptions.post import PostNotFoundError, PostPermissionError
from src.domain.repositories.post_repository import BasePostRepository
from uuid import UUID


class PostService:
    """Сервис для работы с постами."""

    def __init__(self, repository: BasePostRepository, category_service=None) -> None:
        """Конструктор.

        Args:
            repository (BaseRepository): Репозиторий для работы с БД
        """
        self._repo = repository
        # optional CategoryService for fetching categories by id
        self._category_service = category_service

    async def get_post_by_id(self, post_id: str) -> Post:
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
        category_ids = built.get("category_ids")

        post = Post.create(user, title, content)

        # attach categories if provided and category service is available
        if category_ids and self._category_service:
            categories = []
            for cid in category_ids:
                try:
                    cat = await self._category_service.get_category_by_id(cid)
                except ValueError:
                    # propagate as ValueError to caller to map to 404
                    raise
                categories.append(cat)
            post.categories = categories

        await self._repo.add(post)
        return post

    async def add_category_to_post(self, user: User, post: Post, category_id: str | UUID) -> Post:
        """Add a category to an existing post. Only author can modify their post."""
        if str(user.id) != str(post.author_id):
            raise PostPermissionError("You do not have permission to modify this post")

        if not self._category_service:
            raise ValueError("Category service not available")

        try:
            # ensure category_id is a string when calling the category service
            category = await self._category_service.get_category_by_id(str(category_id))
        except ValueError:
            raise

        if not post.categories:
            post.categories = [category]
        else:
            # avoid duplicates
            if not any(str(c.id) == str(category.id) for c in post.categories):
                post.categories.append(category)

        # repository methods expect string ids
        updated = await self._repo.update(str(post.id), post)
        return updated

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
            raise PermissionError(
                "You do not have permission to delete this post"
            )

        return await self._repo.delete(post.id)
