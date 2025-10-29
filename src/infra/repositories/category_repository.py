# -*- coding: utf-8 -*-

from dataclasses import asdict

from bson import ObjectId

from domain.entities.category import Category
from domain.repositories.category_repository import BaseCategoryRepository


class CategoryRepository(BaseCategoryRepository):
    """Репозиторий для работы с категориями."""

    def __init__(self, gateway, collection_name: str) -> None:
        """Конструктор.

        Args:
            gateway (DBGateway): Гейт подключения к бд
            collection_name (str): Имя коллекции
        """
        self.__gw = gateway
        self.collection_name = collection_name

    async def _init_collection(self):
        return await self.__gw.get_collection(self.collection_name)

    async def add(self, data: Category) -> str:
        """Добавление документа в БД.

        Args:
            data (dict[str, Any]): Документ

        Returns:
            str: ID нового документа
        """
        collection = await self._init_collection()
        result = await collection.insert_one(asdict(data))
        return str(result.inserted_id)

    async def get_by_id(self, id: str) -> Category | None:
        """Получение конкретного объекта из БД.

        Args:
            id (str): ID объекта

        Returns:
            dict[str, Any]: Результат поиска
        """
        collection = await self._init_collection()
        try:
            result = await collection.find_one({"_id": ObjectId(id)})
        except Exception as e:
            raise ValueError(e)
        if result:
            return Category.from_raw(result)
        return None

    async def get_many(
        self, cursor: str | None, limit: int = 10
    ) -> list[Category]:
        """Получение N объектов из БД.

        Args:
            cursor (str, optional): Курсор для пагинации. Defaults to None.
            limit (int, optional): Лимит. Defaults to 10.

        Returns:
            list[dict[str, Any]]: Результаты поиска
        """
        collection = await self._init_collection()
        query = {"_id": {"$gt": cursor}} if cursor else {}
        cursor = collection.find(query).limit(limit)
        results = []
        for document in cursor:
            results.append(document)
        return [Category.from_raw(res) for res in results]
