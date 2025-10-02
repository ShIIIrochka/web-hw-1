# -*- coding: utf-8 -*-

from dataclasses import dataclass, field

from bson import ObjectId


@dataclass
class BaseModel:
    """Базовая модель для работы."""

    _id: str = field(default_factory=ObjectId, kw_only=True)

    @property
    def id(self) -> str:
        """Возвращает ID в человеко читаемом виде."""
        return str(self._id)
