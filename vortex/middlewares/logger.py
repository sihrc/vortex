import time
from aiohttp.web import middleware

from vortex.logger import Logging


@middleware
async def logger_middleware(request, handler):
    start_time = time.time()

    request.logger = Logging.get("route")
    request.logger.info(
        f"{'[' + request.method + ']':<6} {request.path:<20}{' ' * 10}received"
    )
    response = await handler(request)

    log_str = ""
    log_str += f"{'[' + request.method + ']':<6} {request.path:<20} "
    if request.auth and request.auth.id:
        log_str += f"{'user_id:' + str(request.auth.id):<8} "
    else:
        log_str += f"{'unauth':<8} "
    if response is not None:
        log_str += str(response.status) + " "
    log_str += f"{(time.time() - start_time) * 1000:.3f}ms"

    request.logger.info(log_str)
    return response
