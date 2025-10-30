# -*- coding: utf-8 -*-

from __future__ import annotations

from contextlib import asynccontextmanager

from litestar import Litestar
from litestar.di import Provide
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.spec import Components, SecurityScheme
from src.infra.gateways.interfaces import DBGateway
from src.api.routers import routers
from src.infra.container import container_builder
from src.middlewares.auth_middleware import middlewares


openapi_config = OpenAPIConfig(
    title="Blog API",
    version="1.0.0",
    path="/schema",
    components=Components(
        security_schemes={
            "BearerAuth": SecurityScheme(
                type="http",
                scheme="bearer",
                bearer_format="JWT",
            )
        }
    ),
)


@asynccontextmanager
async def lifespan(app: Litestar):
    db_gateway = app.state.container.resolve(DBGateway)
    await db_gateway.init()
    yield
    await db_gateway.close()


app = Litestar(
    route_handlers=[routers],
    debug=True,
    dependencies={"container": Provide(container_builder)},
    middleware=middlewares,
    openapi_config=openapi_config,
    lifespan=[lifespan],
)

app.state.container = container_builder()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
