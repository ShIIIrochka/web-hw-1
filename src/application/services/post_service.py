# -*- coding: utf-8 -*-

from __future__ import annotations

from uuid import UUID

from litestar.dto import DTOData

from src.domain.entities.post import Post
from src.domain.entities.user import User
from src.domain.exceptions.category import CategoryNotFoundError
from src.domain.exceptions.post import PostNotFoundError, PostPermissionError
from src.domain.repositories.post_repository import BasePostRepository
from src.domain.repositories.post_search_repository import (
    BasePostSearchRepository,
)
from src.domain.repositories.user_repository import BaseUserRepository
from src.domain.value_objects.cursor import Page
from src.infra.providers.interfaces import CacheProvider


class PostService:
    """Сервис для работы с постами."""

    def __init__(
        self,
        repository: BasePostRepository,
        search_repository: BasePostSearchRepository,
        cache_provider: CacheProvider,
        user_repository: BaseUserRepository,
    ) -> None:
        """Конструктор.

        Args:
            repository (BasePostRepository): Репозиторий для работы с постами
            search_repository (BasePostSearchRepository): Репозиторий для поиска и индексации постов
            cache_provider (CacheProvider): Провайдер кеширования
            user_repository (BaseUserRepository): Репозиторий для работы с пользователями
        """
        self._repo = repository
        self._search_repo = search_repository
        self._cache = cache_provider
        self._user_repo = user_repository

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
        await self._search_repo.index(post)

        await self._cache.delete_pattern("search:query:*")

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
            categories=update_data.as_builtins().get("categories"),
        )
        await self._repo.update(post.id, updated_post)

        await self._search_repo.update(updated_post)

        await self._cache.delete_pattern("search:query:*")

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

        result = await self._repo.delete(post.id)

        await self._search_repo.delete(post.id)

        await self._cache.delete_pattern("search:query:*")

        return result

    async def get_posts_paginated(
        self, cursor: UUID | None, limit: int = 10
    ) -> Page:
        """Получение постов с cursor-offset пагинацией.

        Args:
            cursor (UUID | None): Курсор для пагинации
            limit (int): Количество постов на странице

        Returns:
            Page с постами и next_cursor
        """

        posts = await self._repo.get_paginated(
            cursor_id=cursor,
            limit=limit + 1,
        )

        has_more = len(posts) > limit
        next_cursor = None
        if has_more:
            posts = posts[:limit]
            next_cursor = posts[-1].id

        return Page(
            items=posts,
            next_cursor=next_cursor,
            has_more=has_more,
        )

    async def get_feed_posts(
        self, user: User, cursor: UUID | None, limit: int = 10
    ) -> Page:
        """Получение ленты постов от подписанных авторов с cursor-offset пагинацией.

        Args:
            user (User): Текущий пользователь
            cursor (UUID | None): Курсор для пагинации
            limit (int): Количество постов на странице

        Returns:
            Page с постами и next_cursor
        """
        following_ids = await self._user_repo.get_following_ids(user.id)

        if not following_ids:
            return Page(
                items=[],
                next_cursor=None,
                has_more=False,
            )

        posts = await self._repo.get_posts_by_authors(
            author_ids=following_ids,
            cursor_id=cursor,
            limit=limit + 1,
        )

        has_more = len(posts) > limit
        next_cursor = None
        if has_more:
            posts = posts[:limit]
            next_cursor = posts[-1].id

        return Page(
            items=posts,
            next_cursor=next_cursor,
            has_more=has_more,
        )
