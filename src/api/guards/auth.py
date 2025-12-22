# -*- coding: utf-8 -*-

from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.handlers import BaseRouteHandler


async def auth_guard(connection: ASGIConnection, _: BaseRouteHandler) -> None:
    """Guard для проверки аутентификации пользователя."""
    if not connection.user:
        raise NotAuthorizedException


async def is_admin(connection: ASGIConnection, _: BaseRouteHandler) -> bool:
    """Guard для проверки админ ли пользователь."""
    if connection.user and connection.user.is_admin:
        return True
    return False
