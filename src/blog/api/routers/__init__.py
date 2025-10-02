# -*- coding: utf-8 -*-

from litestar import Router

from blog.api.routers.auth import AuthController
from blog.api.routers.posts import PostController
from blog.api.routers.users import UserController

routers = Router(
    path="/", route_handlers=[UserController, AuthController, PostController]
)
