# -*- coding: utf-8 -*-
from uuid import UUID

from src.domain.entities.category import Category
from src.domain.exceptions.category import CategoryNotFoundError
from src.domain.repositories.category_repository import BaseCategoryRepository


class CategoryService:
    """Сервис для работы с категориями."""

    def __init__(self, repository: BaseCategoryRepository) -> None:
        """Конструктор.

        Args:
            repository: Репозиторий для работы с БД
        """
        self._repo = repository

    async def create_category(self, data: Category) -> Category:
        """Создание категории.

        Args:

        Returns:
            Category: Созданная категория
        """
        name = data.name
        category = Category.create(name=name)
        await self._repo.add(category)
        return category

    async def get_all_categories(
        self, limit: int, cursor: UUID | None
    ) -> list[Category]:
        """Получение всех категорий.

        Args:
            limit (int): Лимит на количество категорий
            cursor (Optional[UUID]): Курсор для пагинации

        Returns:
            list[Category]: Список категорий
        """
        categories = await self._repo.get_many(cursor, limit)
        return categories

    async def get_category_by_id(self, id: UUID) -> Category:
        """Get a single category by id.

        Raises:
            ValueError: if category is not found

        Returns:
            Category
        """
        category = await self._repo.get_by_id(id)
        if not category:
            raise CategoryNotFoundError
        return category

    async def delete_category(self, id: UUID) -> bool:
        """Удаление категории.

        Args:
            id (UUID): ID категории

        Returns:
            bool: Статус удаления

        Raises:
            CategoryNotFoundError: Если категория не найдена
        """
        category = await self._repo.get_by_id(id)
        if not category:
            raise CategoryNotFoundError
        return await self._repo.delete(id)
