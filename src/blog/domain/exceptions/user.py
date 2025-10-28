# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class UserNotFoundError(Exception):
    """Ошибка при отсутствии пользователя в БД."""

    message: str | Exception = "Пользователь не найден."


@dataclass
class EmailSyntaxError(Exception):
    """Ошибка при неверном формате email."""

    message: str | Exception = "Неверный формат email."
