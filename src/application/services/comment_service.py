# -*- coding: utf-8 -*-

from __future__ import annotations

from uuid import UUID

from litestar.dto import DTOData

from src.domain.entities.comment import Comment
from src.domain.entities.post import Post
from src.domain.entities.user import User
from src.domain.exceptions.comment import (
    CommentNotFoundError,
    CommentPermissionError,
)
from src.domain.exceptions.post import PostNotFoundError
from src.domain.repositories.comment_repository import BaseCommentRepository
from src.domain.repositories.post_repository import BasePostRepository


class CommentService:
    """Сервис для работы с комментариями."""

    def __init__(
        self,
        comment_repository: BaseCommentRepository,
        post_repository: BasePostRepository,
    ) -> None:
        """Конструктор.

        Args:
            comment_repository (BaseCommentRepository): Репозиторий для работы с комментариями
            post_repository (BasePostRepository): Репозиторий для работы с постами
        """
        self._comment_repo = comment_repository
        self._post_repo = post_repository

    async def get_comment_by_id(self, comment_id: UUID) -> Comment:
        """Получение комментария по ID.

        Args:
            comment_id (UUID): ID комментария

        Returns:
            Comment: Объект комментария

        Raises:
            CommentNotFoundError: Если комментарий не найден
        """
        comment = await self._comment_repo.get_by_id(comment_id)
        if not comment:
            raise CommentNotFoundError
        return comment

    async def get_comments_by_post(self, post: Post) -> list[Comment]:
        """Получение всех комментариев к посту.

        Args:
            post (post): Пост

        Returns:
            list[Comment]: Список комментариев

        Raises:
            PostNotFoundError: Если пост не найден
        """
        if not post:
            raise PostNotFoundError

        comments = await self._comment_repo.get_by_post(post.id)
        return comments

    async def create_comment(
        self,
        user: User,
        post_id: UUID,
        data: DTOData[Comment],
        parent_comment_id: UUID | None = None,
    ) -> Comment:
        """Создание комментария.

        Args:
            user (User): Автор комментария
            post_id (UUID): ID поста
            data (DTOData[Comment]): Данные для создания
            parent_comment_id (UUID | None): ID родительского комментария (для ответов)

        Returns:
            Comment: Созданный комментарий

        Raises:
            PostNotFoundError: Если пост не найден
            CommentNotFoundError: Если родительский комментарий не найден
        """
        post = await self._post_repo.get_by_id(post_id)
        if not post:
            raise PostNotFoundError

        built = data.as_builtins()
        content = built.get("content")

        if parent_comment_id:
            parent_comment = await self._comment_repo.get_by_id(
                parent_comment_id
            )
            if not parent_comment:
                raise CommentNotFoundError

        comment = Comment.create(
            content=content,
            post_id=post_id,
            author_id=user.id,
            parent_comment_id=parent_comment_id,
        )

        await self._comment_repo.add(comment)
        return comment

    async def update_comment(
        self, user: User, comment: Comment, update_data: DTOData[Comment]
    ) -> Comment:
        """Обновление комментария.

        Args:
            user (User): Пользователь
            comment (Comment): Комментарий для обновления
            update_data (DTOData[Comment]): Данные для обновления

        Returns:
            Comment: Обновленный комментарий

        Raises:
            CommentPermissionError: Если пользователь не является автором комментария
        """
        if user.id != comment.author_id:
            raise CommentPermissionError

        built = update_data.as_builtins()
        content = built.get("content")

        updated_comment = comment.update(content=content)
        await self._comment_repo.update(comment.id, updated_comment)

        return updated_comment

    async def delete_comment(self, user: User, comment: Comment) -> bool:
        """Удаление комментария.

        Args:
            user (User): Пользователь
            comment (Comment): Комментарий для удаления

        Returns:
            bool: Статус удаления

        Raises:
            CommentPermissionError: Если пользователь не является автором комментария
        """
        if user.id != comment.author_id:
            raise CommentPermissionError

        result = await self._comment_repo.delete(comment.id)
        return result
