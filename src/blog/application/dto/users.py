# -*- coding: utf-8 -*-

from litestar.dto import DataclassDTO, DTOConfig

from blog.domain.entities.user import User


class UserDTO(DataclassDTO[User]):
    """DTO для определения пользователя."""

    config = DTOConfig()


class CreateUserDTO(DataclassDTO[User]):
    """DTO для создания пользователя."""

    config = DTOConfig(exclude={"updated_at", "created_at", "_id"})


class UpdateUserDTO(DataclassDTO[User]):
    """DTO для обновления пользователя."""

    config = DTOConfig(exclude={"updated_at", "created_at", "_id"})
