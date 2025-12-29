# -*- coding: utf-8 -*-

from dataclasses import dataclass


@dataclass
class CommentNotFoundError(Exception):
    """Исключение, возникающее при отсутствии комментария."""

    message: str | Exception = "Comment not found"


@dataclass
class CommentPermissionError(Exception):
    """Исключение, возникающее при отсутствии прав на действие с комментарием."""

    message: str | Exception = (
        "You do not have permission to perform this action on the comment"
    )
