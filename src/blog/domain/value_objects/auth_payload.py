# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from blog.domain.entities import User


@dataclass
class JWTPayload:
    """Пейлоад для JWT авторизации.

    Используется для обычных пользователей.
    """

    user_id: str
    token_type: Literal["access", "refresh"]

    @classmethod
    def make_payload(
        cls, user: User, token_type: Literal["access", "refresh"]
    ) -> JWTPayload:
        """Генерация пейлоада для пользователя.

        Args:
            user (User): Пользователь
            token_type (Literal["access", "refresh"]): Тип токена
        """
        return cls(
            user_id=user.id,
            token_type=token_type,
        )