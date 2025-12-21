# -*- coding: utf-8 -*2-

from __future__ import annotations

import os

from dataclasses import dataclass


@dataclass
class Config:
    debug: bool
    db_uri: str
    secret_key: str
    access_exp: int = 15 * 60
    refresh_exp: int = 7 * 24 * 60 * 60

    @classmethod
    def get_config(cls) -> Config:
        debug = os.getenv("DEBUG", "False") == "True"
        db_uri = os.getenv("DB_URI")
        if not db_uri:
            raise RuntimeError("DB_URI environment variable is not set")
        return cls(
            debug=debug,
            db_uri=db_uri,
            secret_key=os.getenv("SECRET_KEY", "test"),
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
