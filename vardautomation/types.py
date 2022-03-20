from __future__ import annotations

__all__ = ['AnyPath', 'DuplicateFrame', 'Element', 'Trim', 'UpdateFunc', 'VPSIdx', 'ElementTree']

from abc import ABC
from os import PathLike
from typing import Any, Callable, Iterable, Iterator, List, Mapping, MutableSet, Optional, Set, TypeVar, Union, cast

from lxml import etree
from typing_extensions import ParamSpec
from vapoursynth import VideoNode
from vardefunc.types import DuplicateFrame, Trim

T = TypeVar('T')
F = TypeVar('F', bound=Callable[..., Any])
P = ParamSpec('P')

AnyPath = Union[PathLike[str], str]
"""Represents a PathLike"""

Element = etree._Element  # type: ignore

UpdateFunc = Callable[[int, int], None]
"""An update function type suitable for ``vapoursynth.VideoNode.output``"""

VPSIdx = Callable[[str], VideoNode]
"""Vapoursynth function indexer"""


class ElementTree(etree._ElementTree):  # type: ignore
    def xpath(self, _path: Union[str, bytes],  # type: ignore
              namespaces: Optional[Mapping[str, str]] = None,
              extensions: Any = None, smart_strings: bool = True,
              **_variables: Any) -> List[Element]:
        xpathobject = super().xpath(
            _path, namespaces=namespaces, extensions=extensions,
            smart_strings=smart_strings, **_variables
        )
        return cast(List[Element], xpathobject)


class AbstractMutableSet(MutableSet[T], ABC):
    __slots__ = ('__data', )
    __data: Set[T]

    def __init__(self, __iterable: Optional[Iterable[T]] = None) -> None:
        self.__data = set(__iterable) if __iterable is not None else set()
        super().__init__()

    def __str__(self) -> str:
        return self.__data.__str__()

    def __repr__(self) -> str:
        return self.__data.__repr__()

    def __contains__(self, x: object) -> bool:
        return self.__data.__contains__(x)

    def __iter__(self) -> Iterator[T]:
        return self.__data.__iter__()

    def __len__(self) -> int:
        return self.__data.__len__()

    def add(self, value: T) -> None:
        return self.__data.add(value)

    def discard(self, value: T) -> None:
        return self.__data.discard(value)

    def update(self, *s: Iterable[T]) -> None:
        return self.__data.update(*s)
