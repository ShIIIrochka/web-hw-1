# -*- coding: utf-8 -*-

from __future__ import annotations

from litestar.dto import DTOConfig, DataclassDTO

from src.domain.value_objects.cursor import Page


class PaginatedResponseDTO(DataclassDTO[Page]):
    config = DTOConfig()
