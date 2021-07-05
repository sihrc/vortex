from .logger import logger_middleware
from .headers import headers_middleware
from .errors import error_middleware
from .builtin import attach_middleware_to_request_kwargs

from aiohttp.web import (
    HTTPPermanentRedirect,
    middleware,
    normalize_path_middleware,
)

DEFAULT_MIDDLEWARES = (
    normalize_path_middleware(
        remove_slash=True, append_slash=False, redirect_class=HTTPPermanentRedirect
    ),
    logger_middleware,
    headers_middleware,
    error_middleware,
)

__all__ = [
    "middleware",
    "attach_middleware_to_request_kwargs",
    "logger_middleware",
    "headers_middleware",
    "error_middleware",
]
