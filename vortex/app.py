from aiohttp import web

from vortex.logger import Logging
from vortex.middlewares import DEFAULT_MIDDLEWARES


def get_app(route_managers=(), middlewares=DEFAULT_MIDDLEWARES, configs=None):
    configs = configs or {}
    app = web.Application()
    app.update(**configs)
    for route_manager in route_managers:
        # TODO: Log route_manager routes loaded into app
        route_manager.register(app, middlewares or [])

    return app


def start_app(app, host="0.0.0.0", port=80, logger=None):
    # TODO: Log server startup
    logger = logger or Logging.get("web")
    web.run_app(app, host=host, port=port, print=logger or print)
