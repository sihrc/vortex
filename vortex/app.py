from aiohttp import web

DEFAULT_MIDDLEWARES = ()

def get_app(
    route_managers=(),
    middlewares=DEFAULT_MIDDLEWARES,
    configs=None
):
    configs = configs or {}

    app = web.Application()
    app.middlewares.extend(middlewares)
    app.update(**configs)

    for route_manager in route_managers:
        # TODO: Log route_manager routes loaded into app
        route_manager.register(app)

    return app


def start_app(app, host="0.0.0.0", port=80):
    # TODO: Log server startup
    web.run_app(
        app,
        host=host,
        port=port,
        print=print # TODO: Replace with logger
    )
