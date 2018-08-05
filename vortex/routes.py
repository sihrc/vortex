"""
Main interface for creating routes and route hierarchies.
e.g.
RM = RoutesManager(
    base="/api",
    middlewares=(TokenAuthentication, SQLAlchemySession), # Examples of customized middlewares on top of default middlewares applied to the Root Application
    scopes_required=("scope:read", "scope:metadata") # Examples of keyword arguments available in middlewares
)
"""

from functools import wraps, partial

from aiohttp import web

from vortex.middlewares.builtin import attach_middleware_kwargs

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
        self.app = web.Application()
        self.app.middlewares.append(middlewares)
        self.app.update(**middleware_kwargs)

    def route(self, methods, path, route_name=None, middlewares=(), **middleware_kwargs):
        def route_decorator(fn):
            name = route_name or fn.__name__

            handler = partial(
                attach_middleware_kwargs(middleware_kwargs),
                handler=fn
            )

            # Chain middlewares for specific route
            for middleware in middlewares:
                handler = partial(middleware, handler=handler)

            self.app.add_routes([
                getattr(web, method.lower())(path, handler, name=name)
                for method in methods
            ])

            return fn
        return route_decorator
