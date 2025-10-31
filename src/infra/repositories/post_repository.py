# -*- coding: utf-8 -*-

from dataclasses import asdict
from uuid import UUID

from src.domain.entities.post import Post
from src.domain.repositories.post_repository import BasePostRepository
from src.infra.models import Category as CategoryModel
from src.infra.models import Post as PostModel


class PostRepository(BasePostRepository):
    """Репозиторий для работы с постами."""

    def __init__(
        self,
        model: type[PostModel] = PostModel,
        category_model: type[CategoryModel] = CategoryModel,
    ) -> None:
        """Конструктор.

        Args:
            model (type[PostModel]): Модель поста
            category_model (type[CategoryModel]): Модель категории
        """
        self._model = model
        self._category_model = category_model

    async def add(self, data: Post) -> str:
        """Добавление поста в БД."""
        post_data = asdict(data)
        categories = post_data.pop("categories")

        new_post = await self._model.create(**post_data)

        if categories:
            for cat in categories:
                category = await self._category_model.get_or_none(id=cat)
                if category:
                    await new_post.categories.add(category)
                else:
                    raise ValueError

        return str(new_post.id)

    async def get_by_id(self, id: UUID) -> Post | None:
        """Получение конкретного поста из БД."""
        post = await self._model.get_or_none(id=id)
        if not post:
            return None
        return await post.to_entity()

    async def get_many(
        self, cursor: UUID | None = None, limit: int = 10
    ) -> list[Post]:
        """Получение N объектов из БД."""
        query = self._model.all().order_by("created_at")
        if cursor:
            query = query.filter(id__gt=cursor)
        posts = await query.limit(limit)
        result = []
        for post in posts:
            result.append(await post.to_entity())
        return result

    async def update(self, id: UUID, update_data: Post) -> Post:
        """Обновление поста."""
        update_dict = asdict(update_data)
        update_dict.pop("id", None)
        categories = update_dict.pop("categories")

        await self._model.filter(id=id).update(**update_dict)

        post = await self._model.get_or_none(id=id)

        if not post:
            raise ValueError
        if categories:
            await post.fetch_related("categories")
            await post.categories.clear()
            for cat in categories:
                category = await self._category_model.get_or_none(id=cat)
                if category:
                    await post.categories.add(category)
                else:
                    raise ValueError

        return await post.to_entity()

    async def delete(self, id: UUID) -> bool:
        """Удаление объекта."""
        deleted_count = await self._model.filter(id=id).delete()
        return deleted_count > 0
