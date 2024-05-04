import time
import uuid

from sqlalchemy import Column, LargeBinary, MetaData, Sequence, Text
from sqlalchemy.orm import (
    DeclarativeMeta,
    Mapped,
    declarative_base,
    mapped_column,
)

# from
# from sqlpile.files
Base: DeclarativeMeta = declarative_base()
metadata = MetaData()

cache_id_seq = Sequence(
    "cached_records_seq", start=1, optional=True, metadata=Base.metadata
)


class CacheEntry(Base):
    """SQLAlchemy model for cache entries."""

    __tablename__ = "cache_records"

    id: Mapped[str] = Column(
        "id",
        Text,
        default=lambda: str(uuid.uuid4()),
        primary_key=True,
        # postgresql_server_default=func.gen_random_uuid(),
    )
    # key = Column(str)
    key: Mapped[str]
    raw: Mapped[int]
    store_time: Mapped[float]
    expire_time: Mapped[float] = mapped_column(default=time.time() + 3600)
    access_time: Mapped[float]
    access_count: Mapped[int] = mapped_column(default=0)
    tag = Column(LargeBinary)
    size: Mapped[int] = mapped_column(default=0)
    mode: Mapped[int] = mapped_column(default=0)
    filename = Column(Text)
    value = Column(LargeBinary)


# for _ in range(20):
#     print(cache.decr("key_count"))
# print(cache.get("key"))
