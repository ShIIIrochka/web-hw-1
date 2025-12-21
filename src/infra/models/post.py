# -*- coding: utf-8 -*-

from datetime import datetime

from tortoise import fields, models

from src.domain.entities.post import Post as PostEntity
from src.infra.models.category import Category


class Post(models.Model):
    id = fields.UUIDField(pk=True)
    title = fields.CharField(max_length=255)
    content = fields.TextField(null=True)
    created_at = fields.DatetimeField(default=datetime.now)
    updated_at = fields.DatetimeField(default=datetime.now)
    categories: fields.ManyToManyRelation[Category]
    author: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(  # noqa
        "models.User", related_name="posts"
    )
    saved_by: fields.ManyToManyRelation["User"] = fields.ManyToManyField(  # noqa
        "models.User", related_name="saved_posts"
    )
    comments: fields.ReverseRelation["Comment"]  # noqa

    async def to_entity(self) -> PostEntity:
        """Перевод из ORM в Entity."""
        await self.fetch_related("author")

        return PostEntity(
            id=self.id,
            title=self.title,
            content=self.content,
            created_at=self.created_at,
            updated_at=self.updated_at,
            author_id=self.author.id,
        )
