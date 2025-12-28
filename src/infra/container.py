# -*- coding: utf-8 -*-

from __future__ import annotations

from jam.aio import Jam
from punq import Container

from src.application.services.auth_service import AuthService
from src.application.services.category_service import CategoryService
from src.application.services.comment_service import CommentService
from src.application.services.post_search_service import PostSearchService
from src.application.services.post_service import PostService
from src.application.services.user_service import UserService
from src.infra.config import Config
from src.infra.providers.cache import RedisCacheProvider
from src.infra.providers.database import PostgresProvider
from src.infra.providers.interfaces import (
    AuthProvider,
    CacheProvider,
    DBProvider,
)
from src.infra.providers.jwt import JWTProvider
from src.infra.providers.opensearch import OpenSearchClientProvider
from src.infra.repositories.category_repository import CategoryRepository
from src.infra.repositories.comment_repository import CommentRepository
from src.infra.repositories.post_repository import PostRepository
from src.infra.repositories.post_search_repository import (
    PostSearchRepository,
)
from src.infra.repositories.user_repository import UserRepository


def container_builder() -> Container:
    """Сборка DI-контейнера приложения."""
    container = Container()

    config = Config.get_config()
    container.register(Config, instance=config)

    container.register(
        Jam,
        instance=Jam(
            config={
                "auth_type": "jwt",
                "secret_key": config.secret_key,
            }
        ),
    )

    container.register(
        AuthProvider, instance=JWTProvider(jam_instance=container.resolve(Jam))
    )

    container.register(
        DBProvider,
        instance=PostgresProvider(
            uri=config.db_uri,
            modules={"models": ["src.infra.models"]},
        ),
    )

    container.register(
        CacheProvider,
        instance=RedisCacheProvider(
            uri=config.redis_uri,
            default_ttl=config.cache_ttl_seconds,
        ),
    )

    opensearch_client_provider = OpenSearchClientProvider(
        uri=config.opensearch_uri
    )
    container.register(
        OpenSearchClientProvider, instance=opensearch_client_provider
    )

    container.register(
        "SearchRepo",
        factory=lambda: PostSearchRepository(
            client_provider=opensearch_client_provider
        ),
    )

    container.register("UserRepo", factory=lambda: UserRepository())
    container.register("PostRepo", factory=lambda: PostRepository())
    container.register("CategoryRepo", factory=lambda: CategoryRepository())
    container.register("CommentRepo", factory=lambda: CommentRepository())

    container.register(
        AuthService,
        factory=lambda: AuthService(
            auth_provider=container.resolve(AuthProvider),
            access_exp=config.access_exp,
            refresh_exp=config.refresh_exp,
        ),
    )

    container.register(
        UserService,
        factory=lambda: UserService(
            repository=container.resolve("UserRepo"),
            search_repository=container.resolve("SearchRepo"),
        ),
    )

    container.register(
        CategoryService,
        factory=lambda: CategoryService(
            repository=container.resolve("CategoryRepo"),
        ),
    )

    container.register(
        PostService,
        factory=lambda: PostService(
            repository=container.resolve("PostRepo"),
            search_repository=container.resolve("SearchRepo"),
            cache_provider=container.resolve(CacheProvider),
        ),
    )

    container.register(
        PostSearchService,
        factory=lambda: PostSearchService(
            search_repository=container.resolve("SearchRepo"),
            cache_provider=container.resolve(CacheProvider),
            popularity_threshold=config.search_cache_popularity_threshold,
            cache_ttl=config.search_cache_ttl_seconds,
        ),
    )

    container.register(
        CommentService,
        factory=lambda: CommentService(
            comment_repository=container.resolve("CommentRepo"),
            post_repository=container.resolve("PostRepo"),
        ),
    )

    return container
