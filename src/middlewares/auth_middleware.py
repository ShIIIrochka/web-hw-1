# -*- coding: utf -*-

from litestar.connection import ASGIConnection
from litestar.exceptions import NotAuthorizedException
from litestar.middleware import (
    AbstractAuthenticationMiddleware,
    AuthenticationResult,
    DefineMiddleware,
)

from src.application.services.auth_service import AuthService
from src.application.services.user_service import UserService


class AuthMiddleware(AbstractAuthenticationMiddleware):
    """Мидлвеер для авторизации пользователя."""

    async def authenticate_request(
        self, connection: ASGIConnection
    ) -> AuthenticationResult:
        """Авторизуем через реквест."""
        container = connection.app.state.container
        auth_service: AuthService = container.resolve(AuthService)
        user_service: UserService = container.resolve(UserService)

        token = None

        # Try to get token from Authorization header first (for OpenAPI/BearerAuth compatibility)
        auth_header = connection.headers.get("Authorization")
        if auth_header:
            token = auth_header.split("Bearer ")[-1]
        # Fall back to access_token cookie
        elif "access_token" in connection.cookies:
            token = connection.cookies.get("access_token")

        if token:
            try:
                payload = await auth_service.get_payload(token)
                user = await user_service.get_user_by_id(payload.user_id)
                return AuthenticationResult(user=user, auth=token)
            except Exception:
                raise NotAuthorizedException

        return AuthenticationResult(None, None)


auth_mw = DefineMiddleware(AuthMiddleware, exclude="schema")
