# -*- coding: utf-8 -*-

from __future__ import annotations

import os

from contextlib import asynccontextmanager

from litestar import Litestar
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.spec import Components, SecurityScheme
from litestar.plugins.prometheus import PrometheusConfig, PrometheusController

from src.api.routers import routers
from src.infra.container import container_builder
from src.infra.logging import setup_logging
from src.infra.providers.interfaces import DBProvider
from src.infra.providers.opensearch import OpenSearchClientProvider
from src.middlewares import middlewares


setup_logging(level=os.getenv("LOG_LEVEL", "INFO"))

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


container = container_builder()


@asynccontextmanager
async def lifespan(app: Litestar):
    container = app.state.container
    db_provider = container.resolve(DBProvider)
    opensearch_provider = container.resolve(OpenSearchClientProvider)

    await db_provider.init()
    await opensearch_provider.init()

    yield

    await opensearch_provider.close()
    await db_provider.close()


prometheus_config = PrometheusConfig(
    app_name="blog_api",
    excluded_http_methods=["OPTIONS"],
)

app = Litestar(
    route_handlers=[routers, PrometheusController],
    debug=True,
    dependencies={"container": lambda: container},
    middleware=[*middlewares, prometheus_config.middleware],
    openapi_config=openapi_config,
    lifespan=[lifespan],
)

app.state.container = container

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
