from __future__ import annotations

# pylint: disable=no-member

__all__: List[str] = ['logger']

import inspect
import sys
from functools import partial
from types import FunctionType, MethodType
from typing import Any, Callable, ContextManager, List, NamedTuple, NoReturn, Type, cast, overload

import loguru
import pkg_resources as pkgr

from ..types import T, F
from .abstract import Singleton
from .helpers import loguru_format, sys_exit, add_log_attribute


loguru.logger.remove(0)


class LogLevel(NamedTuple):
    name: str
    no: int
    colour: str


TRACE = LogLevel('TRACE', 5, '<cyan><bold>')
DEBUG = LogLevel('DEBUG', 10, '<blue><bold>')
INFO = LogLevel('INFO', 20, '<BLUE><white><bold>')
SUCCESS = LogLevel('SUCCESS', 25, '<green><bold>')
WARNING = LogLevel('WARNING', 30, '<YELLOW><black>')
ERROR = LogLevel('ERROR', 40, '<red><bold>')
CRITICAL = LogLevel('CRITICAL', 50, '<RED><bold>')
LOG_LEVELS = [TRACE, DEBUG, INFO, SUCCESS, WARNING, ERROR, CRITICAL]


class Logger(Singleton):
    __slots__ = ('__id', '__level')

    def __init__(self) -> None:
        self.__level = 20
        __ids = loguru.logger.configure(
            handlers=[
                dict(sink=sys.stderr, level=self.__level, format=loguru_format, backtrace=True, diagnose=True)
            ],
            levels=[{'name': log.name, 'color': log.colour} for log in LOG_LEVELS],  # type: ignore
            extra=dict(global_level=self.__level)
        )
        self.__id = __ids.pop(0)

    @property
    def logger(self) -> loguru.Logger:
        return loguru.logger.bind(global_level=self.__level)

    def set_level(self, level: int) -> None:
        self.__level = level
        loguru.logger.remove(self.__id)
        loguru.logger.add(sys.stderr, level=level, format=loguru_format, backtrace=True, diagnose=True)

    def logo(self) -> None:
        with open(pkgr.resource_filename('vardautomation', 'logo.txt'), 'r', encoding='utf-8') as logo:
            lines = logo.read()
        self.trace('Displaying that based vardautomation logo')
        self.logger.opt(depth=1, colors=True).info('\n' + lines)
        self.logger.opt(raw=True).info('\n')

    @add_log_attribute(TRACE)
    def trace(self, message: str, /, depth: int = 1) -> None:
        self.logger.opt(depth=depth).trace(message)

    @add_log_attribute(DEBUG)
    def debug(self, message: str, /, depth: int = 1) -> None:
        self.logger.opt(depth=depth).debug(message)

    @add_log_attribute(INFO)
    def info(self, message: str, /, depth: int = 1) -> None:
        kwargs = dict(colour=self.info.colour.replace('<BLUE>', '')) if self.__level < 20 else {}
        self.logger.opt(depth=depth).info(message, **kwargs)

    @add_log_attribute(SUCCESS)
    def success(self, message: str, /, depth: int = 1) -> None:
        self.logger.opt(depth=depth).success(message)

    @add_log_attribute(WARNING)
    def warning(self, message: str, /, depth: int = 1) -> None:
        kwargs = dict(colour=self.info.colour.replace('<YELLOW>', '')) if self.__level < 20 else {}
        self.logger.opt(depth=depth).warning(message, **kwargs)

    # @add_log_attribute(log_level=ERROR)
    def error(self, message: str, /, exception: bool | BaseException | None = True, depth: int = 1) -> NoReturn:
        self.logger.opt(exception=exception, depth=depth).error(message)
        sys.exit(1)

    # @add_log_attribute(log_level=CRITICAL)
    def critical(self, message: str, /, exception: bool | BaseException | None = True, depth: int = 1) -> NoReturn:
        kwargs = dict(colour=self.info.colour.replace('<RED>', '')) if self.__level < 20 else {}
        self.logger.opt(exception=exception, depth=depth).critical(message, **kwargs)
        sys.exit(1)

    @overload
    def catch(self, obj: Type[T]) -> Type[T]:
        ...

    @overload
    def catch(self, obj: F) -> F:
        ...

    @overload
    def catch(self, *, force_exit: bool = ..., **kwargs: Any) -> Callable[[T], T]:
        ...

    def catch(self, obj: Type[T] | F | None = None, *,  # type: ignore[misc]
              force_exit: bool = True, **kwargs: Any) -> Type[T] | F | Callable[[T], T]:
        if obj is None:
            return cast(Callable[[T], T], partial(self.catch, force_exit=force_exit, **kwargs))

        if isinstance(obj, type):
            for name, fn in inspect.getmembers(obj):
                if isinstance(fn, (FunctionType, MethodType)):
                    setattr(obj, name, partial(self.catch, force_exit=force_exit, **kwargs)(fn))
            return obj

        return self.logger.catch(obj, **dict(onerror=sys_exit if force_exit else None) | kwargs)

    def catch_ctx(self) -> ContextManager[None]:
        return cast(ContextManager[None], self.logger.catch(level='CRITICAL', onerror=sys_exit))


# The singleton
logger: Logger = Logger()
