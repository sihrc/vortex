"""
Main interface for creating routes and route hierarchies.
e.g.
RM = RoutesManager(
    base="/api",
    middlewares=(TokenAuthentication, SQLAlchemySession), # Examples of customized middlewares on top of default middlewares applied to the Root Application
    scopes_required=("scope:read", "scope:metadata") # Examples of keyword arguments available in middlewares
)
"""

from functools import wraps
from aiohttp.web import RouteTableDef

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
        self.middleware_kwargs = middleware_kwargs
        self.middlewares = middlewares


    def route(self, methods, path, middlewares=(), **middleware_kwargs):
        @wraps
        def handler(fn):
            return fn

        for method in methods:
            # aiohttp web will consolidate multiple methods
            self._add_route(method, path, middlewares, middleware_kwargs)

        return handler


    def _add_route(self, method, path, middlewares, middleware_kwargs):
        raise NotImplementedError()
