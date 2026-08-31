__all__ = ["AnyPath", "DuplicateFrame", "Element", "ElementTree", "Trim", "UpdateFunc", "VPSIdx"]

from abc import ABC
from collections.abc import Callable, Iterable, Iterator, Mapping, MutableSet
from os import PathLike
from typing import Any, cast

from lxml import etree
from vapoursynth import VideoNode
from vardefunc.types import DuplicateFrame, Trim

AnyPath = PathLike[str] | str
"""Represents a PathLike"""

Element = etree._Element

UpdateFunc = Callable[[int, int], None]
"""An update function type suitable for ``vapoursynth.VideoNode.output``"""

VPSIdx = Callable[[str], VideoNode]
"""Vapoursynth function indexer"""


class ElementTree(etree._ElementTree):
    def xpath(  # type: ignore[override]
        self,
        _path: str | bytes,
        namespaces: Mapping[str, str] | None = None,
        extensions: Any = None,
        smart_strings: bool = True,
        **_variables: Any,
    ) -> list[Element]:
        xpathobject = super().xpath(
            _path, namespaces=namespaces, extensions=extensions, smart_strings=smart_strings, **_variables
        )
        return cast(list[Element], xpathobject)


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
