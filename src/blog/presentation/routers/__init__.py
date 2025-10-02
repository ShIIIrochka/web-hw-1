# -*- coding: utf-8 -*-

from litestar import Router

from blog.presentation.routers.auth import AuthController
from blog.presentation.routers.users import UserController

routers = Router(path="/", route_handlers=[UserController, AuthController])
