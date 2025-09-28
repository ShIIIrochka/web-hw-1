# -*- coding: utf-8 -*-

from jam.aio import Jam
from jam.exceptions import TokenLifeTimeExpired

from blog.application.exceptions.auth import AccessTokenExpiredError, InvalidToken
from blog.domain.entities import User
from blog.domain.value_objects.auth_payload import JWTPayload
from blog.domain.value_objects.tokens import JWT


class UserAuthService:
    """Сервис для авторизации пользователей."""

    def __init__(self, jam: Jam, access_exp: int) -> None:
        """Конструктор.

        Args:
            jam (Jam): Инстанс джема
            access_exp (int): Время жизни access токена
        """
        self._jam = jam
        self.access_exp = access_exp

    async def auth_user(self, user: User) -> JWT:
        """Авторизация пользователя.

        Args:
            user (User): Пользователь, для которого выписываем JWT токены

        Returns:
            JWT: Access и refresh токены
        """
        access_token = await self._jam.gen_jwt_token(
            payload=(
                await self._jam.make_payload(
                    exp=self.access_exp,
                    **JWTPayload.make_payload(user, "access").__dict__,
                )
            )
        )
        refresh_token = await self._jam.gen_jwt_token(
            payload=(
                await self._jam.make_payload(
                    **JWTPayload.make_payload(user, "refresh").__dict__
                )
            )
        )

        return JWT(refresh=refresh_token, access=access_token)

    async def decode_access_token(self, token: str) -> JWTPayload:
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
            payload = await self._jam.verify_jwt_token(
                token=token, check_exp=True, check_list=False
            )
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