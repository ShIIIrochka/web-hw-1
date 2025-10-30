# -*- coding: utf-8 -*-

from dataclasses import asdict
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

    async def to_entity(self, include_posts: bool = False) -> CategoryEntity:
        posts = None
        if include_posts:
            await self.fetch_related("posts")
            posts = [asdict(await post.to_entity()) for post in self.posts]
        return CategoryEntity(
            id=self.id,
            name=self.name,
            created_at=self.created_at,
            updated_at=self.updated_at,
            posts=posts,
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

    async def to_entity(self, include_categories: bool = False) -> PostEntity:
        """Перевод из ORM в Entity."""
        await self.fetch_related("author")
        categories = None
        if include_categories:
            await self.fetch_related("categories")
            categories = [
                asdict(await category.to_entity(category))
                for category in self.categories
            ]

        return PostEntity(
            id=self.id,
            title=self.title,
            content=self.content,
            created_at=self.created_at,
            updated_at=self.updated_at,
            author_id=self.author.id,
            categories=categories,
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

    async def to_entity(self, include_posts: bool = False) -> UserEntity:
        """Перевод из ORM в Entity."""
        posts = None
        saved_posts = None

        if include_posts:
            await self.fetch_related("posts", "saved_posts")
            posts = [asdict(await post.to_entity()) for post in self.posts]
            saved_posts = [
                asdict(await post.to_entity()) for post in self.saved_posts
            ]

        return UserEntity(
            id=self.id,
            email=self.email,
            login=self.login,
            password=self.password,
            created_at=self.created_at,
            updated_at=self.updated_at,
            posts=posts,
            saved_posts=saved_posts,
        )
