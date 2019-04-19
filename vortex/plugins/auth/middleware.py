from aiohttp.web import middleware

from .config import Configuration, check_config
from .token import decode_token


class AuthUser(object):
    def __init__(self, values):
        self.values = values

    def __getattribute__(self, key):
        if key in self.values:
            return self.values[key]
        super().__getattribute__(key)

    def __str__(self):
        return str(self.values)


@middleware
async def auth_middleware(request, handler):
    check_config()

    if request.middleware_configs.get("login_required"):
        auth_token = request.cookies.get(Configuration.cookie_name)

        if not auth_token:
            auth_header = request.headers.get("Authorization", "")
            if auth_header.startswith("Bearer "):
                auth_token = auth_header.split()[-1]

        if not auth_token:
            raise Configuration.exc_cls("Login Required", code=401)

            request.current_user = AuthUser(decode_token(auth_token))

        Configuration.logger.debug(
            f"Authenticated User {request.current_user}"
        )

    response = await handler(request)
    return response
