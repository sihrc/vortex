import json as pyjson
import os
import pytest

from vortex.logger import ROOT_LOGGER
from vortex.serialization.json_serializer import JSONEncoder


def serialized_post(post_fn):
    def wrapped(url, json=None, **kwargs):
        data = json
        if data:
            data = pyjson.dumps(json, cls=JSONEncoder)
        return post_fn(url, data=data, **kwargs)

    return wrapped


@pytest.fixture
async def client(vortex_app, set_logging_level, aiohttp_client):
    client = await aiohttp_client(lambda loop: vortex_app)
    client.post = serialized_post(client.post)
    return client


@pytest.fixture
def default_logging_level():
    return "CRITICAL"


@pytest.fixture(autouse=True)
def set_logging_level(default_logging_level):
    value = os.environ.get("LOGGING_LEVEL", default_logging_level)
    ROOT_LOGGER.setLevel(value)
    yield
