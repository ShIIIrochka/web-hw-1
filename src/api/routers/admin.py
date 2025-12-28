# -*- coding: utf-8 -*-

from __future__ import annotations

from uuid import UUID

from litestar import Controller, delete
from litestar.exceptions import NotFoundException
from litestar.status_codes import HTTP_204_NO_CONTENT
from punq import Container

from src.api.guards.admin import is_admin
from src.api.guards.auth import auth_guard
from src.application.services.category_service import CategoryService
from src.application.services.user_service import UserService
from src.domain.exceptions.category import CategoryNotFoundError
from src.domain.exceptions.user import UserNotFoundError
from src.domain.repositories.comment_repository import BaseCommentRepository
from src.domain.repositories.post_repository import BasePostRepository
from src.domain.repositories.post_search_repository import (
    BasePostSearchRepository,
)


class AdminController(Controller):
    """Контроллер для админских операций."""

    path = "/admin"
    tags = ["Admin"]
    guards = [auth_guard, is_admin]
    security: list[dict[str, list]] = [{"BearerAuth": []}]

    @delete(
        "/posts/{post_id:uuid}",
        status_code=HTTP_204_NO_CONTENT,
    )
    async def delete_post(
        self,
        post_id: UUID,
        container: Container,
    ) -> None:
        """Удаление любого поста (админ)."""
        post_repo: BasePostRepository = container.resolve(BasePostRepository)
        search_repo: BasePostSearchRepository = container.resolve(
            BasePostSearchRepository
        )

        post = await post_repo.get_by_id(post_id)
        if not post:
            raise NotFoundException(detail="Post not found")

        await post_repo.delete(post_id)
        await search_repo.delete(post_id)

    @delete(
        "/comments/{comment_id:uuid}",
        status_code=HTTP_204_NO_CONTENT,
    )
    async def delete_comment(
        self,
        comment_id: UUID,
        container: Container,
    ) -> None:
        """Удаление любого комментария (админ)."""
        comment_repo: BaseCommentRepository = container.resolve(
            BaseCommentRepository
        )

        comment = await comment_repo.get_by_id(comment_id)
        if not comment:
            raise NotFoundException(detail="Comment not found")

        await comment_repo.delete(comment_id)

    @delete(
        "/users/{user_id:uuid}",
        status_code=HTTP_204_NO_CONTENT,
    )
    async def delete_user(
        self,
        user_id: UUID,
        container: Container,
    ) -> None:
        """Удаление любого пользователя (админ)."""
        user_service: UserService = container.resolve(UserService)

        try:
            await user_service.delete_user(user_id)
        except UserNotFoundError:
            raise NotFoundException(detail="User not found")

    @delete(
        "/categories/{category_id:uuid}",
        status_code=HTTP_204_NO_CONTENT,
    )
    async def delete_category(
        self,
        category_id: UUID,
        container: Container,
    ) -> None:
        """Удаление любой категории (админ)."""
        category_service: CategoryService = container.resolve(CategoryService)

        try:
            await category_service.delete_category(category_id)
        except CategoryNotFoundError:
            raise NotFoundException(detail="Category not found")
