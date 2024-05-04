import concurrent.futures
import threading
import time
import uuid
from contextlib import contextmanager
from typing import Any

from sqlalchemy import Sequence, create_engine
from sqlalchemy.orm import Session, sessionmaker

from sqlpile.abcs import BaseCache
from sqlpile.database import Base, CacheEntry
from sqlpile.utils import (
    SerializerCompressor,
    create_hash_key,
    deserialize_value,
    get_serialize_value,
)


class SQLCache(BaseCache):
    """SQLAlchemy and file-backed cache."""

    def __init__(self, url, timeout=60, **settings):
        """Initialize cache instance.

        :param str url: SQLAlchemy database URL
        :param float timeout: SQLAlchemy connection timeout
        :param settings: any additional SQLAlchemy engine settings

        """
        self._timeout = timeout
        self._local = threading.local()
        self._engine = create_engine(url, query_cache_size=1200, **settings)
        self._session_factory = sessionmaker(bind=self._engine)

        cache_id_seq = Sequence(
            "cached_records_seq", start=1, optional=True, metadata=Base.metadata
        )
        # Base.metadata.create_all(self._engine)
        cache_id_seq.create(bind=self._session_factory().get_bind(), checkfirst=True)
        Base.metadata.create_all(self._engine)
        self._serializer_compressor = SerializerCompressor()

    @property
    def _session(self) -> Session:
        session = getattr(self._local, "session", None)
        if session is None:
            session = self._local.session = self._session_factory()
        return session

    @contextmanager
    def transact(self, retry=False, max_retries=3, retry_delay=0.1):
        """Context manager to perform a transaction with retry."""
        session = self._session
        retries = 0

        while True:
            try:
                yield session
                session.commit()
                break
            except Exception as e:
                session.rollback()

                if retry and retries < max_retries:
                    retries += 1
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    continue
                else:
                    raise e
            finally:
                session.close()

    def get_serial_key(self, key) -> bytes:
        return create_hash_key(key)

    def get_serial_value(self, value) -> bytes:
        return get_serialize_value(value)
        # serialized_value = self._serializer_compressor.serialize(value)
        # return self._serializer_compressor.compress(serialized_value)

    def get_deserial_value(self, compressed_value) -> Any:
        return deserialize_value(compressed_value)

    def set(self, key, value, expire=None, tag=None, retry=False):
        """Set `key` and `value` item in cache."""
        now = time.time()
        expire_time = None if expire is None else now + expire
        serialized_key = self.get_serial_key(key)
        compressed_value = self.get_serial_value(value)

        with self.transact(retry):
            entry = (
                self._session.query(CacheEntry).filter_by(key=serialized_key).first()
            )
            if entry:
                entry.store_time = now
                entry.expire_time = (
                    expire_time or entry.expire_time or time.time() + 3600
                )
                entry.access_time = now
                entry.access_count = 0
                entry.tag = tag
                entry.value = compressed_value
            else:
                entry = CacheEntry(
                    key=serialized_key,
                    raw=1,
                    store_time=now,
                    expire_time=expire_time,
                    access_time=now,
                    tag=tag,
                    value=compressed_value,
                )
                self._session.add(entry)

        return True

    def get(self, key, default=None, expire_time=False, tag=False, retry=False):
        """Retrieve value from cache. If `key` is missing, return `default`."""
        serialized_key = self.get_serial_key(key)

        with self.transact(retry):
            entry = (
                self._session.query(CacheEntry).filter_by(key=serialized_key).first()
            )

            if entry is None or (
                entry.expire_time is not None and entry.expire_time < time.time()
            ):
                return default

            compressed_value = entry.value
            value = self.get_deserial_value(compressed_value)

            entry.access_time = time.time()
            entry.access_count += 1

            if expire_time and tag:
                return value, entry.expire_time, entry.tag
            elif expire_time:
                return value, entry.expire_time
            elif tag:
                return value, entry.tag
            else:
                return value

    def delete(self, key, retry=False):
        """Delete corresponding item for `key` from cache."""
        serialized_key = self.get_serial_key(key)

        with self.transact(retry):
            entry = (
                self._session.query(CacheEntry).filter_by(key=serialized_key).first()
            )

            if entry is None:
                raise KeyError(key)

            self._session.delete(entry)

        return True

    def pop(self, key, default=None, expire_time=False, tag=False, retry=False):
        """Remove corresponding item for `key` from cache and return value.

        If `key` is missing, return `default`.

        Operation is atomic. Concurrent operations will be serialized.

        :param key: key for item
        :param default: return value if key is missing (default None)
        :param bool expire_time: if True, return expire_time in tuple
            (default False)
        :param bool tag: if True, return tag in tuple (default False)
        :param bool retry: retry if database timeout occurs (default False)
        :return: value for item if key is found else default
        :raises Timeout: if database timeout occurs

        """
        serialized_key = self.get_serial_key(key)

        with self.transact(retry):
            entry = (
                self._session.query(CacheEntry).filter_by(key=serialized_key).first()
            )

            if entry is None:
                return default

            value = self.get_deserial_value(entry.value)
            self._session.delete(entry)

            if expire_time and tag:
                return value, entry.expire_time, entry.tag
            elif expire_time:
                return value, entry.expire_time
            elif tag:
                return value, entry.tag
            else:
                return value

    def incr(self, key, delta=1, default=0, retry=False):
        """Increment value by delta for item with key.

        If key is missing and default is None then raise KeyError. Else if key
        is missing and default is not None then use default for value.

        Operation is atomic. All concurrent increment operations will be
        counted individually.

        :param key: key for item
        :param int delta: amount to increment (default 1)
        :param int default: value if key is missing (default 0)
        :param bool retry: retry if database timeout occurs (default False)
        :return: new value for item
        :raises KeyError: if key is not found and default is None
        :raises Timeout: if database timeout occurs

        """
        serialized_key = self.get_serial_key(key)

        with self.transact(retry):
            entry = (
                self._session.query(CacheEntry).filter_by(key=serialized_key).first()
            )

            if entry is None:
                if default is None:
                    raise KeyError(key)

                value = default + delta

                compressed_value = self.get_serial_value(value)
                entry = CacheEntry(
                    key=serialized_key,
                    raw=1,
                    store_time=time.time(),
                    value=compressed_value,
                )
                self._session.add(entry)
            else:
                value = self.get_deserial_value(entry.value)

                if entry.expire_time is not None and entry.expire_time < time.time():
                    if default is None:
                        raise KeyError(key)

                    value = default + delta
                else:
                    value += delta

                compressed_value = self.get_serial_value(value)
                entry.value = compressed_value

            return value

    def _generate_key(self, prefix=None):
        """Generate a random key."""
        if prefix is None:
            return str(uuid.uuid4())
        else:
            return "{}-{}".format(prefix, uuid.uuid4())

    def push(
        self,
        value,
        prefix=None,
        side="back",
        expire=None,
        tag=None,
        retry=False,
    ):
        """Push `value` onto `side` of queue identified by `prefix` in cache."""
        now = time.time()
        expire_time = None if expire is None else now + expire
        serialized_value = self.get_serial_value(value)

        with self.transact(retry) as session:
            if prefix is None:
                key = self._generate_key()
            else:
                key = self._generate_key(prefix)

            serialized_key = self.get_serial_key(key)

            entry = CacheEntry(
                key=serialized_key,
                raw=1,
                store_time=now,
                expire_time=expire_time,
                access_time=now,
                tag=tag,
                size=len(serialized_value),
                value=serialized_value,
            )

            if side == "back":
                session.add(entry)
            else:
                session.add(entry)

            return key

    def decr(self, key, delta=1, default=0, retry=False):
        """Decrement value by delta for item with key.

        If key is missing and default is None then raise KeyError. Else if key
        is missing and default is not None then use default for value.

        Operation is atomic. All concurrent decrement operations will be
        counted individually.

        Unlike Memcached, negative values are supported. Value may be
        decremented below zero.

        :param key: key for item
        :param int delta: amount to decrement (default 1)
        :param int default: value if key is missing (default 0)
        :param bool retry: retry if database timeout occurs (default False)
        :return: new value for item
        :raises KeyError: if key is not found and default is None
        :raises Timeout: if database timeout occurs

        """
        return self.incr(key, -delta, default, retry)

    def __getitem__(self, key):
        """Retrieve value from cache for `key`.

        :param key: key for item
        :return: value for item
        :raises KeyError: if key is missing

        """
        value = self.get(key)
        if value is None:
            raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        """Set `key` and `value` item in cache.

        :param key: key for item
        :param value: value for item

        """
        self.set(key, value)

    def __delitem__(self, key, retry=True):
        """Delete corresponding item for `key` from cache.

        :param key: key for item
        :param bool retry: retry if database timeout occurs (default True)
        :raises KeyError: if key is missing
        :raises Timeout: if database timeout occurs

        """
        self.delete(key, retry)

    def contains(self, key, retry=False):
        serialized_key = self.get_serial_key(key)

        with self.transact(retry):
            entry = (
                self._session.query(CacheEntry).filter_by(key=serialized_key).first()
            )
            return entry is not None

    def __contains__(self, key, retry=False):
        """Check if `key` is in cache without retrieving value.

        :param key: key for item
        :return: True if key is found, else False

        """
        return self.contains(key, retry)


class MultiLayerCache(BaseCache):
    def __init__(self, remote_cache: BaseCache, local_cache: BaseCache):
        self.localz = remote_cache
        # We could add a middle one too
        self.remote = local_cache
        self.init_executor()

    def init_executor(self):
        self.executor = concurrent.futures.ThreadPoolExecutor()

    def __enter__(self):
        self.init_executor()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.executor.shutdown()

    def get(self, key):
        result = self.localz.get(key)

        if result is None:
            result = self.remote.get(key)
            if result is not None:
                self.localz.set(key, result)

        return result

    def __set_background(self, key, value):
        self.localz.set(key, value)
        self.remote.set(key, value)

    def set(self, key, value):
        self.executor.submit(self.__set_background, key, value)

    def __delete_background(self, key):

        self.localz.delete(key)
        self.remote.delete(key)

    def delete(self, key):
        self.executor.submit(self.__delete_background, key)

    def __getitem__(self, key):
        """Retrieve value from cache for `key`.

        :param key: key for item
        :return: value for item
        :raises KeyError: if key is missing

        """
        value = self.get(key)
        if value is None:
            raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        """Set `key` and `value` item in cache.

        :param key: key for item
        :param value: value for item

        """
        self.set(key, value)

    def __delitem__(self, key, retry=True):
        """Delete corresponding item for `key` from cache.

        :param key: key for item
        :param bool retry: retry if database timeout occurs (default True)
        :raises KeyError: if key is missing
        :raises Timeout: if database timeout occurs

        """
        self.delete(key, retry)

    def __contains__(self, key, retry=False):
        """Check if `key` is in cache without retrieving value.

        :param key: key for item
        :return: True if key is found, else False

        """

        if self.localz.contains(key):
            return True
        elif self.remote.contains(key):
            return True
        return False
