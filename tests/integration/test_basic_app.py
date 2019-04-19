import unittest

from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp import web

from vortex.app import get_app
from vortex.routes import RouteManager


"""
Basic health check route.
"""
RM = RouteManager("/")


@RM.route(path="/health", methods=["GET"])
async def health_check(request):
    return web.Response(text="ready", status=200)


class AppIntegrationTestCase(AioHTTPTestCase):
    """
    Integrations test for basic application use
    """

    async def get_application(self):
        return get_app(route_managers=(RM,))

    @unittest_run_loop
    async def test_health_check(self):
        response = await self.client.request("GET", "/health")
        assert response.status == 200
        text = await response.text()
        self.assertEqual(text, "ready")
