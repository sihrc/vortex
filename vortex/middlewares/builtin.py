"""
Builtin Middleware for Vortex.
Allows modifying the request / response objects with customizable data for use in other custom middlewares
"""
import logging
from copy import deepcopy
from aiohttp.web import middleware as aiohttp_middleware

middleware_logger = logging.getLogger("vortex.middlewares")


class Middleware(object):
    configs: dict


def middleware(fn):
    fn = aiohttp_middleware(fn)

    async def wrapped(request, handler):
        middleware_logger.debug(f"Running {fn.__name__} middleware")
        return await fn(request, handler)

    return wrapped


def attach_middleware_to_request_kwargs(request_kwargs=None):
    @middleware
    async def route_kwargs_middleware(request, handler):
        if not hasattr(request, "middleware"):
            request.middleware = Middleware()
            request.middleware.configs = {}
        request.middleware.configs.update(deepcopy(request_kwargs or {}))
        response = await handler(request)
        return response

    return route_kwargs_middleware
