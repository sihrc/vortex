from aiohttp.web import HTTPPermanentRedirect, middleware, normalize_path_middleware

from .builtin import attach_middleware_to_request_kwargs
from .errors import error_middleware
from .headers import headers_middleware
from .logger import logger_middleware

DEFAULT_MIDDLEWARES = (
    normalize_path_middleware(
        remove_slash=True, append_slash=False, redirect_class=HTTPPermanentRedirect
    ),
    logger_middleware,
    error_middleware,
    headers_middleware,
)

__all__ = [
    "attach_middleware_to_request_kwargs",
    "DEFAULT_MIDDLEWARES",
    "error_middleware",
    "headers_middleware",
    "logger_middleware",
    "middleware",
]
