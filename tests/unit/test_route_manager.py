import unittest
from unittest.mock import MagicMock, patch

from vortex.routes import RouteManager, _partial
from aiohttp import web

from tests.mixins.async_mixin import AsyncTestMixin


class RouteManagerUnitTests(AsyncTestMixin, unittest.TestCase):
    """
    RouteManager unit tests
    """
    def test_partial(self):
        """
        Ensure that custom partial for function attribute inheritance functions
        """

        middleware_called = MagicMock()
        route_called = MagicMock()

        def mock_middleware_function(request, handler):
            middleware_called()
            return handler(request)

        def mock_route_function(request):
            """
            Some mock doc string
            """
            route_called()
            return

        resulting_func = _partial(
            mock_middleware_function,
            handler=mock_route_function
        )

        # Ensure function attrs are bubbled up
        self.assertEqual(resulting_func.__name__, mock_route_function.__name__)
        self.assertEqual(resulting_func.__module__, mock_route_function.__module__)
        self.assertEqual(resulting_func.__doc__, mock_route_function.__doc__)

        # Ensure all functions are called
        resulting_func(MagicMock())

        middleware_called.assert_any_call()
        route_called.assert_any_call()


    def test_basic_route(self):
        """
        Test that basic routes work.
        """
        application_mock = MagicMock()
        RM = RouteManager(base="/mock")
        RM.app = application_mock

        @RM.route(methods=["GET"], path="/mock_route")
        async def mock_route(request):
            return

        # Not using assert_called_with because separate instances of RouteDef are not equal
        mock_args, _ = application_mock.add_routes.call_args

        self.assertEqual(len(mock_args[0]), 1)
        route_def = mock_args[0][0]

        self.assertIsInstance(route_def, web.RouteDef)
        self.assertEqual(route_def.method, "GET")
        self.assertEqual(route_def.path, "/mock_route")
        self.assertEqual(route_def.handler.__name__, mock_route.__name__)


    def test_middlewares(self):
        """
        Ensures that application middlewares are added to the sub-application
        Ensures that route middlewares are applied to the handlers & called
        """
        application_mock = MagicMock()

        @web.middleware
        async def mock_app_middleware(request, handler):
            response = await handler(request)
            return response

        route_middleware_run_check = MagicMock()
        @web.middleware
        async def mock_route_middleware(request, handler):
            route_middleware_run_check()
            response = await handler(request)
            return response

        with patch("vortex.routes.web.Application", MagicMock(return_value=application_mock)):
            RM = RouteManager(base="/mock", middlewares=(mock_app_middleware, ))

        # Ensure sub-application wide middlewares were added
        application_mock.middlewares.append.assert_called_with((mock_app_middleware, ))

        mock_route_run_check = MagicMock()
        @RM.route(methods=["GET"], path="/mock_route", middlewares=(mock_route_middleware, ))
        async def mock_route(request):
            mock_route_run_check()
            return MagicMock()

        mock_args, _ = application_mock.add_routes.call_args

        self.assertEqual(len(mock_args[0]), 1)
        route_def = mock_args[0][0]

        # Ensure even with middlewares, the handler still maintains function signature.
        self.assertEqual(route_def.method, "GET")
        self.assertEqual(route_def.path, "/mock_route")
        self.assertEqual(route_def.handler.__name__, mock_route.__name__)

        # Check route middlewares are called.
        self.run_in_loop(route_def.handler(MagicMock()))
        route_middleware_run_check.assert_any_call()
        mock_route_run_check.assert_any_call()

    def test_middleware_kwargs(self):
        """
        Ensure application level middleware kwargs and route level middleware kwargs
        are present in both response and request
        """
        application_mock = MagicMock()

        resulting_middleware_kwargs = {
            "mock_kwarg_1": "mock_kwarg_1",
            "mock_kwarg_2": "mock_kwarg_2"
        }

        route_middleware_run_check = MagicMock()
        @web.middleware
        async def mock_route_middleware(request, handler):
            route_middleware_run_check()
            self.assertEqual(request.middleware_configs,
                             resulting_middleware_kwargs)

            response = await handler(request)

            self.assertEqual(response.middleware_configs,
                             resulting_middleware_kwargs)

            return response

        RM = RouteManager(base="/mock", mock_kwarg_1="mock_kwarg_1")
        RM.app = application_mock
        self.assertEqual(RM.base_middleware_kwargs, {"mock_kwarg_1": "mock_kwarg_1"})

        route_called_run_check = MagicMock()

        @RM.route(methods=["GET"], path="/mock_route", middlewares=(mock_route_middleware, ), mock_kwarg_2="mock_kwarg_2")
        async def mock_route(request):
            route_called_run_check()
            self.assertEqual(request.middleware_configs,
                             resulting_middleware_kwargs)
            return MagicMock()

        mock_args, _ = application_mock.add_routes.call_args
        route_def = mock_args[0][0]

        # Run the route
        self.run_in_loop(route_def.handler(MagicMock()))
        route_called_run_check.assert_any_call()
        route_middleware_run_check.assert_any_call()



