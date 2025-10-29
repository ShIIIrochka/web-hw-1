# -*- coding: utf-8 -*-

from dataclasses import dataclass

from litestar.dto import DTOConfig, DataclassDTO

from src.domain.entities.user import User


class UserDTO(DataclassDTO[User]):
    """DTO для определения пользователя."""

    config = DTOConfig(underscore_fields_private=False)


class CreateUserDTO(DataclassDTO[User]):
    """DTO для создания пользователя."""

    config = DTOConfig(exclude={"updated_at", "created_at"})


class UpdateUserDTO(DataclassDTO[User]):
    """DTO для обновления пользователя."""

    config = DTOConfig(include={"email", "login"})


@dataclass
class LoginUserDTO:
    """DTO для логина пользователя."""

    email: str
    password: str
