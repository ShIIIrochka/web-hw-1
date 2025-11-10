# -*- coding: utf-8 -*-

from typing import Sequence
from uuid import UUID

from litestar import Controller, Request, get, post
from litestar.datastructures import State
from litestar.exceptions import NotAuthorizedException, NotFoundException
from litestar.status_codes import HTTP_200_OK
from punq import Container

from src.api.dto.categories import CategoryDTO, CreateCategoryDTO
from src.api.guards.auth import auth_guard
from src.application.services.category_service import CategoryService
from src.domain.entities.category import Category
from src.domain.entities.user import User
from src.domain.exceptions.category import CategoryNotFoundError


class CategoryController(Controller):
    """Контроллер для работы с категориями."""

    path = "/categories"
    tags = ["Categories"]
    guards = [auth_guard]
    security: list[dict[str, list]] = [{"BearerAuth": []}]
    return_dto = CategoryDTO

    @post(
        path="/create",
        dto=CreateCategoryDTO,
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

    @get(path="", status_code=HTTP_200_OK)
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

    @get(path="/{category_id:uuid}", status_code=HTTP_200_OK)
    async def get_category_by_id(
        self,
        category_id: UUID,
        container: Container,
    ) -> CategoryDTO:
        """Получение категории по ID."""
        category_service = container.resolve(CategoryService)
        try:
            category = await category_service.get_category_by_id(category_id)
        except CategoryNotFoundError:
            raise NotFoundException
        return category
