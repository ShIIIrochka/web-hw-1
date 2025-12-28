# -*- coding: utf-8 -*-

from __future__ import annotations

from litestar.dto import DTOConfig, DataclassDTO

from src.domain.entities.comment import Comment


class CommentDTO(DataclassDTO[Comment]):
    """DTO для комментария."""

    config = DTOConfig()


class CreateCommentDTO(DataclassDTO[Comment]):
    """DTO для создания комментария."""

    config = DTOConfig(include={"content"})


class UpdateCommentDTO(DataclassDTO[Comment]):
    """DTO для обновления комментария."""

    config = DTOConfig(include={"content"})
