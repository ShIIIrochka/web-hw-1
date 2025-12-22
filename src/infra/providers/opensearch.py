# -*- coding: utf-8 -*-

from __future__ import annotations

from urllib.parse import urlparse

from opensearchpy import AsyncOpenSearch


class OpenSearchClientProvider:
    """Провайдер для OpenSearch клиента (инфраструктура)."""

    def __init__(
        self,
        uri: str,
    ) -> None:
        """Инициализация OpenSearch клиента.

        Args:
            uri: Host подключения к OpenSearch
        """
        parsed = urlparse(uri)
        self.host = parsed.hostname
        self.port = parsed.port
        self.username = parsed.username
        self.password = parsed.password
        self.doc_index = parsed.path.lstrip("/")
        if parsed.scheme == "https":
            self.use_ssl = True
        else:
            self.use_ssl = False
        self._client: AsyncOpenSearch = self._init_client()

    def _init_client(self) -> AsyncOpenSearch:
        """Создание клиента OpenSearch."""
        auth = None
        if self.username and self.password:
            auth = (self.username, self.password)

        return AsyncOpenSearch(
            hosts=[{"host": self.host, "port": self.port}],
            http_auth=auth,
            use_ssl=self.use_ssl,
            verify_certs=False,
        )

    async def init(self) -> None:
        """Инициализация подключения к OpenSearch."""
        await self._ensure_index()

    async def close(self) -> None:
        """Закрытие подключения."""
        await self._client.close()

    async def _ensure_index(self) -> None:
        """Создание индекса если его нет."""
        exists = await self._client.indices.exists(index=self.doc_index)
        if not exists:
            await self._client.indices.create(
                index=self.doc_index,
                body={
                    "mappings": {
                        "properties": {
                            "id": {"type": "keyword"},
                            "title": {
                                "type": "text",
                                "analyzer": "standard",
                            },
                            "content": {
                                "type": "text",
                                "analyzer": "standard",
                            },
                            "author_id": {"type": "keyword"},
                            "created_at": {"type": "date"},
                            "updated_at": {"type": "date"},
                        }
                    },
                },
            )

    async def search(self, body: dict) -> dict:
        """Выполнение поискового запроса.

        Args:
            body: Тело поискового запроса

        Returns:
            Результат поиска
        """
        return await self._client.search(index=self.doc_index, body=body)

    async def index(self, id: str, body: dict) -> None:
        """Индексация документа.

        Args:
            id: Идентификатор документа
            body: Тело документа для индексацииs
        """
        await self._client.index(
            index=self.doc_index,
            id=id,
            body=body,
            refresh=True,
        )

    async def update(self, id: str, body: dict) -> None:
        """Обновление документа в индексе.

        Args:
        """
        await self._client.update(
            index=self.doc_index,
            id=id,
            body={"doc": body},
            refresh=True,
        )

    async def delete(self, id: str) -> None:
        """Удаление документа из индекса.

        Args:
            id: Идентификатор документа
        """
        await self._client.delete(
            index=self.doc_index,
            id=id,
            refresh=True,
        )

    async def bulk(self, body: list[dict]) -> None:
        """Массовая индексация документов.

        Args:
            body: Список документов для индексации
        """
        await self._client.bulk(
            index=self.doc_index,
            body=body,
            refresh=True,
        )
