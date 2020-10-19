"""
Main interface for creating routes and route hierarchies.
e.g.
RM = RoutesManager(
    base="/api",
    middlewares=(TokenAuthentication, SQLAlchemySession), # Examples of customized middlewares on top of default middlewares applied to the Root Application
    scopes_required=("scope:read", "scope:metadata") # Examples of keyword arguments available in middlewares
)
"""
from copy import deepcopy

from aiohttp import web

from vortex.middlewares.builtin import attach_middleware_to_request_kwargs
from vortex.typing import type_check


def _partial(middleware, handler):
    """
    Custom partial in order to propagate original fn attributes
    """

    async def partial(request):
        response = await middleware(request, handler=handler)
        return response

    partial.__name__ = handler.__name__
    partial.__module__ = handler.__module__
    partial.__doc__ = handler.__doc__
    return partial


class RouteManager(object):
    """
    Quick References:
    https://github.com/aio-libs/aiohttp/blob/master/docs/web_quickstart.rst#id47

    Variables in path are formatted as {identifier:regex} using Python Regex language.
    e.g. /api/datasets/{dataset_id:\\d+}

    These are later accessible via request.match_info[identifier]
    """

    middlewares = []

    @classmethod
    def register_default_middlewares(cls, middlewares):
        cls.middlewares = middlewares

    def __init__(self, base, middlewares=None, **middleware_kwargs):
        self.base = base
        self.middlewares = middlewares if middlewares is not None else self.middlewares
        self.middlewares = list(self.middlewares)
        self.base_middleware_kwargs = middleware_kwargs
        self.routes = []

    def register(
        self, app
    ):  # Attach Middleware is not working when additional middlewars are specified in RouteManager
        if self.base != "" and self.base != "/":
            subapp = web.Application()
            subapp.add_routes(self.routes)
            app.add_subapp(self.base, subapp)
        else:
            app.add_routes(self.routes)

    def route(
        self, methods, path, route_name=None, middlewares=(), **middleware_kwargs
    ):
        # Chain middlewares for specific route
        middlewares = self.middlewares + list(middlewares)
        if path.endswith("/"):
            path = path[:-1]

        result_middleware_kwargs = deepcopy(self.base_middleware_kwargs)
        result_middleware_kwargs.update(middleware_kwargs)
        middlewares.append(attach_middleware_to_request_kwargs(middleware_kwargs))

        def route_decorator(handler):
            name = route_name or handler.__name__
            handler = type_check(handler)

            for middleware in middlewares:
                handler = _partial(middleware, handler=handler)

            self.routes.extend(
                [
                    getattr(web, method.lower())(path, handler, name=name)
                    for method in methods
                ]
            )

            return handler

        return route_decorator
