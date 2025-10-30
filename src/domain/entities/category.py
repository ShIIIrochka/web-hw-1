# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any

from src.domain.entities.base_model import BaseModel


@dataclass
class Category(BaseModel):
    """Модель категории."""

    name: str
    posts: list[dict[str, Any]] | None = None
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    @classmethod
    def create(cls, name: str) -> Category:
        """Создает новую категорию.

        Args:
            name (str): Название категории

        Returns:
            Category: Созданная категория
        """
        category = cls(
            name=name,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        return category
