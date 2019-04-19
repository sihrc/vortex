import logging
from vortex.errors import VortexException


class Configuration(object):
    configured = False

    logger = logging.getLogger("vortex.plugins.auth")
    exc_cls = VortexException
    audience = ["vortex:auth"]
    cookie_name = "auth_token"
    cookie_domain = NotImplemented
    auth_secret = NotImplemented


def configure(
    auth_secret,
    cookie_domain,
    audience=(),
    cookie_name="auth_token",
    exc_cls=None,
    logger=None,
):
    if Configuration.configured:
        raise RuntimeError("configure cannot be called twice")

    Configuration.logger = logger
    Configuration.auth_secret = auth_secret
    Configuration.logger = logger

    assert issubclass(exc_cls, VortexException)
    Configuration.exc_cls = exc_cls

    assert isinstance(
        audience, (list, tuple, set)
    ), "audience must be list,tuple,set"

    Configuration.audience = audience
    Configuration.cookie_name = cookie_name
    Configuration.configured = True


def check_config():
    if not Configuration.configured:
        raise RuntimeError(
            "vortex.auth.config.configured was not run. Must be run once."
        )
