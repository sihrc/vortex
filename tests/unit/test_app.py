import unittest
from unittest.mock import MagicMock, patch

from aiohttp import web

from vortex.app import start_app, DEFAULT_MIDDLEWARES


class AppUnitTestCase(unittest.TestCase):
    """
    Unit testing start_app function
    """
    def test_start_app_default(self):
        with patch("vortex.app.web.run_app", MagicMock()) as run_app_mock:
            start_app()
            # Check defaults
            called_args, called_kwargs =  run_app_mock.call_args
            app = called_args[0]
            self.assertEqual(len(app.middlewares), len(DEFAULT_MIDDLEWARES))
            self.assertIsInstance(app, web.Application)

            # Ensure no configs passed
            self.assertEqual(list(app.items()), [])
            self.assertEqual(called_kwargs, {
                "host": "0.0.0.0",
                "port": 80,
                "print": print
            })


    def test_start_app_non_default(self):
        with patch("vortex.app.web.run_app", MagicMock()) as run_app_mock:
            start_app(
                middlewares=[],
                bind="127.0.0.1",
                port=8080,
                configs={"environment": "development"}
            )

            # Check custom arguments
            called_args, called_kwargs = run_app_mock.call_args
            app = called_args[0]
            self.assertIsInstance(app, web.Application)
            self.assertEqual(len(app.middlewares), 0)

            # Ensure no configs passed
            self.assertEqual(dict(app.items()), {"environment": "development"})
            self.assertEqual(called_kwargs, {
                "host": "127.0.0.1",
                "port": 8080,
                "print": print
            })


    def test_start_app_route_manager(self):
        app_mock = MagicMock()
        with patch("vortex.app.web.run_app", MagicMock()) as run_app_mock:
            with patch("vortex.app.web.Application", MagicMock(return_value=app_mock)):
                mock_route_managers = MagicMock()

                start_app(route_managers=(mock_route_managers, ))
                app_mock.add_subapp.assert_called_once()

                called_args, _ = run_app_mock.call_args
                app = called_args[0]
                self.assertEqual(app_mock, app)


