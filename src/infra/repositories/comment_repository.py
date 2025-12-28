# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import asdict
from uuid import UUID

from src.domain.entities.comment import Comment
from src.domain.repositories.comment_repository import BaseCommentRepository
from src.infra.models.comment import Comment as CommentModel


class CommentRepository(BaseCommentRepository):
    """Репозиторий для работы с комментариями."""

    def __init__(
        self,
        model: type[CommentModel] = CommentModel,
    ) -> None:
        """Конструктор.

        Args:
            model (type[CommentModel]): Модель комментария
        """
        self._model = model

    async def add(self, data: Comment) -> str:
        """Добавление комментария в БД."""
        comment_data = asdict(data)

        new_comment = await self._model.create(**comment_data)

        return str(new_comment.id)

    async def get_by_id(self, id: UUID) -> Comment | None:
        """Получение конкретного комментария из БД."""
        comment = await self._model.get_or_none(id=id)
        if not comment:
            return None
        return await comment.to_entity()

    async def get_by_post(self, post_id: UUID) -> list[Comment]:
        """Получение всех комментариев к посту (включая вложенные)."""
        comments = await self._model.filter(post_id=post_id).order_by(
            "created_at"
        )
        return [await comment.to_entity() for comment in comments]

    async def update(self, id: UUID, update_data: Comment) -> Comment:
        """Обновление комментария."""
        update_dict = asdict(update_data)
        update_dict.pop("id", None)

        await self._model.filter(id=id).update(**update_dict)

        comment = await self._model.get_or_none(id=id)

        if not comment:
            raise ValueError("Comment not found")

        return await comment.to_entity()

    async def delete(self, id: UUID) -> bool:
        """Удаление комментария."""
        deleted_count = await self._model.filter(id=id).delete()
        return deleted_count > 0
