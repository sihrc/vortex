import jwt
import datetime

from .config import Configuration, check_config


def decode_token(self, token):
    check_config()
    try:
        data = jwt.decode(
            token,
            Configuration.auth_secret,
            algorithm="HS256",
            audience=Configuration.audience,
        )
    except (jwt.DecodeError, jwt.InvalidAudienceError):
        raise Configuration.exc_cls("Invalid Token", code=403)
    except jwt.ExpiredSignatureError:
        raise Configuration.exc_cls("Expired Token", code=403)
    else:
        return {
            key[5:]: value
            for key, value in data.items()
            if key.startswith("user_")
        }


def encode_token(self, user_payload, audience=tuple()):
    check_config()
    audience = Configuration.audience + list(audience)
    now = datetime.datetime.utcnow()
    token_payload = {
        "rt_id": None,  # Stub for refresh token in future
        "aud": list(audience),
        "iat": now,
        "exp": now + datetime.timedelta(days=120),
    }

    for key, value in user_payload.items():
        token_payload[f"user_{key}"] = value

    return jwt.encode(
        token_payload, Configuration.auth_secret, algorithm="HS256"
    ).decode()
