# -*- coding: utf-8 -*-

from datetime import datetime

from tortoise import fields, models

from src.domain.entities.comment import Comment as CommentEntity
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
    parent_comment: fields.ForeignKeyNullableRelation["Comment"] = (
        fields.ForeignKeyField(
            "models.Comment",
            related_name="replies",
            null=True,
        )
    )
    replies: fields.ReverseRelation["Comment"]  # noqa

    async def to_entity(self) -> CommentEntity:
        """Перевод из ORM в Entity."""
        await self.fetch_related("author", "post")

        return CommentEntity(
            id=self.id,
            content=self.content,
            post_id=self.post.id,
            author_id=self.author.id,
            parent_comment_id=self.parent_comment_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
