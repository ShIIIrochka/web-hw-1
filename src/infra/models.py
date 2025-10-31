# -*- coding: utf-8 -*-

from datetime import datetime

from tortoise import fields, models

from src.domain.entities.category import Category as CategoryEntity
from src.domain.entities.post import Post as PostEntity
from src.domain.entities.user import User as UserEntity


class Category(models.Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=255)
    posts: fields.ManyToManyRelation["Post"] = fields.ManyToManyField(
        "models.Post", related_name="categories", through="post_categories"
    )
    created_at = fields.DatetimeField(default=datetime.now)
    updated_at = fields.DatetimeField(default=datetime.now)

    async def to_entity(self) -> CategoryEntity:
        return CategoryEntity(
            id=self.id,
            name=self.name,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )


class Post(models.Model):
    id = fields.UUIDField(pk=True)
    title = fields.CharField(max_length=255)
    content = fields.TextField(null=True)
    created_at = fields.DatetimeField(default=datetime.now)
    updated_at = fields.DatetimeField(default=datetime.now)
    categories: fields.ManyToManyRelation[Category]
    author: fields.ForeignKeyRelation["User"] = fields.ForeignKeyField(
        "models.User", related_name="posts"
    )
    saved_by: fields.ManyToManyRelation["User"] = fields.ManyToManyField(
        "models.User", related_name="saved_posts"
    )

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


class User(models.Model):
    id = fields.UUIDField(pk=True)
    email = fields.CharField(max_length=255, unique=True)
    login = fields.CharField(max_length=255)
    password = fields.CharField(max_length=255)
    created_at = fields.DatetimeField(default=datetime.now)
    updated_at = fields.DatetimeField(default=datetime.now)
    posts: fields.ReverseRelation["Post"]
    saved_posts: fields.ManyToManyRelation[Post]

    async def to_entity(self) -> UserEntity:
        """Перевод из ORM в Entity."""
        return UserEntity(
            id=self.id,
            email=self.email,
            login=self.login,
            password=self.password,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
