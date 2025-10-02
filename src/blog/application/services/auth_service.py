# -*- coding: utf-8 -*-

from jam.exceptions import TokenLifeTimeExpired

from blog.application.exceptions.auth import (
    AccessTokenExpiredError,
    InvalidToken,
)
from blog.domain.entities.user import User
from blog.domain.value_objects.auth_payload import JWTPayload
from blog.domain.value_objects.tokens import JWT
from blog.infra.providers.interfaces import AuthProvider


class AuthService:
    """Сервис для авторизации пользователей."""

    def __init__(
        self, auth_provider: AuthProvider, access_exp: int, refresh_exp: int
    ) -> None:
        """Конструктор.

        Args:
            auth_provider (AuthProvider): Провайдер аутентификации
            access_exp (int): Время жизни access токена
            refresh_exp (int): Время жизни refresh токена
        """
        self.auth_provider = auth_provider
        self.access_exp = access_exp
        self.refresh_exp = refresh_exp

    async def auth_user(self, user: User) -> JWT:
        """Авторизация пользователя.

        Args:
            user (User): Пользователь, для которого выписываем JWT токены

        Returns:
            JWT: Access и refresh токены
        """
        access_token = await self.auth_provider.create(
            data=JWTPayload.make_payload(user, "access").__dict__,
            exp=self.access_exp,
        )
        refresh_token = await self.auth_provider.create(
            data=JWTPayload.make_payload(user, "refresh").__dict__,
            exp=self.refresh_exp,
        )

        return JWT(refresh=refresh_token, access=access_token)

    async def get_payload(self, token: str) -> JWTPayload:
        """Декодирование access токена.

        Args:
            token (str): Access токен

        Raises:
            AccessTokenExpiredError: Если время жизни токена истекло
            InvalidToken: Если токен не валиден

        Returns:
            JWTPayload: Пейлоад токена
        """
        try:
            payload = await self.auth_provider.verify(token=token)
        except TokenLifeTimeExpired:
            raise AccessTokenExpiredError
        except ValueError:
            raise InvalidToken

        try:
            if payload["token_type"] != "access":
                raise InvalidToken
        except KeyError:
            raise InvalidToken

        return JWTPayload(
            user_id=payload["user_id"],
            token_type=payload["token_type"],
        )
