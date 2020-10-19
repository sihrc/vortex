from aiohttp import web
from aiohttp.web_exceptions import HTTPPermanentRedirect

from vortex.middlewares import (
    attach_middleware_to_request_kwargs,
    headers_middleware,
    error_middleware,
    logger_middleware,
)
from vortex.logger import Logging


DEFAULT_MIDDLEWARES = (
    web.normalize_path_middleware(
        remove_slash=True, append_slash=False, redirect_class=HTTPPermanentRedirect
    ),
    attach_middleware_to_request_kwargs(),
    logger_middleware,
    headers_middleware,
    error_middleware,
)


def get_app(route_managers=(), middlewares=(), configs=None):
    configs = configs or {}
    apply_middlewares = list(DEFAULT_MIDDLEWARES)
    if middlewares:
        apply_middlewares.extend(list(middlewares))
    app = web.Application(middlewares=apply_middlewares)
    app.update(**configs)
    for route_manager in route_managers:
        # TODO: Log route_manager routes loaded into app
        route_manager.register(app)

    return app


def start_app(app, host="0.0.0.0", port=80, logger=None):
    # TODO: Log server startup
    logger = logger or Logging.get("web")
    web.run_app(app, host=host, port=port, print=logger.info or print)
