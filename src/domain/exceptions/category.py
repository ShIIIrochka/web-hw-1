# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class CategoryNotFoundError(Exception):
    """Ошибка при отсутствии категории в БД."""

    message: str | Exception = "Category not found."
