import asyncio
import unittest

class AsyncTestMixin(unittest.TestCase):
    """
    Async tests that setup and teardown an asyncio loop
    attribute: asyncio_loop
    """
    def setUp(self):
        self.asyncio_loop = asyncio.get_event_loop()

    def tearDown(self):
        self.asyncio_loop.close()