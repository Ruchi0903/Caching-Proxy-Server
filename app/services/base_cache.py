from abc import ABC, abstractmethod
from typing import Any

class BaseCache(ABC):
    @abstractmethod
    def get(self, key: str) -> Any:
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any, ttl: int):
        pass

    @abstractmethod
    def clear(self):
        pass