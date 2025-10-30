# -*- coding: utf-8 -*-

from dataclasses import asdict
from uuid import UUID

from src.domain.entities.post import Post
from src.domain.repositories.post_repository import BasePostRepository
from src.infra.models import Post as PostModel


class PostRepository(BasePostRepository):
    """Репозиторий для работы с постами."""

    def __init__(
        self,
        model: type[PostModel] = PostModel,
    ) -> None:
        """Конструктор.

        Args:
            model (type[PostModel]): Модель поста
        """
        self._model = model

    async def add(self, data: Post) -> str:
        """Добавление поста в БД."""
        post_data = asdict(data)
        post_data.pop("id", None)
        categories = post_data.pop("categories")

        new_post = await self._model.create(**post_data)

        if categories:
            category_ids = [cat.id for cat in categories]
            if category_ids:
                await new_post.categories.add(*category_ids)

        return str(new_post.id)

    async def get_by_id(self, id: str) -> Post | None:
        """Получение конкретного поста из БД."""
        post = await self._model.get_or_none(id=UUID(id))
        if not post:
            return None
        return await post.to_entity(include_categories=True)

    async def get_many(
        self, cursor: str | None = None, limit: int = 10
    ) -> list[Post]:
        """Получение N объектов из БД."""
        query = self._model.all().order_by("created_at")
        if cursor:
            query = query.filter(self._model.id > UUID(cursor))
        posts = await query.limit(limit)
        result = []
        for post in posts:
            result.append(await post.to_entity(include_categories=True))
        return result

    async def update(self, id: str, update_data: Post) -> Post:
        """Обновление поста."""
        update_dict = asdict(update_data)
        update_dict.pop("id", None)
        categories = update_dict.pop("categories")

        await self._model.filter(id=id).update(**update_dict)

        post = await self._model.get_or_none(id=UUID(id))

        if categories:
            await post.fetch_related("categories")
            await post.categories.clear()
            category_ids = [cat.id for cat in categories]
            if category_ids:
                await post.categories.add(*category_ids)

        return await post.to_entity(include_categories=True)

    async def delete(self, id: str) -> bool:
        """Удаление объекта."""
        deleted_count = await self._model.filter(id=UUID(id)).delete()
        return deleted_count > 0
