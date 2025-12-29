# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class PostSearchHit:
    """Value Object для результата поиска поста."""

    post_id: UUID
    title: str
    content: str
    author_id: UUID
    created_at: datetime
    updated_at: datetime
    score: float
    highlight: dict[str, list[str]]


@dataclass(frozen=True)
class PostSearchResult:
    """Value Object для результата поискового запроса."""

    hits: list[PostSearchHit]
    total: int
    limit: int
    offset: int
