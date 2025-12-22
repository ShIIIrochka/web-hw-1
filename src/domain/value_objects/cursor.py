# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass
from typing import Generic, TypeVar
from uuid import UUID


T = TypeVar("T")


@dataclass
class Page(Generic[T]):
    """Страница с результатами и курсором."""

    items: list[T]
    next_cursor: UUID | None
    has_more: bool
