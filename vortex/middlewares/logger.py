from aiohttp.web import middleware

from vortex.logger import Logging

REQUEST_LOGGER = Logging.get("server.route")


@middleware
async def logger_middleware(request, handler):
    REQUEST_LOGGER.info(f"{request.method} {request.path}")
    response = await handler(request)
    REQUEST_LOGGER.info(f"{request.method} {request.path} {response.status}")

    return response
