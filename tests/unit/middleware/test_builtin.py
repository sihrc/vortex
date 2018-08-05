from unittest.mock import MagicMock

from aiohttp.web import Request

from tests.mixins.async_mixin import AsyncTestMixin


class BuiltinMiddlewareTest(AsyncTestMixin):
    """
    tests for vortex/middlewares.py
    """

    def test_attach_middleware_kwargs(self):
        """
        Ensures request object has middleware_configs attached and
        aiohttp.web.Request does not use middleware_configs
        """
        from vortex.middlewares.builtin import attach_middleware_kwargs

        mock_request_kwargs = {"mock_argument": "mock_value"}
        self.assertFalse("middleware_configs" in Request.ATTRS)

        async def mock_route(request):
            self.assertTrue(hasattr(request, "middleware_configs"))
            self.assertCountEqual(request.middleware_configs, mock_request_kwargs)

        middleware = attach_middleware_kwargs(mock_request_kwargs)

        request = MagicMock()
        self.asyncio_loop.run_until_complete(middleware(request, mock_route))

