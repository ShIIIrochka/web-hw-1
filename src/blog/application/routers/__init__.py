# -*- coding: utf-8 -*-

from litestar import Router

from blog.application.routers.auth import AuthController
from blog.application.routers.posts import PostController
from blog.application.routers.users import UserController

routers = Router(
    path="/", route_handlers=[UserController, AuthController, PostController]
)
