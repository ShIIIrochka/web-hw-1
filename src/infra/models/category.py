# -*- coding: utf-8 -*-

from datetime import datetime

from tortoise import fields, models

from src.domain.entities.category import Category as CategoryEntity


class Category(models.Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=255)
    posts: fields.ManyToManyRelation["Post"] = fields.ManyToManyField(  # noqa
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
