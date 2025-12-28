# -*- coding: utf-8 -*-

from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.handlers import BaseRouteHandler


async def auth_guard(connection: ASGIConnection, _: BaseRouteHandler) -> None:
    """Guard для проверки аутентификации пользователя."""
    if not connection.user:
        raise NotAuthorizedException
