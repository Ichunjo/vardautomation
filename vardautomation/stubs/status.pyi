from typing import NoReturn, Optional, Type

class Colours:
    FAIL: str
    WARN: str
    INFO: str
    RESET: str

class Status:
    @staticmethod
    def fail(string: str, *, exception: Type[BaseException] = ..., chain_err: Optional[BaseException] = ...) -> NoReturn: ...
    @staticmethod
    def warn(string: str, raise_error: bool = ..., *, exception: Optional[Type[BaseException]] = ..., chain_err: Optional[BaseException] = ...) -> None: ...
    @staticmethod
    def info(string: str, raise_error: bool = ..., *, exception: Optional[Type[BaseException]] = ..., chain_err: Optional[BaseException] = ...) -> None: ...
