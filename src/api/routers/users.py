# -*- coding: utf-8 -*-

from uuid import UUID

from litestar import Controller, Request, delete, get, post, put
from litestar.datastructures import State
from litestar.dto import DTOData
from litestar.exceptions import ValidationException
from litestar.status_codes import HTTP_200_OK, HTTP_204_NO_CONTENT
from punq import Container

from src.api.dto.posts import PostDTO
from src.api.dto.users import UpdateUserDTO, UserDTO
from src.api.guards.auth import auth_guard
from src.application.services.user_service import UserService
from src.domain.entities.user import User
from src.domain.exceptions.user import EmailSyntaxError


class UserController(Controller):
    """Контроллер для работы с пользователями."""

    path = "/users"
    tags = ["Users"]
    guards = [auth_guard]
    security: list[dict[str, list]] = [{"BearerAuth": []}]

    @get(
        path="/me",
        return_dto=UserDTO,
        status_code=HTTP_200_OK,
    )
    async def get_me(self, request: Request[User, str, State]) -> User:
        """Получение информации о текущем пользователе."""
        return request.user

    @get(
        path="/{user_id:uuid}",
        return_dto=UserDTO,
        status_code=HTTP_200_OK,
    )
    async def get_user_by_id(
        self,
        user_id: UUID,
        container: Container,
    ) -> User:
        """Получение информации о пользователе по ID."""
        user_service = container.resolve(UserService)
        user = await user_service.get_user_by_id(str(user_id))
        return user

    @get(path="/posts/saved", return_dto=PostDTO, status_code=HTTP_200_OK)
    async def get_saved_posts(
        self,
        request: Request[User, str, State],
        container: Container,
    ) -> list[PostDTO]:
        """Получение сохранённых постов текущего пользователя."""
        user_service = container.resolve(UserService)
        saved_posts = await user_service.get_saved_posts(request.user.id)
        return saved_posts

    @put(
        path="/update",
        dto=UpdateUserDTO,
        return_dto=UserDTO,
        status_code=HTTP_200_OK,
    )
    async def update_user(
        self,
        data: DTOData[User],
        request: Request[User, str, State],
        container: Container,
    ) -> User:
        """Обновление информации о пользователе."""
        user_service = container.resolve(UserService)
        try:
            updated_user = await user_service.update_user(request.user, data)
        except EmailSyntaxError:
            raise ValidationException(detail="Invalid email format.")
        return updated_user

    @delete(
        path="/delete",
        status_code=HTTP_204_NO_CONTENT,
        response_cookies={"token": ""},
        response_headers={},
    )
    async def delete_user(
        self, request: Request[User, str, State], container: Container
    ) -> None:
        """Удаление информации о пользователе"""
        user_service = container.resolve(UserService)
        await user_service.delete_user(request.user.id)

    @post(
        path="/posts/save/{post_id:uuid}",
        status_code=HTTP_204_NO_CONTENT,
        security=[{"BearerAuth": []}],
    )
    async def save_post(
        self,
        post_id: UUID,
        request: Request[User, str, State],
        container: Container,
    ) -> None:
        """Сохранение поста пользователем."""
        user_service = container.resolve(UserService)
        await user_service.save_post(request.user.id, post_id)

    @delete(
        path="/unsave-post/{post_id:uuid}",
        status_code=HTTP_204_NO_CONTENT,
        security=[{"BearerAuth": []}],
    )
    async def unsave_post(
        self,
        post_id: UUID,
        request: Request[User, str, State],
        container: Container,
    ) -> None:
        """Удаление сохраненного поста пользователем."""
        user_service = container.resolve(UserService)
        await user_service.unsave_post(request.user.id, post_id)
