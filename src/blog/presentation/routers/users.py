# -*- coding: utf-8 -*-

from litestar import Controller, Request, get, post
from litestar.datastructures import State
from litestar.exceptions import NotAuthorizedException
from punq import Container

from blog.application.dto.users import UserDTO
from blog.application.services.user_service import UserService
from blog.domain.entities.user import User


class UserController(Controller):
    """Контроллер для работы с пользователями."""

    path = "/user"
    tags = ["Users"]

    @get(
        path="/",
        return_dto=UserDTO,
        security=[{"BearerAuth": []}],
    )
    async def get_user(self, request: Request[User, str, State]) -> User:
        """Получение информации о пользователе."""
        user = request.user
        if not user:
            raise NotAuthorizedException
        return user

    @post(
        path="/update",
        dto=UserDTO,
        return_dto=UserDTO,
        security=[{"BearerAuth": []}],
    )
    async def update_user(
        self,
        data: User,
        request: Request[User, str, State],
        container: Container,
    ) -> User:
        """Обновление информации о пользователе."""
        user = request.user
        if not user:
            raise NotAuthorizedException

        user_service = container.resolve(UserService)
        user = await user_service.update_user(user, data.__dict__)
        return user

    @post(
        path="/delete",
        security=[{"BearerAuth": []}],
    )
    async def delete_user(
        self, request: Request[User, str, State], container: Container
    ) -> bool:
        """Удаление информации о пользователе"""
        user = request.user
        if not user:
            raise NotAuthorizedException
        user_service = container.resolve(UserService)
        return await user_service.delete_user(user)
