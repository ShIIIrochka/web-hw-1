# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class PostSearchHitDTO:
    """DTO для результата поиска одного поста."""

    post_id: UUID
    title: str
    content: str
    author_id: UUID
    created_at: datetime
    updated_at: datetime
    score: float
    highlight: dict[str, list[str]]


@dataclass
class PostSearchResultDTO:
    """DTO для результатов поискового запроса."""

    hits: list[PostSearchHitDTO]
    total: int
    limit: int
    offset: int
