# -*- coding: utf-8 -*-

from dataclasses import dataclass

from litestar.dto import DTOConfig, DataclassDTO

from src.domain.entities.user import User


class UserDTO(DataclassDTO[User]):
    """DTO для определения пользователя."""

    config = DTOConfig()


class CreateUserDTO(DataclassDTO[User]):
    """DTO для создания пользователя."""

    config = DTOConfig(exclude={"updated_at", "created_at", "_id"})


@dataclass
class UpdateUserDTO:
    """DTO для обновления пользователя."""

    email: str
    login: str


@dataclass
class LoginUserDTO:
    """DTO для логина пользователя."""

    email: str
    password: str
