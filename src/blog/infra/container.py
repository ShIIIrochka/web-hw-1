# -*- coding: utf-8 -*2-

from punq import Container

from blog.application.services.auth_service import AuthService
from blog.application.services.user_service import UserService
from blog.infra.config import Config
from blog.infra.gateways.database import MongoGateway
from blog.infra.gateways.interfaces import DBGateway
from blog.infra.providers.interfaces import AuthProvider
from blog.infra.providers.jwt import JWTProvider
from blog.infra.repositories.database_repository import MongoRepository


def container_builder() -> Container:

    container = Container()

    container.register(Config, instance=Config.get_config())

    container.register(AuthProvider, instance=JWTProvider)

    container.register(
        DBGateway,
        instance=MongoGateway(
            uri=container.resolve(Config).db_uri,
            db_name=container.resolve(Config).db_name,
        )
    )

    container.register(
        AuthService,
        factory=lambda: AuthService(
            auth_provider=container.resolve(AuthProvider),
            access_exp=container.resolve(Config).access_exp,
            refresh_exp=container.resolve(Config).refresh_exp,
        )
    )

    container.register(
        "UserRepo",
        factory=lambda: MongoRepository(
            gateway=container.resolve(DBGateway),
            collection_name="users",
        ),
    )

    container.register(
        UserService,
        factory=lambda: UserService(
            repository=container.resolve("UserRepo"),
        )
    )
    return container
