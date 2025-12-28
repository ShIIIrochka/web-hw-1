# -*- coding: utf-8 -*-

from litestar.connection import ASGIConnection
from litestar.handlers import BaseRouteHandler


async def is_admin(connection: ASGIConnection, _: BaseRouteHandler) -> bool:
    """Guard для проверки админ ли пользователь."""
    if connection.user and connection.user.is_admin:
        return True
    return False
