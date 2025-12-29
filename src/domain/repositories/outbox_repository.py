# -*- coding: utf-8 -*-

from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID


class BaseOutboxRepository(ABC):
    """Абстрактный репозиторий для работы с outbox событиями."""

    @abstractmethod
    async def add_event(
        self,
        aggregate_type: str,
        aggregate_id: UUID,
        event_type: str,
        payload: dict,
    ) -> UUID:
        """Добавление события в outbox."""
        raise NotImplementedError

    @abstractmethod
    async def get_pending_events(
        self, limit: int = 10, worker_id: str | None = None
    ) -> list:
        """Получение pending событий для обработки."""
        raise NotImplementedError

    @abstractmethod
    async def mark_processing(self, event_id: UUID, worker_id: str) -> None:
        """Пометить событие как обрабатываемое."""
        raise NotImplementedError

    @abstractmethod
    async def mark_processed(self, event_id: UUID) -> None:
        """Пометить событие как обработанное."""
        raise NotImplementedError

    @abstractmethod
    async def mark_failed(self, event_id: UUID, error: str) -> None:
        """Пометить событие как проваленное."""
        raise NotImplementedError
