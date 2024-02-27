from __future__ import annotations

import re
import sys
from typing import TYPE_CHECKING, Callable, Concatenate, Generic, List, NoReturn, cast, final

import loguru

from ..vtypes import P, T

if TYPE_CHECKING:
    from .core import Logger, LogLevel


__all__: List[str] = []

# pylint: disable=no-member


# Helpers stuff
def close_and_reverse_tags(colour_tags: str) -> str:
    return ''.join(f'</{tag}>' for tag in reversed(re.split(r'<(.*?)>', colour_tags)) if tag)


def loguru_format(record: loguru.Record) -> str:
    global_lvl = record['extra']['global_level']
    if global_lvl >= 20:
        return '<level>{message}</level>\n{exception}'

    if 'colour' in record['extra']:
        lvl_c = str(record['extra']['colour']), close_and_reverse_tags(record['extra']['colour'])
    else:
        lvl_c = '<level>', '</level>'

    return (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        + "<level>{level.name: <8}</level> | "
        + "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        + lvl_c[0] + "{message}" + lvl_c[1] + '\n{exception}'
    )


def sys_exit(_: BaseException) -> NoReturn:
    sys.exit(1)


@final
class _log_func_wrapper(Generic[P, T]):
    name: str
    no: int
    colour: str
    colour_close: str

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T: # type: ignore[empty-body]
        ...


def add_log_attribute(log_level: LogLevel) -> Callable[[Callable[Concatenate[Logger, P], T]], _log_func_wrapper[P, T]]:

    def _wrapper(func: Callable[Concatenate[Logger, P], T]) -> _log_func_wrapper[P, T]:
        funcw = cast(_log_func_wrapper[P, T], func)
        funcw.name = log_level.name
        funcw.no = log_level.no
        funcw.colour = log_level.colour
        funcw.colour_close = close_and_reverse_tags(log_level.colour)
        return funcw

    return _wrapper
