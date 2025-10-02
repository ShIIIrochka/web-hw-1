# -*- coding: utf-8 -*2-

from abc import ABC, abstractmethod
from typing import Any


class AuthProvider(ABC):
    """Интерфейс для провайдеров аутентификации."""

    @abstractmethod
    async def create(self, **kwargs) -> Any:
        """Создание jwt токена/сессии/др."""
        raise NotImplementedError

    @abstractmethod
    async def verify(self, **kwargs) -> Any:
        """Верификация jwt токена/сессии/др."""
        raise NotImplementedError
