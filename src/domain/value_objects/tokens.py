# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class JWT:
    """Скоуп JWT токенов."""

    access: str
    refresh: str
