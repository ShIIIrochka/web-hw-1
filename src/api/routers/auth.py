# -*- coding: utf-8 -*-

from litestar import Controller, Request, Response, post
from litestar.datastructures import Cookie, State
from litestar.dto import DTOData
from litestar.exceptions import (
    NotAuthorizedException,
    NotFoundException,
    ValidationException,
)
from litestar.status_codes import HTTP_200_OK, HTTP_204_NO_CONTENT
from punq import Container

from src.api.dto.tokens import JWTTokens
from src.api.dto.users import CreateUserDTO, LoginUserDTO
from src.application.services.auth_service import AuthService
from src.application.services.user_service import UserService
from src.domain.entities.user import User
from src.domain.exceptions.user import EmailSyntaxError, UserNotFoundError
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
        config: Config = container.resolve(Config)
        try:
            user = await user_service.create_user(data)
        except EmailSyntaxError:
            raise ValidationException(detail="Invalid email format.")
        tokens = await auth_service.auth_user(user)

        # Use 'lax' for dev (localhost), 'none' for prod with HTTPS
        samesite = "lax" if config.debug else "none"
        secure = not config.debug

        return Response(
            tokens,
            cookies=[
                Cookie(
                    key="access_token",
                    value=tokens.access,
                    httponly=True,
                    samesite=samesite,
                    secure=secure,
                    max_age=config.access_exp,
                ),
                Cookie(
                    key="refresh_token",
                    value=tokens.refresh,
                    httponly=True,
                    samesite=samesite,
                    secure=secure,
                    max_age=config.refresh_exp,
                ),
            ],
            headers={"Authorization": f"Bearer {tokens.access}"},
        )

    @post(
        path="/refresh",
        status_code=HTTP_200_OK,
        return_dto=JWTTokens,
    )
    async def refresh(
        self,
        request: Request[User, str, State],
        container: Container = None,
    ) -> Response[JWT]:
        """Обновление токенов."""
        auth_service: AuthService = container.resolve(AuthService)
        config: Config = container.resolve(Config)
        token: str | None = request.cookies.get("refresh_token")
        if token:
            tokens = await auth_service.refresh_tokens(token)
        else:
            raise NotAuthorizedException

        samesite = "lax" if config.debug else "none"
        secure = not config.debug

        return Response(
            tokens,
            cookies=[
                Cookie(
                    key="access_token",
                    value=tokens.access,
                    httponly=True,
                    samesite=samesite,
                    secure=secure,
                    max_age=config.access_exp,
                ),
                Cookie(
                    key="refresh_token",
                    value=tokens.refresh,
                    httponly=True,
                    samesite=samesite,
                    secure=secure,
                    max_age=config.refresh_exp,
                ),
            ],
            headers={"Authorization": f"Bearer {tokens.access}"},
        )

    @post(
        path="/login",
        status_code=HTTP_200_OK,
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
        config: Config = container.resolve(Config)
        try:
            user = await user_service.get_user(data)
        except UserNotFoundError as e:
            raise NotFoundException(detail=str(e))
        except EmailSyntaxError as e:
            raise ValidationException(detail=str(e))
        tokens = await auth_service.auth_user(user)

        samesite = "lax" if config.debug else "none"
        secure = not config.debug

        return Response(
            tokens,
            cookies=[
                Cookie(
                    key="access_token",
                    value=tokens.access,
                    httponly=True,
                    samesite=samesite,
                    secure=secure,
                    max_age=config.access_exp,
                ),
                Cookie(
                    key="refresh_token",
                    value=tokens.refresh,
                    httponly=True,
                    samesite=samesite,
                    secure=secure,
                    max_age=config.refresh_exp,
                ),
            ],
            headers={"Authorization": f"Bearer {tokens.access}"},
        )

    @post(
        path="/logout",
        status_code=HTTP_204_NO_CONTENT,
    )
    async def logout(
        self,
        container: Container,
    ) -> Response[None]:
        """Выход пользователя (очистка cookies)."""
        config: Config = container.resolve(Config)

        samesite = "lax" if config.debug else "none"
        secure = not config.debug

        return Response(
            None,
            cookies=[
                Cookie(
                    key="access_token",
                    value="",
                    httponly=True,
                    samesite=samesite,
                    secure=secure,
                    max_age=0,
                ),
                Cookie(
                    key="refresh_token",
                    value="",
                    httponly=True,
                    samesite=samesite,
                    secure=secure,
                    max_age=0,
                ),
            ],
        )
