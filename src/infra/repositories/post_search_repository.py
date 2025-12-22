# -*- coding: utf-8 -*-

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from src.domain.entities.post import Post
from src.domain.repositories.post_search_repository import (
    BasePostSearchRepository,
)
from src.domain.value_objects.search import PostSearchHit, PostSearchResult
from src.infra.providers.opensearch import OpenSearchClientProvider


class PostSearchRepository(BasePostSearchRepository):
    """Реализация репозитория поиска постов через OpenSearch."""

    def __init__(self, client_provider: OpenSearchClientProvider) -> None:
        """Конструктор.

        Args:
            client_provider: Провайдер OpenSearch клиента
        """
        self._provider = client_provider

    @staticmethod
    def _post_to_document(post: Post) -> dict:
        """Маппинг Post сущности в документ индекса.

        Args:
            post: Сущность поста

        Returns:
            Документ для индексации
        """
        return {
            "id": str(post.id),
            "title": post.title,
            "content": post.content,
            "author_id": str(post.author_id),
            "created_at": post.created_at.isoformat(),
            "updated_at": post.updated_at.isoformat(),
        }

    @staticmethod
    def _parse_hit(hit: dict) -> PostSearchHit:
        """Парсинг hit из ответа OpenSearch в domain модель.

        Args:
            hit: Элемент из hits массива ответа OpenSearch

        Returns:
            PostSearchHit VO
        """
        source = hit["_source"]
        return PostSearchHit(
            post_id=UUID(source["id"]),
            title=source["title"],
            content=source["content"],
            author_id=UUID(source["author_id"]),
            created_at=datetime.fromisoformat(source["created_at"]),
            updated_at=datetime.fromisoformat(source["updated_at"]),
            score=hit["_score"],
            highlight=hit.get("highlight", {}),
        )

    async def search(
        self, query: str, limit: int = 10, offset: int = 0
    ) -> PostSearchResult:
        """Поиск постов по запросу.

        Args:
            query: Поисковый запрос
            limit: Количество результатов
            offset: Смещение для пагинации

        Returns:
            PostSearchResult с результатами поиска
        """

        result = await self._provider.search(
            body={
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["title^2", "content"],
                        "type": "best_fields",
                    }
                },
                "highlight": {
                    "fields": {
                        "title": {},
                        "content": {"fragment_size": 128},
                    }
                },
                "from": offset,
                "size": limit,
                "sort": [{"_score": "desc"}, {"created_at": "desc"}],
            },
        )

        hits_data = result.get("hits", {}).get("hits", [])
        total = result.get("hits", {}).get("total", {}).get("value", 0)

        hits = [self._parse_hit(hit) for hit in hits_data]

        return PostSearchResult(
            hits=hits,
            total=total,
            limit=limit,
            offset=offset,
        )

    async def index(self, post: Post) -> None:
        """Индексация поста.

        Args:
            post: Сущность поста для индексации
        """
        document = self._post_to_document(post)
        await self._provider.index(
            id=str(post.id),
            body=document,
        )

    async def update(self, post: Post) -> None:
        """Обновление поста в индексе.

        Args:
            post: Сущность поста для обновления
        """

        document = self._post_to_document(post)
        await self._provider.update(
            id=str(post.id),
            body=document,
        )

    async def delete(self, post_id: UUID) -> None:
        """Удаление поста из индекса.

        Args:
            post_id: Идентификатор поста
        """

        await self._provider.delete(
            id=str(post_id),
        )

    async def bulk_index(self, posts: list[Post]) -> None:
        """Массовая индексация постов.

        Args:
            posts: Список постов для индексации
        """
        if not posts:
            return

        bulk_body = []
        for post in posts:
            bulk_body.append({"index": {"_id": str(post.id)}})
            bulk_body.append(self._post_to_document(post))

        await self._provider.bulk(body=bulk_body)
