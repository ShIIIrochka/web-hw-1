# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from bson import ObjectId

from src.domain.entities.base_model import BaseModel
from src.domain.entities.user import User


@dataclass
class Post(BaseModel):
    """Модель поста."""

    author_id: str
    title: str
    content: str
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
        )
        post._id = str(raw["_id"])
        return post

    @classmethod
    def create(cls, author: User, title: str, content: str) -> Post:
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
            _id=str(ObjectId()),
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
