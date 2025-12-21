# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class AccessTokenExpiredError(Exception):
    """Ошибка при истечении срока жизни access токена."""

    message: str | Exception = "Время жизни токена истекло, нужен refresh."


@dataclass
class InvalidToken(Exception):
    """Ошибка при невалидном токене."""

    message: str | Exception = "Не валидный токен авторизации."
