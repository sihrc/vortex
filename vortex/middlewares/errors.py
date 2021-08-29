from aiohttp.web import HTTPException, json_response, HTTPFound

from vortex.errors import UnhandledException, VortexException
from vortex.middlewares import middleware

UNHANDLED = json_response(UnhandledException().to_dict(), status=500)


@middleware
async def error_middleware(request, handler):
    response = UNHANDLED
    try:
        try:
            response = await handler(request)
        except VortexException as exc:
            request.logger.debug(exc.message, exc_info=True)
            response = json_response(exc.to_dict(), status=exc.code)
        except HTTPException as exc:
            if exc.status >= 500:
                request.logger.exception("5xx http exception")
            else:
                request.logger.debug(exc.reason, exc_info=True)
            response = json_response(
                {"code": exc.status, "message": exc.reason}, status=exc.status
            )
    except Exception:
        request.logger.exception("Unhandled Error")
    finally:
        return response
