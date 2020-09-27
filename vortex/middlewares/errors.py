from aiohttp.web import HTTPException, json_response, middleware

from vortex.errors import UnhandledException, VortexException
from vortex.logger import Logging

LOGGER = Logging.get("middleware.error")


@middleware
async def error_middleware(request, handler):
    try:
        return await handler(request)
    except VortexException as exc:
        LOGGER.debug(exc.message, exc_info=True)
        return json_response(exc.to_dict(), status=exc.code)
    except HTTPException as exc:
        if exc.status >= 500:
            LOGGER.exception("5xx http exception")
        else:
            LOGGER.debug(exc.reason, exc_info=True)
        return json_response(
            {"code": exc.status, "message": exc.reason}, status=exc.status
        )
    except Exception:
        LOGGER.exception("Unhandled error in route/middlewares")
        error = UnhandledException()
        return json_response(error.to_dict(), status=error.code)
