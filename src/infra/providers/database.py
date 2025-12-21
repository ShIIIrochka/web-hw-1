# -*- coding: utf-8 -*-

from tortoise import Tortoise

from .interfaces import DBProvider


class PostgresProvider(DBProvider):
    """Провайдер для подключения к MongoDB."""

    def __init__(
        self,
        uri: str,
        modules: dict[str, list[str]],
    ) -> None:
        """Конструктор.

        Args:
            uri (str): URI подключение к MongoDB
            modules (dict[str, list[str]]): Модули с моделями

        Returns:
            None
        """
        self.db_uri = uri
        self.modules = modules

    async def init(self):
        await Tortoise.init(db_url=self.db_uri, modules=self.modules)
        await Tortoise.generate_schemas()

    @staticmethod
    async def close():
        await Tortoise.close_connections()
