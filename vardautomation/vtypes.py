__all__ = ["AnyPath", "DuplicateFrame", "Element", "ElementTree", "Trim", "UpdateFunc", "VPSIdx"]

import xml.etree.ElementTree as ET
from abc import ABC
from collections.abc import Callable, Iterable, Iterator, MutableSet
from os import PathLike
from typing import TYPE_CHECKING

from vapoursynth import VideoNode
from vardefunc.types import DuplicateFrame, Trim

AnyPath = PathLike[str] | str
"""Represents a PathLike"""

Element = ET.Element

if TYPE_CHECKING:
    ElementTree = ET.ElementTree[ET.Element]
else:
    ElementTree = ET.ElementTree

UpdateFunc = Callable[[int, int], None]
"""An update function type suitable for ``vapoursynth.VideoNode.output``"""

VPSIdx = Callable[[str], VideoNode]
"""Vapoursynth function indexer"""


class AbstractMutableSet[T](MutableSet[T], ABC):
    __slots__ = ("__data",)
    __data: set[T]

    def __init__(self, iterable: Iterable[T] | None = None, /) -> None:
        self.__data = set(iterable) if iterable is not None else set()
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
