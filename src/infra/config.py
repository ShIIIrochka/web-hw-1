# -*- coding: utf-8 -*-

from __future__ import annotations

import os

from dataclasses import dataclass


@dataclass
class Config:
    debug: bool
    db_uri: str
    secret_key: str
    opensearch_uri: str
    redis_uri: str
    cache_ttl_seconds: int = 60
    search_cache_popularity_threshold: int = 10
    search_cache_ttl_seconds: int = 300
    access_exp: int = 15 * 60
    refresh_exp: int = 7 * 24 * 60 * 60

    @classmethod
    def get_config(cls) -> Config:
        debug = os.getenv("DEBUG", "False") == "True"
        db_uri = os.getenv("DB_URI")
        redis_uri = os.getenv("REDIS_URI")
        elastic_uri = os.getenv("OPENSEARCH_URI")

        if not db_uri or not redis_uri or not elastic_uri:
            raise RuntimeError("Missing required environment variables")
        return cls(
            debug=debug,
            db_uri=db_uri,
            secret_key=os.getenv("SECRET_KEY", "test"),
            redis_uri=redis_uri,
            cache_ttl_seconds=int(os.getenv("CACHE_TTL_SECONDS", "60")),
            search_cache_popularity_threshold=int(
                os.getenv("CACHE_POPULARITY_THRESHOLD", "10")
            ),
            opensearch_uri=elastic_uri,
        )


TORTOISE_ORM = {
    "connections": {"default": os.getenv("DB_URI")},
    "apps": {
        "models": {
            "models": ["src.infra.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
