# -*- coding: utf-8 -*2-

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Config:
    debug: bool
    db_uri: str
    db_name: str
    secret_key: str
    access_exp: int = 15 * 60
    refresh_exp: int = 7 * 24 * 60 * 60

    @classmethod
    def get_config(cls) -> Config:
        debug = os.getenv("DEBUG", "False") == "True"
        return cls(
            debug=debug,
            db_uri=os.getenv("DB_URI"),
            db_name=os.getenv("DB_NAME"),
            secret_key=os.getenv("SECRET_KEY"),
        )
