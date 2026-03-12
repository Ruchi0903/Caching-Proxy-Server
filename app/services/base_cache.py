from abc import ABC, abstractmethod
from typing import Any

class BaseCache(ABC):
    @abstractmethod
    async def get(self, key: str) -> Any:
        pass
    
    @abstractmethod
    async def delete(self, key: str) -> bool:
        pass

    @abstractmethod
    async def set(self, key: str, value: Any, ttl: int):
        pass

    @abstractmethod
    async def clear(self):
        pass