# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from typing import Any


class DBGateway(ABC):
    """Гейтвей для подключения к базе данных."""

    @abstractmethod
    def get_connection(self) -> Any:
        """Получение или создание коннекшена."""
        raise NotImplementedError

    @abstractmethod
    def get_collection(self, collection_name: str) -> Any:
        """Получение или создание коллекции."""
        raise NotImplementedError
