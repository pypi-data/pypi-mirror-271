import functools
import os
import time
from pathlib import Path

import asyncer
import cloudpickle as pickle
import pyrsistent
import xxhash
from loguru import logger
from rich import print
from sqlalchemy import UUID
from toolz import curry

from sqlpile.abcs import BaseCache
from sqlpile.config import settings as config
from sqlpile.core import MultiLayerCache, SQLCache


def dogpile(cache_instance: BaseCache):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            raw_key = (func.__name__, args, tuple(sorted(kwargs.items())))
            result = cache_instance.get(raw_key)
            if result is not None:
                return result
            else:
                result = func(*args, **kwargs)
                cache_instance.set(raw_key, result)
                return result

        return wrapper

    return decorator


def get_layered_cache():
    remote = SQLCache(config.remote_db_uri)
    local = SQLCache(config.local_db_uri)
    cache = MultiLayerCache(local, remote)
    return cache


# Create curry function of dogpile
cache = get_layered_cache()
dogpile = curry(dogpile)
sqlpile = dogpile(cache_instance=cache)
# sqlpile = curry(dogpile)(cache_instance=layered_cache)


@sqlpile
def example_function():
    time.sleep(10)
    return 42


def main():

    print(cache.set("key", 1))
    print(cache["key"])
    print("key" in cache)
    for i in range(10):
        logger.debug("Starting example function")
        example_function()
        logger.success("Finished example function")

    # CacheEntry.__table__.drop(session.get_bind(), checkfirst=True)
    # engine = create_engine()
    # print(engine)

    # print(CacheEntry.__table__)

    # remote.set("key", "value")
    # print(remote["key"])
    # print("key" in remote)
    # # cache.delete("key")
    # # for i in range(10):

    # #     print(remote.incr("key_count"))

    # local = SQLCache(LOCAL_URL)
    # cache = MultiLayerCache(local, remote)
    # print(cache["key"])


if __name__ == "__main__":
    main()
