# -*- coding: utf-8 -*-

from typing import Sequence
from uuid import UUID

from litestar import Controller, Request, get, post
from litestar.datastructures import State
from litestar.exceptions import NotAuthorizedException
from punq import Container

from src.api.dto.categories import CategoryDTO, CreateCategoryDTO
from src.application.services.category_service import CategoryService
from src.domain.entities.category import Category
from src.domain.entities.user import User


class CategoryController(Controller):
    """Контроллер для работы с категориями."""

    path = "/categories"
    tags = ["Categories"]

    @post(
        path="/create",
        dto=CreateCategoryDTO,
        return_dto=CategoryDTO,
        security=[{"BearerAuth": []}],
    )
    async def create_category(
        self,
        data: Category,
        request: Request[User, str, State],
        container: Container,
    ) -> CategoryDTO:
        """Создание категории."""
        user = request.user
        if not user:
            raise NotAuthorizedException
        category_service = container.resolve(CategoryService)
        category = await category_service.create_category(data)
        return category

    @get(
        path="",
        return_dto=CategoryDTO,
    )
    async def get_all_categories(
        self,
        limit: int = 10,
        cursor: UUID | None = None,
        container: Container = None,
    ) -> Sequence[CategoryDTO]:
        """Получение всех категорий."""
        category_service = container.resolve(CategoryService)
        categories = await category_service.get_all_categories(limit, cursor)
        return categories
