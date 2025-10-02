# -*- coding: utf-8 -*-

from litestar import Controller, Request, Response, post
from litestar.datastructures import Cookie, State
from punq import Container

from blog.application.dto.tokens import JWTTokens
from blog.application.dto.users import UserDTO
from blog.application.services.auth_service import AuthService
from blog.application.services.user_service import UserService
from blog.domain.entities.user import User
from blog.domain.value_objects.tokens import JWT
from blog.infra.config import Config


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
        container: Container,
    ) -> Response[JWT]:
        """Регистрация пользователя."""

        user_service: UserService = container.resolve(UserService)
        auth_service: AuthService = container.resolve(AuthService)
        user = await user_service.create_user(data.__dict__)
        tokens = await auth_service.auth_user(user)
        return Response(
            tokens,
            cookies=[
                Cookie(
                    key="token",
                    value=tokens.refresh,
                    httponly=True,
                    samesite="strict",
                    max_age=container.resolve(Config).refresh_exp,
                ),
            ],
            headers={"Authorization": f"Bearer {tokens.access}"},
        )

    @post(
        path="/refresh",
        return_dto=JWTTokens,
    )
    async def refresh(
        self,
        request: Request[User, str, State],
        container: Container = None,
    ) -> Response[JWT]:
        """Обновление токенов."""
        auth_service: AuthService = container.resolve(AuthService)
        tokens = await auth_service.refresh_tokens(request.cookies.get("token"))
        return Response(
            tokens,
            cookies=[
                Cookie(
                    key="token",
                    value=tokens.refresh,
                    httponly=True,
                    samesite="strict",
                    max_age=container.resolve(Config).refresh_exp,
                ),
            ],
            headers={"Authorization": f"Bearer {tokens.access}"},
        )
