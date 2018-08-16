import unittest
from unittest.mock import MagicMock, patch

from aiohttp import web

from vortex.app import start_app, get_app, DEFAULT_MIDDLEWARES


class AppUnitTestCase(unittest.TestCase):
    """
    Unit testing start_app function
    """
    def test_get_app_default(self):
        # Check defaults
        app = get_app()

        self.assertEqual(len(app.middlewares), len(DEFAULT_MIDDLEWARES))
        self.assertIsInstance(app, web.Application)
        self.assertEqual(list(app.items()), [])


    def test_get_app_non_default(self):
        app = get_app(
            middlewares=[],
            configs={"environment": "development"}
        )

        # Check custom arguments
        self.assertIsInstance(app, web.Application)
        self.assertEqual(len(app.middlewares), 0)

        # Ensure configs were passed properly
        self.assertEqual(dict(app.items()), {"environment": "development"})


    def test_start_app_default(self):
        with patch("vortex.app.web.run_app", MagicMock()) as run_app_mock:
            app = MagicMock()
            start_app(app)
            args, kwargs = run_app_mock.call_args

            self.assertEqual(args[0], app)
            self.assertEqual(kwargs, {
                "host":"0.0.0.0",
                "port":80,
                "print":print
            })


    def test_start_app_non_default(self):
        with patch("vortex.app.web.run_app", MagicMock()) as run_app_mock:
            custom_arguments = {
                "port": 8080,
                "host": "127.0.0.1"
            }
            app = MagicMock()
            start_app(app, **custom_arguments)
            args, kwargs = run_app_mock.call_args

            self.assertEqual(args[0], app)
            custom_arguments["print"] = print
            self.assertEqual(kwargs, custom_arguments)


    def test_get_app_route_manager(self):
        app_mock = MagicMock()
        with patch("vortex.app.web.Application", MagicMock(return_value=app_mock)):
            mock_route_manager = MagicMock()

            get_app(route_managers=(mock_route_manager, ))
            mock_route_manager.register.assert_called_once()


