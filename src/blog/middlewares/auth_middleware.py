# -*- coding: utf -*-

from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.middleware import (
    AbstractAuthenticationMiddleware,
    AuthenticationResult,
    DefineMiddleware,
)

from blog.application.services.auth_service import AuthService
from blog.application.services.user_service import UserService


class AuthMiddleware(AbstractAuthenticationMiddleware):
    """Мидлвеер для авторизации пользователя."""

    async def authenticate_request(
        self, connection: ASGIConnection
    ) -> AuthenticationResult:
        """Авторизуем через реквест."""
        container = connection.app.state.container
        auth_service: AuthService = container.resolve(AuthService)
        user_service: UserService = container.resolve(UserService)

        auth_header = connection.headers.get("Authorization")
        if auth_header:
            token = auth_header.split("Bearer ")[-1]
            try:
                payload = await auth_service.get_payload(token)
                user = await user_service.get_user_by_id(payload.user_id)
            except Exception:
                raise NotAuthorizedException

            return AuthenticationResult(user=user, auth=token)
        else:
            return AuthenticationResult(None, None)


auth_mw = DefineMiddleware(AuthMiddleware, exclude="schema")
middlewares = [auth_mw]
