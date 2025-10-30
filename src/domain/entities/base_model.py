# -*- coding: utf-8 -*-

from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass
class BaseModel:
    """Базовая модель для работы."""

    id: UUID = field(default_factory=uuid4, kw_only=True)
