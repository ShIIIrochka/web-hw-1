# -*- coding: utf-8 -*2-

from typing import Any

from jam.aio import Jam

from blog.infra.providers.interfaces import AuthProvider


class JWTProvider(AuthProvider):
    """Провайдер аутентификации с использованием JWT."""

    def __init__(self, jam_instance: Jam) -> None:
        """Конструктор.

        Args:
            jam_instance (Jam): Инстанс джема
        """
        self.jam_instance = jam_instance

    async def create(self, exp: int, data: dict[str, Any]) -> str:
        """Создание JWT токена."""
        payload = await self.jam_instance.make_payload(exp, data=data)
        return await self.jam_instance.gen_jwt_token(payload)

    async def verify(self, token: str) -> dict:
        """Верификация JWT токена."""
        return await self.jam_instance.verify_jwt_token(
            token=token, check_exp=True, check_list=False
        )
