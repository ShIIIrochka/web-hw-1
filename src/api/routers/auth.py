# -*- coding: utf-8 -*-

from litestar import Controller, Request, Response, post
from litestar.datastructures import Cookie, State
from litestar.dto import DTOData
from litestar.exceptions import (
    NotAuthorizedException,
    NotFoundException,
    ValidationException,
)
from punq import Container

from api.dto.users import LoginUserDTO
from domain.exceptions.user import UserNotFoundError
from src.api.dto.tokens import JWTTokens
from src.api.dto.users import CreateUserDTO
from src.application.services.auth_service import AuthService
from src.application.services.user_service import UserService
from src.domain.entities.user import User
from src.domain.exceptions.user import EmailSyntaxError
from src.domain.value_objects.tokens import JWT
from src.infra.config import Config


class AuthController(Controller):
    """Контроллер для авторизации/аутентификации."""

    path = "/user/auth"
    tags = ["Auth"]

    @post(
        path="/register",
        dto=CreateUserDTO,
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
        try:
            user = await user_service.create_user(data)
        except EmailSyntaxError:
            raise ValidationException(detail="Invalid email format.")
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
        token: str | None = request.cookies.get("token")
        if token:
            tokens = await auth_service.refresh_tokens(token)
        else:
            raise NotAuthorizedException
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
        path="/login",
        dto=LoginUserDTO,
        return_dto=JWTTokens,
    )
    async def login(
        self,
        data: DTOData[User],
        container: Container,
    ) -> Response[JWT]:
        """Вход пользователя."""
        user_service: UserService = container.resolve(UserService)
        auth_service: AuthService = container.resolve(AuthService)
        try:
            user = await user_service.get_user(data)
        except UserNotFoundError as e:
            raise NotFoundException(detail=str(e))
        except EmailSyntaxError as e:
            raise ValidationException(detail=str(e))
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
