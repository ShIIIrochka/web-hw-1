# -*- coding: utf-8 -*-

from datetime import datetime

from tortoise import fields, models

from src.domain.entities.user import User as UserEntity
from src.infra.models.post import Post


class User(models.Model):
    id = fields.UUIDField(pk=True)
    email = fields.CharField(max_length=255, unique=True)
    login = fields.CharField(max_length=255)
    password = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(default=datetime.now)
    updated_at = fields.DatetimeField(default=datetime.now)
    is_admin = fields.BooleanField(default=False)
    posts: fields.ReverseRelation["Post"]
    saved_posts: fields.ManyToManyRelation[Post]
    followers: fields.ManyToManyRelation["User"] = fields.ManyToManyField(
        "models.User", related_name="following", through="user_followers"
    )
    liked_categories: fields.ManyToManyRelation["Category"] = (  # noqa
        fields.ManyToManyField(  # noqa
            "models.Category",
            related_name="liked_by",
            through="user_category_likes",
        )
    )
    comments: fields.ReverseRelation["Comment"]  # noqa

    async def to_entity(self) -> UserEntity:
        """Перевод из ORM в Entity."""
        return UserEntity(
            id=self.id,
            email=self.email,
            login=self.login,
            password=self.password,
            is_admin=self.is_admin,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
