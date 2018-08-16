from aiohttp import web

DEFAULT_MIDDLEWARES = ()

def start_app(
    bind="0.0.0.0",
    port=80,
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
        app.add_subapp(route_manager.base, route_manager.app)

    # TODO: Log server startup
    web.run_app(
        app,
        host=bind,
        port=port,
        print=print # TODO: Replace with logger
    )