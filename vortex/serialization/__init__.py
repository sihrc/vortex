"""
Serialization Module
"""
from functools import partial
from .json_serializer import (
    threaded_json_response as _threaded_json_response,
    json_response as _json_response,
    JSONEncoder,
)


class Config(object):
    default_json_encoder = JSONEncoder


json_response = partial(_json_response, Config.default_json_encoder)
threaded_json_response = partial(_threaded_json_response, Config.default_json_encoder)

__all__ = ["json_response", "threaded_json_response", "Config", "JSONEncoder"]
