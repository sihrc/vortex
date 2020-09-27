import os
from distutils.util import strtobool
from urllib.parse import urlparse

from aiohttp.web import Response, middleware

ALLOWED_ORIGINS = os.getenv("VORTEX_ALLOWED_ORIGINS")
DISABLE_ORIGIN_CHECK = strtobool(os.getenv("VORTEX_DISABLE_ORIGIN_CHECK", "False"))


ACCEPT = [
    "text/html",
    "application/xhtml+xml",
    "application/xml",
    "application/json;q=0.9",
    "*/*;q=0.8",
]


@middleware
async def headers_middleware(request, handler):
    origin = request.headers.get("Origin")
    if origin is not None:
        parsed = urlparse(origin)
        request.domain = parsed.hostname

    if request.method != "OPTIONS":
        response = await handler(request)
    else:
        response = Response()

    if DISABLE_ORIGIN_CHECK or getattr(request, "domain", "").endswith(ALLOWED_ORIGINS):
        response.headers["Access-Control-Allow-Origin"] = origin

    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers[
        "Access-Control-Allow-Headers"
    ] = "Origin, X-Requested-With, Content-Type, Accept, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS, DELETE, PUT"
    response.headers["Accept"] = ",".join(ACCEPT)
    response.headers["Accept-Language"] = "en-us,en;q=0.5"
    response.headers["Accept-Encoding"] = "gzip,deflate"
    response.headers["Accept-Charset"] = "ISO-8859-1,utf-8;q=0.7,*;q=0.7"

    return response
