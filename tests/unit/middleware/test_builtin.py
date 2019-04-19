from unittest.mock import MagicMock

from aiohttp.web import Request, Response
from vortex.middlewares.builtin import (
    attach_middleware_to_request_kwargs,
    attach_middleware_to_response_kwargs,
)

from tests.mixins.async_mixin import AsyncTestMixin


class BuiltinMiddlewareTest(AsyncTestMixin):
    """
    tests for vortex/middlewares.py
    """

    def test_attach_middleware_to_request_kwargs(self):
        """
        Ensures request object has middleware_configs attached and
        aiohttp.web.Request does not use middleware_configs
        """
        mock_kwargs = {"mock_argument": "mock_value"}
        self.assertFalse("middleware_configs" in Request.ATTRS)

        async def mock_route(request):
            self.assertTrue(hasattr(request, "middleware_configs"))
            self.assertCountEqual(request.middleware_configs, mock_kwargs)

        middleware = attach_middleware_to_request_kwargs(mock_kwargs)
        self.run_in_loop(middleware(MagicMock(), mock_route))

    def test_attach_middleware_to_response_kwargs(self):
        """
        Ensures request object has middleware_configs attached and
        aiohttp.web.Request does not use middleware_configs
        """
        mock_kwargs = {"mock_argument": "mock_value"}
        self.assertFalse("middleware_configs" in Response.ATTRS)

        async def mock_route(request):
            return MagicMock()

        middleware = attach_middleware_to_response_kwargs(mock_kwargs)

        response = self.run_in_loop(middleware(MagicMock(), mock_route))

        self.assertEqual(response.middleware_configs, mock_kwargs)
