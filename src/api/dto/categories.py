# -*- coding: utf-8 -*-

from litestar.dto import DTOConfig, DataclassDTO

from domain.entities.category import Category


class CategoryDTO(DataclassDTO[Category]):
    """DTO для категории."""

    config = DTOConfig(underscore_fields_private=True)


class CreateCategoryDTO(DataclassDTO[Category]):
    """DTO для создания категории."""

    config = DTOConfig()
