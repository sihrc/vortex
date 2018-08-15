"""
Builtin Middleware for Vortex.
Allows modifying the request / response objects with customizable data for use in other custom middlewares
"""
import warnings
from aiohttp.web import middleware

def attach_middleware_to_request_kwargs(request_kwargs):
    @middleware
    async def route_kwargs_middleware(request, handler):
        request.middleware_configs = request_kwargs
        response = await handler(request)
        return response
    return route_kwargs_middleware


def attach_middleware_to_response_kwargs(request_kwargs):
    @middleware
    async def route_kwargs_middleware(request, handler):
        response = await handler(request)
        response.middleware_configs = request_kwargs
        return response
    return route_kwargs_middleware
