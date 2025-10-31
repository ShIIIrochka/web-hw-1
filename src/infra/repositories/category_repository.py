# -*- coding: utf-8 -*-

from dataclasses import asdict
from uuid import UUID

from src.domain.entities.category import Category
from src.domain.repositories.category_repository import BaseCategoryRepository
from src.infra.models import Category as CategoryModel


class CategoryRepository(BaseCategoryRepository):
    """Репозиторий для работы с категориями."""

    def __init__(self, model: type[CategoryModel] = CategoryModel) -> None:
        """Конструктор.

        Args:
            model (type[CategoryModel], optional): ORM модель
        """
        self._model = model

    async def add(self, data: Category) -> str:
        """Добавление документа в БД."""
        category_data = asdict(data)
        category = await self._model.create(**category_data)
        return str(category.id)

    async def get_by_id(self, id: UUID) -> Category | None:
        """Получение конкретного объекта из БД."""
        category = await self._model.get_or_none(id=id)
        if category is None:
            return None
        return await category.to_entity()

    async def get_many(
        self, cursor: UUID | None, limit: int = 10
    ) -> list[Category]:
        """Получение N объектов из БД."""
        query = self._model.all().limit(limit)
        if cursor:
            query = query.filter(id__gt=cursor)
        categories = await query
        result = []
        for category in categories:
            entity = await category.to_entity()
            result.append(entity)
        return result
