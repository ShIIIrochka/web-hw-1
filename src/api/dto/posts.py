# -*- coding: utf-8 -*-


from __future__ import annotations

from litestar.dto import DTOConfig, DataclassDTO

from src.domain.entities.post import Post


class PostDTO(DataclassDTO[Post]):
    """DTO для поста."""

    config = DTOConfig()


class CreatePostDTO(DataclassDTO[Post]):
    """DTO для создания поста."""

    config = DTOConfig(include={"title", "content", "categories"})


class UpdatePostDTO(DataclassDTO[Post]):
    """DTO для обновления поста."""

    config = DTOConfig(include={"title", "content", "categories"})
