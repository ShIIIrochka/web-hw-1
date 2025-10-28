# -*- coding: utf-8 -*-

from litestar import Litestar
from litestar.di import Provide
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.spec import Components, SecurityScheme

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

app = Litestar(
    route_handlers=[routers],
    debug=True,
    dependencies={"container": Provide(container_builder)},
    middleware=middlewares,
    openapi_config=openapi_config,
)

app.state.container = container_builder()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
