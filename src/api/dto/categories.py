# -*- coding: utf-8 -*-

from __future__ import annotations

from litestar.dto import DTOConfig, DataclassDTO

from src.domain.entities.category import Category


class CategoryDTO(DataclassDTO[Category]):
    """DTO для категории."""

    config = DTOConfig(underscore_fields_private=True)


class CreateCategoryDTO(DataclassDTO[Category]):
    """DTO для создания категории."""

    config = DTOConfig()
