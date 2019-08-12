"""
Builtin Middleware for Vortex.
Allows modifying the request / response objects with customizable data for use in other custom middlewares
"""
from copy import deepcopy

from aiohttp.web import middleware


def attach_middleware_to_request_kwargs(request_kwargs):
    @middleware
    async def route_kwargs_middleware(request, handler):
        if not hasattr(request, "middleware_configs"):
            request.middleware_configs = {}
        request.middleware_configs.update(deepcopy(request_kwargs))
        response = await handler(request)
        return response

    return route_kwargs_middleware
