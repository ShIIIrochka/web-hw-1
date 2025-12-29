# -*- coding: utf-8 -*-

from __future__ import annotations

from litestar.dto import DTOConfig, DataclassDTO

from src.domain.entities.category import Category


class CategoryDTO(DataclassDTO[Category]):
    """DTO для категории."""

    config = DTOConfig()


class CreateCategoryDTO(DataclassDTO[Category]):
    """DTO для создания категории."""

    config = DTOConfig(exclude={"created_at", "updated_at", "id"})
