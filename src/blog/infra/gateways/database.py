# -*- coding: utf-8 -*-

from pymongo import AsyncMongoClient

from .interfaces import DBGateway


class MongoGateway(DBGateway):
    """Гейтвей для подключения к MongoDB."""

    def __init__(self, uri: str, db_name: str) -> None:
        """Конструктор.

        Args:
            uri (str): URI подключение к MongoDB
            db_name (str): Имя базы данных

        Returns:
            None
        """
        self.client = AsyncMongoClient(uri)
        self.db = self.client[db_name]

    @property
    async def get_connection(self) -> None:
        """Создание асинхронного коннекшена."""
        await self.client.aconnect()
        return None

    async def get_collection(self, collection_name: str):
        """Получаем/создаем коллекцию.

        Args:
            collection_name (str): Имя коллекции
        """
        return self.db[collection_name]