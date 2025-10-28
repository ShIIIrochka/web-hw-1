# -*- coding: utf-8 -*-

from litestar import Controller, Request, delete, get, post, put
from litestar.datastructures import State
from litestar.dto import DataclassDTO
from litestar.exceptions import (
    NotAuthorizedException,
    NotFoundException,
    PermissionDeniedException,
)
from litestar.status_codes import HTTP_204_NO_CONTENT
from punq import Container

from src.api.dto.posts import CreatePostDTO, PostDTO, UpdatePostDTO
from src.application.services.post_service import PostService
from src.domain.entities.post import Post
from src.domain.entities.user import User
from src.domain.exceptions.post import PostNotFoundError, PostPermissionError


class PostController(Controller):
    path = "/posts"
    tags = ["Posts"]

    @get("/{post_id:str}", response_dto=PostDTO)
    async def get_post(
        self,
        post_id: str,
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
        dto=DataclassDTO[CreatePostDTO],
        response_dto=PostDTO,
        security=[{"BearerAuth": []}],
    )
    async def create_post(
        self,
        data: CreatePostDTO,
        container: Container,
        request: Request[User, str, State],
    ) -> Post:
        """Создание нового поста."""
        post_service: PostService = container.resolve(PostService)
        user = request.user
        if not user:
            raise NotAuthorizedException
        post = await post_service.create_post(user, data)
        return post

    @put(
        "/{post_id:str}/update",
        dto=DataclassDTO[UpdatePostDTO],
        response_dto=PostDTO,
        security=[{"BearerAuth": []}],
    )
    async def update_post(
        self,
        post_id: str,
        data: UpdatePostDTO,
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
        except PostPermissionError as e:
            raise PermissionDeniedException(detail=str(e))

    @delete(
        "/{post_id:str}/delete",
        status_code=HTTP_204_NO_CONTENT,
        security=[{"BearerAuth": []}],
    )
    async def delete_post(
        self,
        post_id: str,
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
        except PostPermissionError as e:
            raise PermissionDeniedException(detail=str(e))
