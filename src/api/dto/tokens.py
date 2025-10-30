# -*- coding: utf-8 -*-

from __future__ import annotations

from litestar.dto import DTOConfig, DataclassDTO

from src.domain.value_objects.tokens import JWT


class JWTTokens(DataclassDTO[JWT]):
    """DTO представления JWT токенов."""

    config = DTOConfig()
