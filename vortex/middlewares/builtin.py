"""
Builtin Middleware for Vortex.
Allows modifying the request / response objects with customizable data for use in other custom middlewares
"""
from copy import deepcopy
from aiohttp.web import middleware


class Middleware(object):
    configs: dict


def attach_middleware_to_request_kwargs(request_kwargs=None):
    @middleware
    async def route_kwargs_middleware(request, handler):
        if not hasattr(request, "middleware"):
            request.middleware = Middleware()
            request.middleware.configs = {}
        print("ATTACH HAS RUN")
        request.middleware.configs.update(deepcopy(request_kwargs or {}))
        response = await handler(request)
        return response

    return route_kwargs_middleware
