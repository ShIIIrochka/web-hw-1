# -*- coding: utf-8 -*-

from litestar.dto import DataclassDTO, DTOConfig

from blog.domain.entities.user import User


class UserDTO(DataclassDTO[User]):
    """DTO для определения пользователя."""

    config = DTOConfig()
