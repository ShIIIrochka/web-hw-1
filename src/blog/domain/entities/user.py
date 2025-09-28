# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from src.blog.domain.entities.base_model import BaseModel


@dataclass
class User(BaseModel):
    """Модель пользователя."""

    email: str
    login: str
    password: str
    created_at: datetime  # Дата и время создания
    updated_at: datetime  # Дата и время последнего редактирования

    @classmethod
    def from_raw(cls, raw: dict[str, Any]) -> User:
        """Собирает модель из raw, например при сборке из репозитория.

        Args:
            raw (dict[str, Any]): RAW в dict формате

        Returns:
            User: Собранная модель
        """
        user = cls(
            email=raw["email"],
            login=raw["login"],
            password=raw["password"],
            created_at=raw["created_at"],
            updated_at=raw["updated_at"],
        )
        user._id = raw["_id"]
        return user

