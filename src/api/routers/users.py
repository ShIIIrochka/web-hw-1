# -*- coding: utf-8 -*-

from litestar import Controller, Request, get, post, put
from litestar.datastructures import State
from litestar.dto import DTOData
from litestar.exceptions import ValidationException
from litestar.status_codes import HTTP_200_OK, HTTP_204_NO_CONTENT
from punq import Container

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

    @get(
        path="/me",
        return_dto=UserDTO,
        status_code=HTTP_200_OK,
        security=[{"BearerAuth": []}],
    )
    async def get_me(self, request: Request[User, str, State]) -> User:
        """Получение информации о текущем пользователе."""
        return request.user

    @put(
        path="/update",
        dto=UpdateUserDTO,
        return_dto=UserDTO,
        status_code=HTTP_200_OK,
        security=[{"BearerAuth": []}],
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

    @post(
        path="/delete",
        status_code=HTTP_204_NO_CONTENT,
        security=[{"BearerAuth": []}],
        response_cookies={"token": ""},
        response_headers={},
    )
    async def delete_user(
        self, request: Request[User, str, State], container: Container
    ) -> None:
        """Удаление информации о пользователе"""
        user_service = container.resolve(UserService)
        await user_service.delete_user(request.user.id)
