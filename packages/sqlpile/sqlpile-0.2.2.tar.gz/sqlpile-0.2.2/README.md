# SQLPile - SQL-Based Multi-Layered Caching (Arrow + SQLite + Postgres)

Full-featured multi-layered distributed cache using SQL databases. Why build a cache on top of a database? Largely because SQL has similar interfaces across many different databases, and it's easy to scale out. This project is a work in progress, and is not yet ready for production use.

Think about this project as if it's like Ibis, but for SQL caching. The goal is to have a simple interface that can be used to cache data in a SQL database. The project is designed to be used with a SQL database, and is not designed to be used with a NoSQL database. Just use redis at that point.


## Installation

```bash
pip install sqlpile
```

## Usage

```python
from sqlpile import sqlpile
import sleep


@sqlpile
def expensive_function():
    sleep.sleep(10)
    return 1


def main():
    for _ in range(10):
        # Moves slow at first, but speeds up over time
        print(expensive_function)
```

## Features
- Multi-layered caching using local (SQLite) and remote (Postgres) databases
-  Serialization and compression of cached values using cloudpickle and lz4
-  Hashing of cache keys using xxhash for efficient lookup
-  Automatic caching of function results using a decorator
-  Asynchronous support with asyncio and aiosqlite
-  Dependency management using pyproject.toml and hatch
-  Code style enforcement with ruff


## Configuration

```python
from sqlpile.config import Config

config = ApplicationSettings(
    local_database_type="sqlite",
    local_database_name="cache.db",
    remote_database_type="postgresql",
    # ...
)

```