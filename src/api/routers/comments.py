# -*- coding: utf-8 -*-

from __future__ import annotations

from uuid import UUID

from litestar import Controller, Request, delete, get, post, put
from litestar.datastructures import State
from litestar.dto import DTOData
from litestar.exceptions import (
    NotFoundException,
    PermissionDeniedException,
)
from litestar.status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
)
from punq import Container

from src.api.dto.comments import CommentDTO, CreateCommentDTO, UpdateCommentDTO
from src.api.guards.auth import auth_guard
from src.application.services.comment_service import CommentService
from src.application.services.post_service import PostService
from src.domain.entities.comment import Comment
from src.domain.entities.user import User
from src.domain.exceptions.comment import (
    CommentNotFoundError,
    CommentPermissionError,
)
from src.domain.exceptions.post import PostNotFoundError


class CommentController(Controller):
    path = "/comments"
    tags = ["Comments"]
    return_dto = CommentDTO
    security: list[dict[str, list]] = [{"BearerAuth": []}]
    guards = [auth_guard]

    @get("/{comment_id:uuid}", status_code=HTTP_200_OK)
    async def get_comment(
        self,
        comment_id: UUID,
        container: Container,
    ) -> Comment:
        """Получение комментария по ID."""
        comment_service: CommentService = container.resolve(CommentService)
        try:
            return await comment_service.get_comment_by_id(comment_id)
        except CommentNotFoundError:
            raise NotFoundException(detail="Comment not found")

    @get("/post/{post_id:uuid}", status_code=HTTP_200_OK)
    async def get_comments_by_post(
        self,
        post_id: UUID,
        container: Container,
    ) -> list[Comment]:
        """Получение всех комментариев к посту."""
        comment_service: CommentService = container.resolve(CommentService)
        post_service: PostService = container.resolve(PostService)
        try:
            post = await post_service.get_post_by_id(post_id)
            return await comment_service.get_comments_by_post(post)
        except PostNotFoundError:
            raise NotFoundException(detail="Post not found")

    @post(
        "/post/{post_id:uuid}",
        status_code=HTTP_201_CREATED,
        dto=CreateCommentDTO,
    )
    async def create_comment(
        self,
        post_id: UUID,
        data: DTOData[Comment],
        container: Container,
        request: Request[User, str, State],
    ) -> Comment:
        """Создание комментария к посту."""
        comment_service: CommentService = container.resolve(CommentService)
        try:
            comment = await comment_service.create_comment(
                request.user, post_id, data
            )
            return comment
        except PostNotFoundError:
            raise NotFoundException(detail="Post not found")
        except CommentNotFoundError:
            raise NotFoundException(detail="Parent comment not found")

    @post(
        "/{parent_comment_id:uuid}/reply",
        status_code=HTTP_201_CREATED,
        dto=CreateCommentDTO,
    )
    async def reply_to_comment(
        self,
        parent_comment_id: UUID,
        data: DTOData[Comment],
        container: Container,
        request: Request[User, str, State],
    ) -> Comment:
        """Создание ответа на комментарий."""
        comment_service: CommentService = container.resolve(CommentService)
        try:
            parent_comment = await comment_service.get_comment_by_id(
                parent_comment_id
            )

            comment = await comment_service.create_comment(
                request.user, parent_comment.post_id, data, parent_comment_id
            )
            return comment
        except CommentNotFoundError:
            raise NotFoundException(detail="Comment not found")
        except PostNotFoundError:
            raise NotFoundException(detail="Post not found")

    @put(
        "/{comment_id:uuid}",
        status_code=HTTP_200_OK,
        dto=UpdateCommentDTO,
    )
    async def update_comment(
        self,
        comment_id: UUID,
        data: DTOData[Comment],
        container: Container,
        request: Request[User, str, State],
    ) -> Comment:
        """Обновление комментария."""
        comment_service: CommentService = container.resolve(CommentService)
        try:
            comment = await comment_service.get_comment_by_id(comment_id)
        except CommentNotFoundError:
            raise NotFoundException(detail="Comment not found")

        try:
            return await comment_service.update_comment(
                request.user, comment, data
            )
        except CommentPermissionError:
            raise PermissionDeniedException(
                detail="You can only edit your own comments"
            )

    @delete(
        "/{comment_id:uuid}",
        status_code=HTTP_204_NO_CONTENT,
    )
    async def delete_comment(
        self,
        comment_id: UUID,
        container: Container,
        request: Request[User, str, State],
    ) -> None:
        """Удаление комментария."""
        comment_service: CommentService = container.resolve(CommentService)
        try:
            comment = await comment_service.get_comment_by_id(comment_id)
        except CommentNotFoundError:
            raise NotFoundException(detail="Comment not found")

        try:
            await comment_service.delete_comment(request.user, comment)
        except CommentPermissionError:
            raise PermissionDeniedException(
                detail="You can only delete your own comments"
            )
