import datetime
import json
from collections import Mapping
from enum import Enum

from aiohttp import web

from ..threading_utils import threaded


class JSONEncoder(json.JSONEncoder):
    """Class for turning objects into valid json."""

    def default(self, o):
        """Encode objects when no custom handling has been defined."""
        if isinstance(o.__class__, DeclarativeMeta):
            fields = {}

            if hasattr(o, "_format"):
                # object specific prep for json serialization
                o._format()

            for field in o.response_columns:
                fields[field] = self.default(getattr(o, field, None))

            return fields

        elif isinstance(o, datetime.datetime):
            return o.timestamp()

        elif isinstance(o, Enum):
            if hasattr(o, "json_encode"):
                return o.json_encode()
            return o.value

        elif isinstance(o, (list, tuple)):
            return [self.default(el) for el in o]

        elif isinstance(o, (MappedCollection, Mapping)):
            result = {}
            for field in o:
                result[field] = self.default(o[field])
            return result

        elif isinstance(o, dict):
            return_dict = {}
            for field, value in o.items():
                return_dict[self.default(field)] = self.default(value)
            return return_dict

        elif isinstance(o, (int, float, str, type(None))):
            return o
        elif isinstance(o, bytes):
            return o.decode("utf-8")
        return super().default(o)


try:
    from sqlalchemy.ext.declarative import DeclarativeMeta
    from sqlalchemy.orm.collections import MappedCollection
except ImportError:
    pass
else:
    _JSONEncoder = JSONEncoder

    class JSONEncoder(_JSONEncoder):
        def default(self, o):
            """Encode objects when no custom handling has been defined."""
            if isinstance(o.__class__, DeclarativeMeta):
                fields = {}

                if hasattr(o, "_format"):
                    # object specific prep for json serialization
                    o._format()

                for field in o.response_columns:
                    fields[field] = self.default(getattr(o, field, None))

                return fields
            elif isinstance(o, (MappedCollection, Mapping)):
                result = {}
                for field in o:
                    result[field] = self.default(o[field])
                return result
            else:
                return super(self).default(o)


def json_response(json_encoder, response, status=200):
    web_response = web.Response(
        body=json.dumps(response, cls=JSONEncoder), status=status
    )
    web_response.headers["Content-Type"] = "application/json"
    return web_response


@threaded
def threaded_json_response(json_encoder, response, status=200):
    web_response = web.Response(
        body=json.dumps(response, cls=JSONEncoder), status=status
    )
    web_response.headers["Content-Type"] = "application/json"
    return web_response
