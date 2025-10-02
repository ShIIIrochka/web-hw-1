# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from bson import ObjectId

from blog.domain.entities.user import User
from blog.domain.entities.base_model import BaseModel


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

    @staticmethod
    def create(
        author: User, title: str, content: str
    ) -> dict[str, str | ObjectId | datetime]:
        """Создает новый пост.

        Args:
            author (User): Автор поста
            title (str): Заголовок поста
            content (str): Содержимое поста

        Returns:
            data (dict[str, str | ObjectId | datetime]): Данные для создания поста в БД
        """
        return {
            "author_id": ObjectId(author.id),
            "title": title,
            "content": content,
            "created_at": datetime.now(),
            "updated_at": datetime.now(),
        }
