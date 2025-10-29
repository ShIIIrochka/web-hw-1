# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass

from domain.entities.base_model import BaseModel


@dataclass
class Category(BaseModel):
    """Модель категории."""

    name: str

    @classmethod
    def from_raw(cls, raw: dict) -> Category:
        """Собирает модель из raw, например при сборке из репозитория.

        Args:
            raw (dict): RAW в dict формате
        Returns:
            Category: Собранная модель
        """
        category = cls(
            name=raw["name"],
        )
        category._id = str(raw["_id"])
        return category

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
        )
        return category
