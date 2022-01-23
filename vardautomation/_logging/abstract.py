from abc import ABC, ABCMeta
from threading import Lock
from typing import Any, Dict, List

__all__: List[str] = []


class SingletonMeta(ABCMeta):
    _instances: Dict[object, Any] = {}
    _lock: Lock = Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Singleton(ABC, metaclass=SingletonMeta):
    __slots__ = ()
