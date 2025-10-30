# -*- coding: utf-8 -*2-

from jam.aio import Jam
from punq import Container

from application.services.category_service import CategoryService
from infra.gateways.database import PostgresGateway
from infra.repositories.category_repository import CategoryRepository
from infra.repositories.post_repository import PostRepository
from infra.repositories.user_repository import UserRepository
from src.application.services.auth_service import AuthService
from src.application.services.post_service import PostService
from src.application.services.user_service import UserService
from src.infra.config import Config
from src.infra.gateways.interfaces import DBGateway
from src.infra.providers.interfaces import AuthProvider
from src.infra.providers.jwt import JWTProvider


def container_builder() -> Container:
    container = Container()

    container.register(Config, instance=Config.get_config())

    container.register(
        Jam,
        instance=Jam(
            config={
                "auth_type": "jwt",
                "secret_key": (container.resolve(Config)).secret_key,
            }
        ),
    )

    container.register(
        AuthProvider, instance=JWTProvider(jam_instance=container.resolve(Jam))
    )

    container.register(
        DBGateway,
        instance=PostgresGateway(
            uri=container.resolve(Config).db_uri,
            modules={"models": ["src.nfra.models"]},
        ),
    )

    container.register(
        AuthService,
        factory=lambda: AuthService(
            auth_provider=container.resolve(AuthProvider),
            access_exp=container.resolve(Config).access_exp,
            refresh_exp=container.resolve(Config).refresh_exp,
        ),
    )

    container.register(
        "UserRepo",
        factory=lambda: UserRepository(),
    )

    container.register(
        UserService,
        factory=lambda: UserService(
            repository=container.resolve("UserRepo"),
        ),
    )

    container.register(
        "PostRepo",
        factory=lambda: PostRepository(),
    )

    container.register(
        PostService,
        factory=lambda: PostService(
            repository=container.resolve("PostRepo"),
        ),
    )

    container.register(
        "CategoryRepo",
        factory=lambda: CategoryRepository(),
    )

    container.register(
        CategoryService,
        factory=lambda: CategoryService(
            repository=container.resolve("CategoryRepo"),
        ),
    )
    return container
