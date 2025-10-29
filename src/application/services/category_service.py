# -*- coding: utf-8 -*-

from api.dto.categories import CreateCategoryDTO
from domain.entities.category import Category
from domain.repositories.category_repository import BaseCategoryRepository


class CategoryService:
    """Сервис для работы с категориями."""

    def __init__(self, repository: BaseCategoryRepository) -> None:
        """Конструктор.

        Args:
            repository: Репозиторий для работы с БД
        """
        self._repo = repository

    async def create_category(self, data: CreateCategoryDTO) -> Category:
        """Создание категории.

        Args:

        Returns:
            Category: Созданная категория
        """
        category = Category.create(name=data.name)
        await self._repo.add(category)
        return category

    async def get_all_categories(
        self, limit: int, cursor: str | None
    ) -> list[Category]:
        """Получение всех категорий.

        Args:
            limit (int): Лимит на количество категорий
            cursor (Optional[str]): Курсор для пагинации

        Returns:
            list[Category]: Список категорий
        """
        categories = await self._repo.get_many(cursor, limit)
        return categories
