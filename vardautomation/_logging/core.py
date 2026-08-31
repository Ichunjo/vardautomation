from __future__ import annotations

# pylint: disable=no-member
# pylint: disable=broad-except
# pylint: disable=inconsistent-return-statements

__all__: list[str] = ["logger"]

import importlib.resources as impr
import sys
from collections.abc import Callable
from contextlib import AbstractContextManager as ContextManager
from functools import wraps
from typing import Any, NamedTuple, NoReturn, overload

import loguru
from jetpytools import Singleton

from .helpers import add_log_attribute, loguru_format, sys_exit

loguru.logger.remove(0)


class LogLevel(NamedTuple):
    name: str
    no: int
    colour: str


TRACE = LogLevel("TRACE", 5, "<cyan><bold>")
DEBUG = LogLevel("DEBUG", 10, "<blue><bold>")
INFO = LogLevel("INFO", 20, "<BLUE><white><bold>")
SUCCESS = LogLevel("SUCCESS", 25, "<green><bold>")
WARNING = LogLevel("WARNING", 30, "<YELLOW><black>")
ERROR = LogLevel("ERROR", 40, "<red><bold>")
CRITICAL = LogLevel("CRITICAL", 50, "<RED><bold>")
LOG_LEVELS = [TRACE, DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL]


class Logger(Singleton):
    __slots__ = ("__id", "__level")

    def __init__(self) -> None:
        self.__level = 20
        __ids = loguru.logger.configure(
            handlers=[
                {
                    "sink": sys.stderr,
                    "level": self.__level,
                    "format": loguru_format,
                    "backtrace": True,
                    "diagnose": False,
                },
            ],
            levels=[{"name": log.name, "color": log.colour} for log in LOG_LEVELS],
            extra={"global_level": self.__level},
        )
        self.__id = __ids.pop(0)

    @property
    def logger(self) -> loguru.Logger:
        return loguru.logger.bind(global_level=self.__level)

    @property
    def level(self) -> int:
        return self.__level

    def set_level(self, level: int) -> None:
        self.__level = level
        loguru.logger.remove(self.__id)
        loguru.logger.add(sys.stderr, level=level, format=loguru_format, backtrace=True, diagnose=False)

    def logo(self) -> None:
        lines = impr.files("vardautomation").joinpath("logo.txt").read_text(encoding="utf-8")
        self.trace("Displaying that based vardautomation logo")
        self.logger.opt(depth=1, colors=True).info("\n" + lines)
        self.logger.opt(raw=True).info("\n")

    @add_log_attribute(TRACE)
    def trace(self, message: Any, /, depth: int = 1, **kwargs: Any) -> None:
        self.logger.opt(depth=depth).trace(str(message), **kwargs)

    @add_log_attribute(DEBUG)
    def debug(self, message: Any, /, depth: int = 1, **kwargs: Any) -> None:
        self.logger.opt(depth=depth).debug(str(message), **kwargs)

    @add_log_attribute(INFO)
    def info(self, message: Any, /, depth: int = 1, **kwargs: Any) -> None:
        if self.__level < 20:
            kwargs.setdefault("colour", self.info.colour.replace("<BLUE>", ""))
        self.logger.opt(depth=depth).info(str(message), **kwargs)

    @add_log_attribute(SUCCESS)
    def success(self, message: Any, /, depth: int = 1, **kwargs: Any) -> None:
        self.logger.opt(depth=depth).success(str(message), **kwargs)

    @add_log_attribute(WARNING)
    def warning(self, message: Any, /, depth: int = 1, **kwargs: Any) -> None:
        if self.__level < 20:
            kwargs.setdefault("colour", "<yellow><bold>")
        self.logger.opt(depth=depth).warning(str(message), **kwargs)

    # @add_log_attribute(log_level=ERROR)
    def error(
        self,
        message: Any,
        /,
        exception: bool | BaseException | None = True,
        depth: int = 1,
        record: bool = False,
        **kwargs: Any,
    ) -> NoReturn:
        self.logger.opt(exception=exception, record=record, depth=depth).error(str(message), **kwargs)
        sys.exit(1)

    # @add_log_attribute(log_level=CRITICAL)
    def critical(
        self,
        message: Any,
        /,
        exception: bool | BaseException | None = True,
        depth: int = 1,
        record: bool = False,
        **kwargs: Any,
    ) -> NoReturn:
        if self.__level < 20:
            kwargs.setdefault("colour", CRITICAL.colour.replace("<RED>", ""))
        self.logger.opt(exception=exception, record=record, depth=depth).critical(str(message), **kwargs)
        sys.exit(1)

    @overload
    def catch[F: Callable[..., Any]](self, func: F) -> F: ...

    @overload
    def catch[F: Callable[..., Any]](self, **kwargs: Any) -> Callable[[F], F]: ...

    def catch[F: Callable[..., Any]](self, func: F | None = None, **kwargs: Any) -> F | Callable[[F], F]:
        if func is None:
            return lambda func: self.catch(func, **kwargs)

        @wraps(func)
        def _wrapper(*args: Any, **kwrgs: Any) -> Any:
            assert func
            try:
                return func(*args, **kwrgs)
            except Exception as e:  # noqa: BLE001
                self.critical(
                    "{record[name]}:{record[line]}: An error has been caught in function '{record[function]}'",
                    e,
                    **{"depth": 2, "record": True} | kwargs,
                )

        return _wrapper

    def catch_ctx(self) -> ContextManager[None]:
        return self.logger.catch(level="CRITICAL", onerror=sys_exit)


# The singleton
logger: Logger = Logger()
