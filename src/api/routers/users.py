# -*- coding: utf-8 -*-

from litestar import Controller, Request, get, post, put
from litestar.datastructures import State
from litestar.dto import DTOData
from litestar.exceptions import NotAuthorizedException, ValidationException
from litestar.status_codes import HTTP_200_OK, HTTP_204_NO_CONTENT
from punq import Container

from src.api.dto.users import UpdateUserDTO, UserDTO
from src.application.services.user_service import UserService
from src.domain.entities.user import User
from src.domain.exceptions.user import EmailSyntaxError


class UserController(Controller):
    """Контроллер для работы с пользователями."""

    path = "/user"
    tags = ["Users"]

    @get(
        path="/",
        return_dto=UserDTO,
        status_code=HTTP_200_OK,
        security=[{"BearerAuth": []}],
    )
    async def get_user(self, request: Request[User, str, State]) -> User:
        """Получение информации о пользователе."""
        user = request.user
        if not user:
            raise NotAuthorizedException
        return user

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
        user = request.user
        if not user:
            raise NotAuthorizedException

        user_service = container.resolve(UserService)
        email: str = data.as_builtins()["email"]
        login: str = data.as_builtins()["login"]
        try:
            updated_user = await user_service.update_user(
                user,
                login,
                email,
            )
        except EmailSyntaxError:
            raise ValidationException(detail="Invalid email format.")
        return updated_user

    @post(
        path="/delete",
        status_code=HTTP_204_NO_CONTENT,
        security=[{"BearerAuth": []}],
    )
    async def delete_user(
        self, request: Request[User, str, State], container: Container
    ) -> None:
        """Удаление информации о пользователе"""
        user = request.user
        if not user:
            raise NotAuthorizedException
        user_service = container.resolve(UserService)
        await user_service.delete_user(user)
