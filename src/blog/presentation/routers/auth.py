# -*- coding: utf-8 -*-

from litestar import Controller, Request, post
from litestar.datastructures import State
from punq import Container

from blog.application.dto.tokens import JWTTokens
from blog.application.dto.users import UserDTO
from blog.application.services.auth_service import AuthService
from blog.application.services.user_service import UserService
from blog.domain.entities.user import User
from blog.domain.value_objects.tokens import JWT


class AuthController(Controller):
    """Контроллер для авторизации/аутентификации."""

    path = "/user/auth"
    tags = ["Auth"]

    @post(
        path="/register",
        dto=UserDTO,
        return_dto=JWTTokens,
    )
    async def register(
        self,
        data: User,
        request: Request[User, str, State],
        container: Container,
    ) -> JWT:
        """Регистрация пользователя."""

        user_service: UserService = container.resolve(UserService)
        auth_service: AuthService = container.resolve(AuthService)
        user = await user_service.create_user(data.__dict__)
        tokens = await auth_service.auth_user(user)
        return tokens
