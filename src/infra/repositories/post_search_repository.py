# -*- coding: utf-8 -*-

from __future__ import annotations

from uuid import UUID

from src.domain.entities.post import Post
from src.domain.repositories.post_search_repository import (
    BasePostSearchRepository,
)
from src.infra.providers.opensearch import OpenSearchClientProvider


class PostSearchRepository(BasePostSearchRepository):
    """Реализация репозитория поиска постов через OpenSearch."""

    def __init__(self, client_provider: OpenSearchClientProvider) -> None:
        """Конструктор.

        Args:
            client_provider: Провайдер OpenSearch клиента
        """
        self._provider = client_provider

    async def search(
        self, query: str, limit: int = 10, offset: int = 0
    ) -> list[Post]:
        """Поиск постов по запросу.

        Args:
            query (str): Поисковый запрос
            limit (int): Количество результатов
            offset (int): Смещение для пагинации

        Returns:
            list[Post]: Результат поиска
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
                "from": offset,
                "size": limit,
                "sort": [{"_score": "desc"}, {"created_at": "desc"}],
            },
        )

        hits_data = result.get("hits", {}).get("hits", [])
        return [Post.from_row(hit) for hit in hits_data]

    async def index(self, post: Post) -> None:
        """Индексация поста.

        Args:
            post (Post): Сущность поста для индексации
        """
        await self._provider.index(
            id=str(post.id),
            body=post.to_row(),
        )

    async def update(self, post: Post) -> None:
        """Обновление поста в индексе.

        Args:
            post: Сущность поста для обновления
        """

        await self._provider.update(
            id=str(post.id),
            body=post.to_row(),
        )

    async def delete(self, post_id: UUID) -> None:
        """Удаление поста из индекса.

        Args:
            post_id: Идентификатор поста
        """

        await self._provider.delete(
            id=str(post_id),
        )

    async def feed(
        self,
        liked_categories: list[UUID],
        saved_categories: list[UUID],
        limit: int = 10,
        cursor: UUID | None = None,
    ) -> list[Post]:
        sort_clause = [
            {"_score": {"order": "desc"}},
            {"created_at": {"order": "desc"}},
            {"id": {"order": "desc"}},
        ]

        body: dict = {
            "size": limit,
            "sort": sort_clause,
        }

        if cursor:
            body["search_after"] = str(cursor)

        if not liked_categories and not saved_categories:
            body["query"] = {"match_all": {}}
        else:
            should_clauses = []

            for cat_id in liked_categories:
                should_clauses.append(
                    {
                        "term": {
                            "categories": {
                                "value": str(cat_id),
                                "boost": 2.0,
                            }
                        }
                    }
                )

            for cat_id in saved_categories:
                if cat_id not in liked_categories:
                    should_clauses.append(
                        {
                            "term": {
                                "categories": {
                                    "value": str(cat_id),
                                    "boost": 1.0,
                                }
                            }
                        }
                    )

            body["query"] = {
                "bool": {
                    "should": should_clauses,
                    "minimum_should_match": 1,
                }
            }

        result = await self._provider.search(body=body)
        hits_data = result.get("hits", {}).get("hits", [])

        return [Post.from_row(hit) for hit in hits_data]
