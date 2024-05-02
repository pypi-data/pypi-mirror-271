import abc
from typing import Any

from lancedb.pydantic import LanceModel
from sqlalchemy.orm import Session


class BaseCache(abc.ABC):
    def get(self, key: Any):
        pass

    def set(self, key: Any, value: Any) -> Any:
        pass

    def delete(self, key: Any):
        pass

    def get_serial_key(self, key: Any):
        pass

    def get_serial_value(self, value: Any):
        pass

    @property
    def _session(self) -> Session:
        pass


class BaseLance(abc.ABC, LanceModel):

    @abc.abstractmethod
    def table_name(self) -> str:
        pass
