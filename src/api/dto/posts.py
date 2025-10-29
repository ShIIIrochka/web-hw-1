# -*- coding: utf-8 -*-

from dataclasses import dataclass

from litestar.dto import DTOConfig, DataclassDTO

from src.domain.entities.post import Post


class PostDTO(DataclassDTO[Post]):
    """DTO для поста."""

    config = DTOConfig(underscore_fields_private=True)


@dataclass
class CreatePostDTO:
    """DTO для создания поста."""

    title: str
    content: str
    categories: list[str]


@dataclass
class UpdatePostDTO:
    """DTO для обновления поста."""

    title: str
    content: str
