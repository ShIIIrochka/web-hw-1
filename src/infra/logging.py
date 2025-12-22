# -*- coding: utf-8 -*-

from __future__ import annotations

import json
import logging
import sys

from datetime import datetime
from typing import Any


class JSONFormatter(logging.Formatter):
    """JSON formatter для структурированных логов."""

    def format(self, record: logging.LogRecord) -> str:
        """Форматирование лога в JSON."""
        log_data: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Добавляем request_id если есть
        if hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id

        # Добавляем HTTP метаданные если есть
        if hasattr(record, "path"):
            log_data["path"] = record.path
        if hasattr(record, "method"):
            log_data["method"] = record.method
        if hasattr(record, "status_code"):
            log_data["status_code"] = record.status_code
        if hasattr(record, "duration_ms"):
            log_data["duration_ms"] = record.duration_ms
        if hasattr(record, "user_id"):
            log_data["user_id"] = str(record.user_id)

        # Добавляем exception если есть
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_data, ensure_ascii=False)


def setup_logging(level: str = "INFO") -> None:
    """Настройка JSON-логирования для приложения.

    Args:
        level: уровень логирования (DEBUG, INFO, WARNING, ERROR)
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Удаляем существующие handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Создаем handler для stdout с JSON форматом
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    root_logger.addHandler(handler)

    # Настраиваем логеры библиотек
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("tortoise").setLevel(logging.WARNING)
