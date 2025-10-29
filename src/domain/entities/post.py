# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from bson import ObjectId

from domain.entities.category import Category
from src.domain.entities.base_model import BaseModel
from src.domain.entities.user import User


@dataclass
class Post(BaseModel):
    """Модель поста."""

    author_id: str | ObjectId
    title: str
    content: str
    category_ids: list[str | ObjectId] | None = None
    categories: list[Category] | None = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @classmethod
    def from_raw(cls, raw: dict) -> Post:
        """Собирает модель из raw, например при сборке из репозитория.

        Args:
            raw (dict): RAW в dict формате

        Returns:
            Post: Собранная модель
        """
        post = cls(
            author_id=str(raw["author_id"]),
            title=raw["title"],
            content=raw["content"],
            created_at=raw["created_at"],
            updated_at=raw["updated_at"],
            category_ids=raw["category_ids"],
            categories=[
                Category.from_raw(cat) for cat in raw.get("categories_full", [])
            ],
        )
        post._id = str(raw["_id"])
        return post

    @classmethod
    def create(
        cls,
        author: User,
        title: str,
        content: str,
        category_ids: list[str | ObjectId] | None,
    ) -> Post:
        """Создает новый пост.

        Args:
            author (User): Автор поста
            title (str): Заголовок поста
            content (str): Содержимое поста
            category_ids (list[str | ObjectId] | None): Список ID категорий

        Returns:
            Post: Созданный пост
        """
        post = cls(
            author_id=author.id,
            title=title,
            content=content,
            category_ids=category_ids,
        )
        return post

    def update(self, title: str, content: str) -> Post:
        """Обновляет пост.

        Args:
            title (str): Новый заголовок поста
            content (str): Новое содержимое поста

        Returns:
            Post: Обновленный пост
        """
        self.title = title
        self.content = content
        self.updated_at = datetime.now()
        return self

    def add_category(self, category_id: str | ObjectId) -> None:
        """Добавляет категорию к посту.

        Args:
            category_id (str | ObjectId): ID категории
        """
        if self.category_ids is None:
            self.category_ids = []
        self.category_ids.append(category_id)
