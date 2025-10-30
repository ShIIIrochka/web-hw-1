# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
from uuid import UUID

from src.domain.entities.base_model import BaseModel
from src.domain.entities.user import User


@dataclass
class Post(BaseModel):
    """Модель поста."""

    author_id: str | UUID
    title: str
    content: str
    categories: list[dict[str, Any]] | None = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @classmethod
    def create(
        cls,
        author: User,
        title: str,
        content: str,
    ) -> Post:
        """Создает новый пост.

        Args:
            author (User): Автор поста
            title (str): Заголовок поста
            content (str): Содержимое поста

        Returns:
            Post: Созданный пост
        """
        post = cls(
            author_id=author.id,
            title=title,
            content=content,
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
