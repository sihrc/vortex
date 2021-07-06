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

from vortex.middlewares import attach_middleware_to_request_kwargs
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

    default_middlewares = None

    @classmethod
    def register_default_middlewares(cls, middlewares):
        cls.default_middlewares = middlewares

    def __init__(self, route_prefix, middlewares=None, **middleware_kwargs):
        self.route_prefix = route_prefix
        assert (
            route_prefix or not middlewares
        ), "If middlewares are provided, route prefix must not be empty"
        self.middlewares = list(self.default_middlewares or []) + list(
            middlewares or []
        )
        self.base_middleware_kwargs = middleware_kwargs
        self.routes = []

    def register(
        self, app, middlewares
    ):  # Attach Middleware is not working when additional middlewars are specified in RouteManager

        routes = []

        for (method, middleware_kwargs, path, handler, name) in self.routes:
            for middleware in (
                [attach_middleware_to_request_kwargs(middleware_kwargs)]
                + list(middlewares or [])
                + self.middlewares
            )[::-1]:
                handler = _partial(middleware, handler=handler)
            routes.append(getattr(web, method.lower())(path, handler, name=name))

        if self.route_prefix != "" and self.route_prefix != "/":
            subapp = web.Application()
            subapp.add_routes(routes)
            app.add_subapp(self.route_prefix, subapp)
        else:
            app.add_routes(routes)

    def route(self, methods, path, route_name=None, **middleware_kwargs):
        if path.endswith("/"):
            path = path[:-1]

        result_middleware_kwargs = deepcopy(self.base_middleware_kwargs)
        result_middleware_kwargs.update(middleware_kwargs)

        def route_decorator(handler):
            name = route_name or handler.__name__
            handler = type_check(handler)

            self.routes.extend(
                [
                    (method.lower(), result_middleware_kwargs, path, handler, name)
                    for method in methods
                ]
            )

            return handler

        return route_decorator
