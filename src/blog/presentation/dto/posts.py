# -*- coding: utf-8 -*-

from dataclasses import dataclass

from litestar.dto import DataclassDTO, DTOConfig

from blog.domain.entities.post import Post


class PostDTO(DataclassDTO[Post]):
    """DTO для поста."""

    config = DTOConfig()


@dataclass
class CreatePostDTO:
    """DTO для создания поста."""

    title: str
    content: str


@dataclass
class UpdatePostDTO:
    """DTO для обновления поста."""

    title: str
    content: str