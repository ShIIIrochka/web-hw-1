# -*- coding: utf-8 -*-

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from src.domain.repositories.outbox_repository import BaseOutboxRepository
from src.infra.models.outbox import OutboxEvent, OutboxStatus


class OutboxRepository(BaseOutboxRepository):
    """Репозиторий для работы с outbox событиями."""

    def __init__(self, model: type[OutboxEvent] = OutboxEvent) -> None:
        """Конструктор."""
        self._model = model

    async def add_event(
        self,
        aggregate_type: str,
        aggregate_id: UUID,
        event_type: str,
        payload: dict,
    ) -> UUID:
        """Добавление события в outbox."""
        event = await self._model.create(
            aggregate_type=aggregate_type,
            aggregate_id=aggregate_id,
            event_type=event_type,
            payload=payload,
        )
        return event.id

    async def get_pending_events(
        self, limit: int = 10, worker_id: str | None = None
    ) -> list[OutboxEvent]:
        """Получение pending событий для обработки."""
        now = datetime.now()
        events = await self._model.filter(
            status=OutboxStatus.PENDING, next_run_at__lte=now
        ).limit(limit)
        return list(events)

    async def claim_pending_events(
        self, limit: int, worker_id: str, lock_ttl_seconds: int = 300
    ) -> list[OutboxEvent]:
        """Атомарно забрать pending события с блокировкой.

        Args:
            limit: Максимальное количество событий
            worker_id: Идентификатор воркера
            lock_ttl_seconds: TTL блокировки в секундах

        Returns:
            Список заблокированных событий
        """
        from datetime import timedelta

        now = datetime.now()
        lock_expired_at = now - timedelta(seconds=lock_ttl_seconds)

        pending_events = (
            await self._model.filter(
                status=OutboxStatus.PENDING, next_run_at__lte=now
            )
            .limit(limit)
            .all()
        )

        expired_locked = []
        if len(pending_events) < limit:
            expired_locked = (
                await self._model.filter(
                    status=OutboxStatus.PROCESSING,
                    locked_at__lte=lock_expired_at,
                )
                .limit(limit - len(pending_events))
                .all()
            )

        claimed_events = []

        for event in list(pending_events) + list(expired_locked):
            event.mark_processing(worker_id)
            await event.save()
            claimed_events.append(event)

        return claimed_events

    async def mark_processing(self, event_id: UUID, worker_id: str) -> None:
        """Пометить событие как обрабатываемое."""
        event = await self._model.get(id=event_id)
        event.mark_processing(worker_id)
        await event.save()

    async def mark_processed(self, event_id: UUID) -> None:
        """Пометить событие как обработанное."""
        event = await self._model.get(id=event_id)
        event.mark_processed()
        await event.save()

    async def mark_failed(self, event_id: UUID, error: str) -> None:
        """Пометить событие как проваленное."""
        event = await self._model.get(id=event_id)
        event.mark_failed(error)
        await event.save()
