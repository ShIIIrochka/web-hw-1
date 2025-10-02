# -*- coding: utf-8 -*-

from litestar import Litestar
from litestar.openapi.config import OpenAPIConfig
from litestar.openapi.spec import Components, SecurityScheme

from blog.infra.container import container_builder
from blog.middlewares.auth_middleware import middlewares
from blog.presentation.routers import routers

openapi_config = OpenAPIConfig(
    title="Blog API",
    version="1.0.0",
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
    dependencies={"container": container_builder},
    middleware=middlewares,
    openapi_config=openapi_config,
)

app.state.container = container_builder()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)