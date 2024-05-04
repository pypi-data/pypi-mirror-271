from functools import lru_cache
from typing import Any

import cloudpickle
import lz4.frame
import xxhash
from diskcache import Cache, memoize_stampede

from sqlpile.config import settings as config

# Home = Path.home()
data_dir = config.app_data_dir
folder_cache = data_dir / "local_cache"
folder_cache.mkdir(parents=True, exist_ok=True)

local_cache = Cache(folder_cache)


class SerializerCompressor:
    """Serialization and compression using cloudpickle and LZ4."""

    def __init__(self, pickle_protocol=None, compress_level=1):
        self.pickle_protocol = pickle_protocol
        self.compress_level = compress_level

    def serialize(self, value):
        return cloudpickle.dumps(value, protocol=self.pickle_protocol)

    def deserialize(self, serialized_value):
        return cloudpickle.loads(serialized_value)

    def compress(self, value):
        serialized_value = self.serialize(value)
        compressed = lz4.frame.compress(
            serialized_value, compression_level=self.compress_level
        )
        # print(type(compressed))
        return compressed
        # return compressed

    def decompress(self, compressed_value):
        decompressed_value = lz4.frame.decompress(compressed_value)
        return self.deserialize(decompressed_value)


@lru_cache(maxsize=128)
@memoize_stampede(cache=local_cache, expire=config.cache_timeout)
def create_hash_key(key: Any) -> str:
    serial = SerializerCompressor()
    hash_key = serial.serialize(key)
    xxhash_key = xxhash.xxh64(hash_key).hexdigest()
    return xxhash_key


@lru_cache(maxsize=128)
@memoize_stampede(cache=local_cache, expire=config.cache_timeout)
def get_serialize_value(value: Any) -> bytes:
    serial = SerializerCompressor()
    return serial.compress(serial.serialize(value))


@lru_cache(maxsize=128)
@memoize_stampede(cache=local_cache, expire=config.cache_timeout)
def deserialize_value(value: bytes) -> Any:
    serial = SerializerCompressor()
    return serial.deserialize(serial.decompress(value))
