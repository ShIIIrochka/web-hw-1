# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class PostNotFoundError(Exception):
    """Исключение, возникающее при отсутствии поста."""

    message: str | Exception = "Post not found"


@dataclass
class PostPermissionError(Exception):
    """Исключение, возникающее при отсутствии прав на действие с постом."""

    message: str | Exception = (
        "You do not have permission to perform this action on the post"
    )
