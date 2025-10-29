# -*- coding: utf-8 -*-


from litestar.dto import DTOConfig, DataclassDTO

from src.domain.entities.post import Post


class PostDTO(DataclassDTO[Post]):
    """DTO для поста."""

    config = DTOConfig(underscore_fields_private=True)


class CreatePostDTO(DataclassDTO[Post]):
    """DTO для создания поста."""

    config = DTOConfig(include={"title", "content", "category_ids"})


class UpdatePostDTO(DataclassDTO[Post]):
    """DTO для обновления поста."""

    config = DTOConfig(include={"title", "content", "category_ids"})
