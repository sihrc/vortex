from functools import wraps
from concurrent.futures import ThreadPoolExecutor

import asyncio

MAIN_POOL = ThreadPoolExecutor(4)


def threaded(f):
    @wraps(f)
    def wrapped(*args, _sync=False, **kwargs):
        if _sync:
            return f(*args, **kwargs)
        return asyncio.get_event_loop().run_in_executor(
            MAIN_POOL, lambda: f(*args, **kwargs)
        )

    return wrapped


def threaded_exec(f, *args, **kwargs):
    return threaded(f)(*args, **kwargs)
