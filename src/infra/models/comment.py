# -*- coding: utf-8 -*-

from datetime import datetime

from tortoise import fields, models

from src.infra.models.post import Post


class Comment(models.Model):
    id = fields.UUIDField(pk=True)
    content = fields.TextField()
    created_at = fields.DatetimeField(default=datetime.now)
    updated_at = fields.DatetimeField(default=datetime.now)
    post: fields.ForeignKeyRelation[Post] = fields.ForeignKeyField(
        "models.Post", related_name="comments"
    )
    author: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(  # noqa
        "models.User", related_name="comments"
    )
