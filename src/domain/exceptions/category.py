# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class CategoryNotFoundError(Exception):
    """Ошибка при отсутствии категории в БД."""

    message: str | Exception = "Category not found."


@dataclass
class CategoryAlreadyExistsError(Exception):
    """Ошибка при попытке создать категорию с существующим именем."""

    message: str | Exception = "Category with this name already exists."
