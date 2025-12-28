# -*- coding: utf-8 -*-

from litestar import Router

from src.api.routers.auth import AuthController
from src.api.routers.categories import CategoryController
from src.api.routers.comments import CommentController
from src.api.routers.posts import PostController
from src.api.routers.users import UserController


routers = Router(
    path="/",
    route_handlers=[
        UserController,
        AuthController,
        PostController,
        CategoryController,
        CommentController,
    ],
)
