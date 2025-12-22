# -*- coding: utf-8 -*-

from __future__ import annotations

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

    @abstractmethod
    async def close(self) -> None:
        """Закрытие подключения к базе данных."""
        raise NotImplementedError


class CacheProvider(ABC):
    """Провайдер для кэширования."""

    @abstractmethod
    async def get(self, key: str) -> str | None:
        """Получение значения из кэша."""
        raise NotImplementedError

    @abstractmethod
    async def set(self, key: str, value: str, ttl: int | None = None) -> None:
        """Сохранение значения в кэш."""
        raise NotImplementedError

    @abstractmethod
    async def delete(self, key: str) -> None:
        """Удаление значения из кэша."""
        raise NotImplementedError


class SearchProvider(ABC):
    """Провайдер для полнотекстового поиска."""

    @abstractmethod
    async def init(self) -> None:
        """Инициализация подключения к поисковому движку."""
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        """Закрытие подключения."""
        raise NotImplementedError

    @abstractmethod
    async def index_post(self, post_data: dict[str, Any]) -> None:
        """Индексация поста."""
        raise NotImplementedError

    @abstractmethod
    async def update_post(
        self, post_id: str, post_data: dict[str, Any]
    ) -> None:
        """Обновление поста в индексе."""
        raise NotImplementedError

    @abstractmethod
    async def delete_post(self, post_id: str) -> None:
        """Удаление поста из индекса."""
        raise NotImplementedError

    @abstractmethod
    async def search_posts(
        self, query: str, limit: int = 10, offset: int = 0
    ) -> dict[str, Any]:
        """Поиск постов по запросу."""
        raise NotImplementedError
