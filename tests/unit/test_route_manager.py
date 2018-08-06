import unittest
from unittest.mock import MagicMock, Mock

from aiohttp import web

class RouteManagerUnitTests(unittest.TestCase):
    """
    RouteManager unit tests
    """

    def test_basic_route(self):
        """
        Test that basic routes work.
        """
        from vortex.routes import RouteManager
        application_mock = MagicMock()
        application_mock.add_routes = Mock()

        RM = RouteManager(base="/mock")
        RM.app = application_mock

        @RM.route(methods=["GET"], path="/mock_route")
        def mock_route(request):
            return

        mock_args, _ = application_mock.add_routes.call_args

        self.assertEqual(len(mock_args[0]), 1)
        route_def = mock_args[0][0]

        self.assertIsInstance(route_def, web.RouteDef)
        self.assertEqual(route_def.method, "GET")
        self.assertEqual(route_def.path, "/mock_route")
        self.assertEqual(route_def.handler.__name__, mock_route.__name__)





