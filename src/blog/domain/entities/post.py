# -*- coding: utf-8 -*-

from dataclasses import dataclass
from datetime import datetime

from src.blog.domain.entities.base_model import BaseModel


@dataclass
class Post(BaseModel):
    """Модель поста."""

    title: str
    content: str
    createdAt: datetime # Дата и время создания
    updatedAt: datetime # Дата и время последнего редактирования