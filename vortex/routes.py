"""
Main interface for creating routes and route hierarchies.
e.g.
RM = RoutesManager(
    base="/api",
    middlewares=(TokenAuthentication, SQLAlchemySession), # Examples of customized middlewares on top of default middlewares applied to the Root Application
    scopes_required=("scope:read", "scope:metadata") # Examples of keyword arguments available in middlewares
)
"""
from functools import wraps, partial as functools_partial
from copy import deepcopy

from aiohttp import web

from vortex.middlewares.builtin import attach_middleware_to_request_kwargs


def _partial(middleware, handler):
    """
    Custom partial in order to propagate original fn attributes
    """
    resulting_func = functools_partial(middleware, handler=handler)
    resulting_func.__name__ = handler.__name__
    resulting_func.__module__ = handler.__module__
    resulting_func.__doc__ = handler.__doc__
    return resulting_func


class RouteManager(object):
    """
    Quick References:
    https://github.com/aio-libs/aiohttp/blob/master/docs/web_quickstart.rst#id47

    Variables in path are formatted as {identifier:regex} using Python Regex language.
    e.g. /api/datasets/{dataset_id:\\d+}

    These are later accessible via request.match_info[identifier]
    """
    def __init__(self, base, middlewares=(), **middleware_kwargs):
        self.base = base
        self.middlewares = [attach_middleware_to_request_kwargs(middleware_kwargs)] + list(middlewares)
        self.base_middleware_kwargs = middleware_kwargs
        self.routes = []
        self.is_subapp = self.base != "" and self.base != "/"


    def register(self, app): # Attach Middleware is not working when additional middlewars are specified in RouteManager
        if self.is_subapp:
            subapp = web.Application(
                middlewares=self.middlewares
            )
            subapp.add_routes(self.routes)
            app.add_subapp(self.base, subapp)
        else:
            app.add_routes(self.routes)


    def route(self, methods, path, route_name=None, middlewares=(), **middleware_kwargs):
        # Chain middlewares for specific route
        if not self.is_subapp:
            middlewares = self.middlewares + list(middlewares)

        if path.endswith("/"):
            path = path[:-1]

        def route_decorator(handler):
            name = route_name or handler.__name__

            result_middleware_kwargs = deepcopy(self.base_middleware_kwargs)
            result_middleware_kwargs.update(middleware_kwargs)

            for middleware in middlewares:
                handler = _partial(middleware, handler=handler)

            handler = _partial(
                attach_middleware_to_request_kwargs(result_middleware_kwargs),
                handler=handler
            )

            self.routes.extend([
                getattr(web, method.lower())(path, handler, name=name)
                for method in methods
            ])

            return handler
        return route_decorator
