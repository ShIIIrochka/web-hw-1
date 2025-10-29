# -*- coding: utf-8 -*-
from dataclasses import asdict

from bson import ObjectId
from bson.errors import InvalidId

from domain.entities.post import Post
from domain.entities.user import User
from domain.repositories.user_repository import BaseUserRepository
from infra.gateways.interfaces import DBGateway


class UserRepository(BaseUserRepository):
    """Реализация репозитория для работы с пользователями."""

    def __init__(self, gateway: DBGateway, collection_name: str) -> None:
        """Конструктор.

        Args:
            gateway (DBGateway): Гейт подключения к бд
            collection_name (str): Имя коллекции
        """
        self.__gw = gateway
        self.collection_name = collection_name

    async def _init_collection(self):
        return await self.__gw.get_collection(self.collection_name)

    async def add(self, data: User) -> str:
        """Добавление нового пользователя.

        Args:
            data (User): Данные пользователя.

        Returns:
            str: ID нового пользователя.
        """
        collection = await self._init_collection()
        user_dict = asdict(data)
        result = await collection.insert_one(user_dict)
        return str(result.inserted_id)

    async def get_by_id(self, id: str) -> User | None:
        """Получение пользователя по ID.

        Args:
            id (str): ID пользователя.

        Returns:
            User | None: Данные пользователя или None, если не найден.
        """
        collection = await self._init_collection()
        try:
            result = await collection.find_one({"_id": ObjectId(id)})
        except Exception:
            raise ValueError
        if result:
            return User.from_raw(result)
        return None

    async def get_one(self, query: dict) -> Post | None:
        """Получение одного пользователя по запросу.

        Args:
            query (dict): Запрос для поиска пользователя.

        Returns:
            dict | None: Данные пользователя или None, если не найден.
        """
        collection = await self._init_collection()
        result = await collection.find_one(query)
        if result:
            Post.from_raw(result)
        return None

    async def update(self, user_id: str, data: User) -> User:
        """Обновление пользователя.

        Args:
            user_id (str): ID пользователя.
            data (User): Данные для обновления.

        Returns:
            User: Обновленный пользователь.
        """
        collection = await self._init_collection()
        user_dict = asdict(data)
        user_dict.pop("id", None)
        try:
            result = await collection.update_one(
                {"_id": ObjectId(user_id)}, {"$set": user_dict}
            )
        except InvalidId:
            raise ValueError
        return User.from_raw(result)

    async def delete(self, id: str) -> bool:
        """Удаление пользователя по ID.

        Args:
            id (str): ID пользователя.
        """
        collection = await self._init_collection()
        try:
            await collection.delete_one({"_id": ObjectId(id)})
            return True
        except InvalidId:
            raise ValueError
