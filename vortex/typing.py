import datetime
import inspect
import json

from aiohttp.web import middleware

from vortex.errors import VortexException


class InvalidFormat(VortexException):
    def __init__(self, field, format):
        super().__init__(f"{field} should be {format}", code=400)


class MissingField(VortexException):
    def __init__(self, field, exp_type):
        super().__init__(f"{field} of type {exp_type} is missing", code=400)


class Argument(object):
    def __call__(self, value):
        if isinstance(value, str):
            value = self.from_string(value)
        return self.call(value)

    def call(self, value):
        return value

    def from_string(self, value):
        return value

    def __str__(self):
        return self.__class__.__name__


class List(Argument):
    def __init__(self, arg):
        self.arg = arg

    def from_string(self, value):
        return [string.strip() for string in value.strip().split(",")]

    def call(self, value):
        return [self.arg(val) for val in value]

    def __instancecheck__(self, item):
        if not isinstance(item, list):
            return False

        return all([self.arg.__instancecheck__(inner) for inner in item])

    def __str__(self):
        return super().__str__() + "({arg})".format(arg=self.arg)


class DateTime(Argument):
    def from_string(self, value):
        return self.call(int(value))

    def call(self, value):
        if not isinstance(value, int):
            raise ValueError("DateTime must be int seconds since epoch")

        return datetime.datetime.fromtimestamp(value)

    def __instancecheck__(self, value):
        return False


class Dict(Argument):
    def __init__(self, key, value, expected_keys=()):
        self.key = key
        self.value = value
        self.expected_keys = expected_keys

    def from_string(self, value):
        return self.call(json.loads(value))

    def call(self, decoded):
        if not all([key in decoded for key in self.expected_keys]):
            raise TypeError(f"Requires expected keys {self.expected_keys}")

        casted_dict = {}
        for key, value in decoded.items():
            try:
                key = self.key(key)
            except:
                raise TypeError(
                    f"Expected {key} in {decoded} to be castable to {self.key}"
                )
            try:
                value = self.value(value)
            except:
                raise TypeError(
                    f"Expected {value} in {decoded} to be castable to {self.value}"
                )

            casted_dict[key] = value

        return casted_dict

    def __instancecheck__(self, item):
        if not isinstance(item, dict):
            return False

        return all([self.key.__instancecheck__(key) for key in item.keys()]) and all(
            [self.value.__instancecheck__(value) for value in item.values()]
        )

    def __str__(self):
        return (
            super().__str__()
            + f"<{self.key}, {self.value}> with keys:{self.expected_keys}"
        )


class Any(Argument):
    def __call__(self, item):
        return item

    def __instancecheck__(self, item):
        return True


class EnumArgument(Argument):
    def __init__(self, arg):
        self.arg = arg

    def from_string(self, value):
        return self.arg(value)

    def __instancecheck__(self, item):
        return isinstance(item, self.arg)

    def __str__(self):
        return f"{super().__str__()}<{self.arg}>"


class Boolean(Argument):
    def from_string(self, value):
        if value.lower() not in {"true", "false"}:
            raise ValueError("Value must be true or false")
        return value.lower() == "true"

    def call(self, value):
        if self.__instancecheck__(value):
            return value
        return self.from_string(value)

    def __instancecheck__(self, value):
        return isinstance(value, bool)


class Optional(Argument):
    def __init__(self, arg):
        self.arg = arg

    def __call__(self, string):
        if string is None or string == "None":
            return None
        else:
            return self.arg(string)

    def __instancecheck__(self, item):
        if item is None:
            return True
        return self.arg.__instancecheck__(item)

    def __str__(self):
        return super().__str__() + "({arg})".format(arg=self.arg)


def type_check(f):
    spec = inspect.getfullargspec(f)
    defaults = {}
    if spec.defaults:
        default_args_start = len(spec.args) - len(spec.defaults)
        defaults = zip(spec.args[default_args_start:], spec.defaults)
        defaults = {arg: value for arg, value in defaults}

    for field, allowed_type in spec.annotations.items():
        if field not in defaults:
            continue

        value = defaults[field]
        if value is not None and not allowed_type.__instancecheck__(value):
            raise AssertionError(
                f"Default value for {field} must be of type {allowed_type}"
            )

    async def wrapper(request, *args, **kwargs):
        arguments = {}
        arguments.update(request.query)
        if request.can_read_body:
            try:
                post_data = await request.json()
            except ValueError:
                raise InvalidFormat("POST Payload", "application/json")
            else:
                arguments.update(post_data)

        resolved_arguments = {}
        for field in spec.args[1:]:
            value = None
            allowed_type = spec.annotations.get(field, str)

            if field in arguments:
                value = arguments[field]
            elif field in request.match_info:
                value = request.match_info[field]
            elif field in defaults:
                value = defaults[field]
            elif allowed_type is Optional:
                value = None
            else:
                raise MissingField(field, allowed_type)

            if not isinstance(value, allowed_type):
                try:
                    value = allowed_type(value)
                except Exception:
                    raise InvalidFormat(field, allowed_type)

            resolved_arguments[field] = value
        response = await f(request, *args, **kwargs, **resolved_arguments)
        return response

    return wrapper
