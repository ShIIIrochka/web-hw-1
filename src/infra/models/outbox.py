# -*- coding: utf-8 -*-

from __future__ import annotations

from datetime import datetime, timedelta
from enum import Enum

from tortoise import fields, models


class OutboxStatus(str, Enum):
    """Статусы событий в outbox."""

    PENDING = "pending"
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"


class OutboxEvent(models.Model):
    """Модель события в outbox для eventual consistency."""

    id = fields.UUIDField(pk=True)
    aggregate_type = fields.CharField(max_length=50)  # 'post', 'user', etc.
    aggregate_id = fields.UUIDField()
    event_type = fields.CharField(max_length=100)  # 'post.created', etc.
    payload = fields.JSONField()
    status = fields.CharEnumField(OutboxStatus, default=OutboxStatus.PENDING)
    attempts = fields.IntField(default=0)
    max_attempts = fields.IntField(default=5)
    next_run_at = fields.DatetimeField(default=datetime.now)
    locked_at = fields.DatetimeField(null=True)
    locked_by = fields.CharField(max_length=255, null=True)
    last_error = fields.TextField(null=True)
    created_at = fields.DatetimeField(default=datetime.now)
    processed_at = fields.DatetimeField(null=True)

    class Meta:
        table = "outbox_events"
        indexes = [
            ("status", "next_run_at"),
            ("aggregate_type", "aggregate_id"),
        ]

    def mark_processing(self, worker_id: str) -> None:
        """Пометить событие как обрабатываемое."""
        self.status = OutboxStatus.PROCESSING
        self.locked_at = datetime.now()
        self.locked_by = worker_id
        self.attempts += 1

    def mark_processed(self) -> None:
        """Пометить событие как обработанное."""
        self.status = OutboxStatus.PROCESSED
        self.processed_at = datetime.now()
        self.locked_at = None
        self.locked_by = None

    def mark_failed(self, error: str) -> None:
        """Пометить событие как проваленное с ошибкой."""
        self.last_error = error
        if self.attempts >= self.max_attempts:
            self.status = OutboxStatus.FAILED
        else:
            # Возвращаем в pending с экспоненциальным backoff
            self.status = OutboxStatus.PENDING
            backoff_seconds = min(2**self.attempts * 60, 3600)  # макс 1 час
            self.next_run_at = datetime.now() + timedelta(
                seconds=backoff_seconds
            )
        self.locked_at = None
        self.locked_by = None
