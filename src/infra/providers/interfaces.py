# -*- coding: utf-8 -*2-

from abc import ABC, abstractmethod
from typing import Any


class AuthProvider(ABC):
    """Интерфейс для провайдеров аутентификации."""

    @abstractmethod
    async def create(self, data: dict, exp: int) -> Any:
        """Создание jwt токена/сессии/др."""
        raise NotImplementedError

    @abstractmethod
    async def verify(self, token: str) -> Any:
        """Верификация jwt токена."""
        raise NotImplementedError


class DBProvider(ABC):
    """Провайдер для подключения к базе данных."""

    @abstractmethod
    async def init(self) -> None:
        """Инициализация подключения к базе данных."""
        raise NotImplementedError
