# -*- coding: utf-8 -*-

from uuid import UUID

from litestar import Controller, Request, delete, get, post, put
from litestar.datastructures import State
from litestar.dto import DTOData
from litestar.exceptions import (
    NotFoundException,
    PermissionDeniedException,
)
from litestar.status_codes import HTTP_204_NO_CONTENT, HTTP_200_OK
from punq import Container

from src.api.dto.posts import CreatePostDTO, PostDTO, UpdatePostDTO
from src.api.guards.auth import auth_guard
from src.application.services.post_service import PostService
from src.domain.entities.post import Post
from src.domain.entities.user import User
from src.domain.exceptions.category import CategoryNotFoundError
from src.domain.exceptions.post import PostNotFoundError, PostPermissionError


class PostController(Controller):
    path = "/posts"
    tags = ["Posts"]
    return_dto = PostDTO
    security = [{"BearerAuth": []}],
    guards = [auth_guard]

    @get("/{post_id:uuid}", status_code=HTTP_200_OK)
    async def get_post(
        self,
        post_id: UUID,
        container: Container,
    ) -> Post:
        """Получение поста по ID."""
        post_service: PostService = container.resolve(PostService)
        try:
            return await post_service.get_post_by_id(post_id)
        except PostNotFoundError:
            raise NotFoundException(detail="Post not found")

    @post(
        "/create",
        dto=CreatePostDTO,
    )
    async def create_post(
        self,
        data: DTOData[Post],
        container: Container,
        request: Request[User, str, State],
    ) -> Post:
        """Создание нового поста."""
        post_service: PostService = container.resolve(PostService)
        try:
            post = await post_service.create_post(request.user, data)
            return post
        except CategoryNotFoundError:
            raise NotFoundException(detail="One or more categories not found")

    @put(
        "/{post_id:uuid}/update",
        status_code=HTTP_200_OK,
        dto=UpdatePostDTO,
    )
    async def update_post(
        self,
        post_id: UUID,
        data: DTOData[Post],
        container: Container,
        request: Request[User, str, State],
    ) -> Post:
        """Обновление поста."""
        post_service: PostService = container.resolve(PostService)
        try:
            post = await post_service.get_post_by_id(post_id)
        except PostNotFoundError:
            raise NotFoundException
        try:
            return await post_service.update_post(request.user, post, data)
        except PostPermissionError:
            raise PermissionDeniedException

    @delete(
        "/{post_id:uuid}/delete",
        status_code=HTTP_204_NO_CONTENT,
    )
    async def delete_post(
        self,
        post_id: UUID,
        container: Container,
        request: Request[User, str, State],
    ) -> None:
        """Удаление поста."""
        post_service: PostService = container.resolve(PostService)
        try:
            post = await post_service.get_post_by_id(post_id)
        except PostNotFoundError:
            raise NotFoundException
        try:
            await post_service.delete_post(request.user, post)
        except PostPermissionError:
            raise PermissionDeniedException

    @get(
        "/user/{author_id:uuid}",
        status_code=HTTP_200_OK,
    )
    async def get_posts_by_author(
        self,
        author_id: UUID,
        container: Container,
    ) -> list[Post]:
        """Получение постов пользователя по его ID."""
        post_service: PostService = container.resolve(PostService)
        posts = await post_service.get_posts_by_author(author_id)
        return posts