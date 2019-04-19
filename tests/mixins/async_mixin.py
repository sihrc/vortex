import asyncio
import unittest


class AsyncTestMixin(unittest.TestCase):
    """
    Async tests that setup and teardown an asyncio loop
    attribute: asyncio_loop
    """

    def setUp(self):
        self.asyncio_loop = asyncio.new_event_loop()
        self.addCleanup(self.asyncio_loop.close)

    def run_in_loop(self, task):
        return self.asyncio_loop.run_until_complete(task)

    def tearDown(self):
        self.asyncio_loop.close()
