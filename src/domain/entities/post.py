# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from src.domain.entities.base_model import BaseModel


@dataclass
class Post(BaseModel):
    """Модель поста."""

    author_id: UUID
    title: str
    content: str
    categories: list[UUID] | None = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @classmethod
    def create(
        cls,
        user_id: UUID,
        title: str,
        content: str,
        categories: list[UUID] | None,
    ) -> Post:
        """Создает новый пост.

        Args:
            user_id (UUID): Автор поста
            title (str): Заголовок поста
            content (str): Содержимое поста
            categories (list[UUID] | None): Список id категорий поста

        Returns:
            Post: Созданный пост
        """
        post = cls(
            author_id=user_id,
            title=title,
            content=content,
            categories=categories,
        )
        return post

    def add_category(self, category_id: UUID) -> None:
        """Добавляет категорию к посту.

        Args:
            category_id (UUID): ID категории
        """
        if self.categories is None:
            self.categories = []
        self.categories.append(category_id)

    def update(
        self, title: str, content: str, categories: list[UUID] | None
    ) -> Post:
        """Обновляет пост.

        Args:
            title (str): Заголовок поста
            content (str): Cодержание поста
            categories (list[UUID] | None): Cписок id категорий поста

        Returns:
            Post: Обновленный пост
        """
        self.categories = categories
        self.title = title
        self.content = content
        self.categories = categories
        self.updated_at = datetime.now()
        return self
