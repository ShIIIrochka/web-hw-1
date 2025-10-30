# -*- coding: utf-8 -*-

from src.domain.entities.category import Category
from src.api.dto.categories import CreateCategoryDTO
from src.domain.repositories.category_repository import BaseCategoryRepository


class CategoryService:
    """Сервис для работы с категориями."""

    def __init__(self, repository: BaseCategoryRepository) -> None:
        """Конструктор.

        Args:
            repository: Репозиторий для работы с БД
        """
        self._repo = repository

    async def create_category(self, data: Category | CreateCategoryDTO) -> Category:
        """Создание категории.

        Args:

        Returns:
            Category: Созданная категория
        """
        # accept either a Category entity or DTO. Read name safely.
        if hasattr(data, "name") and data.name is not None:
            name = data.name
        elif hasattr(data, "as_builtins"):
            name = data.as_builtins().get("name")
        else:
            name = None

        if not name:
            raise ValueError("Category name is required")

        category = Category.create(name=name)
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

    async def get_category_by_id(self, id: str) -> Category:
        """Get a single category by id.

        Raises:
            ValueError: if category is not found

        Returns:
            Category
        """
        category = await self._repo.get_by_id(id)
        if not category:
            raise ValueError("Category not found")
        return category
