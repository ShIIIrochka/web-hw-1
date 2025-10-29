# -*- coding: utf-8 -*-

from dataclasses import asdict
from typing import Any, Mapping, Sequence

from bson import DBRef, ObjectId
from pymongo.asynchronous.collection import AsyncCollection

from domain.entities.post import Post
from domain.repositories.post_repository import BasePostRepository
from infra.gateways.interfaces import DBGateway


class PostRepository(BasePostRepository):
    """Репозиторий для работы с постами."""

    def __init__(
        self,
        gateway: DBGateway,
        collection_name: str,
        categories_collection_name: str,
    ) -> None:
        """Конструктор.

        Args:
            gateway (DBGateway): Гейт подключения к бд
            collection_name (str): Имя коллекции
            categories_collection_name (str): Имя коллекции категорий
        """
        self.__gw = gateway
        self.collection_name = collection_name
        self.categories_collection_name = categories_collection_name

    async def _init_collection(self) -> AsyncCollection:
        return await self.__gw.get_collection(self.collection_name)

    async def add(self, data: Post) -> str:
        """Добавление документа в БД.

        Args:
            data (dict[str, Any]): Документ

        Returns:
            str: ID нового документа
        """
        collection = await self._init_collection()
        dict_data = asdict(data)
        categories = dict_data["categories"]
        if categories:
            linked_categories = []
            for cat in categories:
                linked_categories.append(
                    DBRef(self.categories_collection_name, ObjectId(cat))
                )
            dict_data["categories"] = linked_categories
        result = await collection.insert_one(dict_data)
        return str(result.inserted_id)

    async def get_by_id(self, id: str) -> Post | None:
        """Получение конкретного объекта из БД.

        Args:
            id (str): ID объекта

        Returns:
            dict[str, Any]: Результат поиска
        """
        collection = await self._init_collection()
        try:
            query = {"_id": ObjectId(id)}
        except Exception:
            raise ValueError
        pipeline: Sequence[Mapping[str, Any]] = [
            {"$match": query},
            {
                "$lookup": {
                    "from": self.categories_collection_name,
                    "localField": "categories.$id",
                    "foreignField": "_id",
                    "as": "categories",
                }
            },
        ]

        result_cursor = await collection.aggregate(pipeline)
        result = await result_cursor.to_list(length=1)
        if result:
            return Post.from_raw(result[0])
        return None

    async def get_many(
        self, query: dict[str, Any], limit: int = 10
    ) -> list[dict[str, Any]]:
        """Получение N объектов из БД.

        Args:
            query (dit[str, Any]): Поисковый запрос
            limit (int): Кол-во объектов

        Returns:
            list[dict[str, Any]]: Результат поиска
        """
        collection = await self._init_collection()
        pipeline: Sequence[Mapping[str, Any]] = [
            {"$match": query},
            {
                "$lookup": {
                    "from": self.categories_collection_name,
                    "localField": "categories.$id",
                    "foreignField": "_id",
                    "as": "categories",
                }
            },
            {"$limit": limit},
        ]

        result_cursor = await collection.aggregate(pipeline)
        result = await result_cursor.to_list(length=limit)
        return result

    async def update(self, id: str, update_data: Post) -> Post:
        """Обновление документа.

        Args:
            id (str): ID объекта
            update_data (dict[str, Any]): Данные для обновления

        Returns:
            dict[str, Any]: Обновленный документ
        """
        collection = await self._init_collection()
        data = asdict(update_data)
        data.pop("_id", None)

        try:
            query = {"_id": ObjectId(id)}
        except Exception:
            raise ValueError

        categories = data.get("categories")
        if categories:
            linked_categories = []
            for cat in categories:
                linked_categories.append(
                    {"$ref": self.categories_collection_name, "$id": cat}
                )
            data["categories"] = linked_categories
        result = await collection.find_one_and_update(
            filter=query, update={"$set": data}
        )
        return Post.from_raw(result)

    async def delete(self, id: str) -> bool:
        """Удаление объекта.

        Args:
            id (str): ID объекта

        Returns:
            bool: Результат операции

        Raises:
            ValueError: При неудачной операции
        """
        collection = await self._init_collection()
        try:
            await collection.find_one_and_delete({"_id": ObjectId(id)})
        except Exception as e:
            raise ValueError(e)
        return True
