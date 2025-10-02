# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class DeleteSessionError(Exception):
    """Ошибка при удалении сессии."""

    message: str | Exception


@dataclass
class EmailValidationError(Exception):
    """При неверном формате емейла."""

    message: str | Exception = "Неверный формат email'а."


@dataclass
class EmailAlreadyTakenError(Exception):
    """При занятом email."""

    message: str | Exception = "Этот email уже используется."


@dataclass
class EmailAlreadyVerificatedError(Exception):
    """При попытке повторной верификации email'а."""

    message: str | Exception = "Email уже подтвержден."


@dataclass
class InvalidOTPCodeError(Exception):
    """Неверный TOTP код."""

    message: str | Exception = "Неверный код."


@dataclass
class AccessTokenExpiredError(Exception):
    """Ошибка при истечении срока жизни access токена."""

    message: str | Exception = "Время жизни токена истекло, нужен refresh."


@dataclass
class InvalidToken(Exception):
    """Ошибка при невалидном токене."""

    message: str | Exception = "Не валидный токен авторизации."
