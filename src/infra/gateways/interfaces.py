# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod


class DBGateway(ABC):
    """Гейтвей для подключения к базе данных."""

    @abstractmethod
    async def init(self) -> None:
        """Инициализация подключения к базе данных."""
        pass
