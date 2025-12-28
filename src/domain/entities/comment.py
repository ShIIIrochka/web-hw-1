# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from src.domain.entities.base_model import BaseModel


@dataclass
class Comment(BaseModel):
    """Модель комментария."""

    content: str
    post_id: UUID
    author_id: UUID
    parent_comment_id: UUID | None = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @classmethod
    def create(
        cls,
        content: str,
        post_id: UUID,
        author_id: UUID,
        parent_comment_id: UUID | None = None,
    ) -> Comment:
        """Создает новый комментарий.

        Args:
            content (str): Содержимое комментария
            post_id (UUID): ID поста
            author_id (UUID): ID автора комментария
            parent_comment_id (UUID | None): ID родительского комментария (для вложенных комментариев)

        Returns:
            Comment: Созданный комментарий
        """
        comment = cls(
            content=content,
            post_id=post_id,
            author_id=author_id,
            parent_comment_id=parent_comment_id,
        )
        return comment

    def update(self, content: str) -> Comment:
        """Обновляет комментарий.

        Args:
            content (str): Новое содержимое комментария

        Returns:
            Comment: Обновленный комментарий
        """
        self.content = content
        self.updated_at = datetime.now()
        return self
