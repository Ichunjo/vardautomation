from __future__ import annotations

__all__ = ['AnyPath', 'DuplicateFrame', 'Element', 'Trim', 'UpdateFunc', 'VPSIdx', 'ElementTree']

from os import PathLike
from typing import Any, Callable, Dict, List, Optional, Union, cast

from lxml import etree
from vapoursynth import VideoNode
from vardefunc.types import DuplicateFrame, Trim

AnyPath = Union[PathLike[str], str]
"""Represents a PathLike"""

Element = etree._Element

UpdateFunc = Callable[[int, int], None]
"""An update function type suitable for ``vapoursynth.VideoNode.output``"""

VPSIdx = Callable[[str], VideoNode]
"""Vapoursynth function indexer"""


class ElementTree(etree._ElementTree):
    def xpath(self, _path: Union[str, bytes],  # type: ignore
              namespaces: Optional[Union[Dict[str, str], Dict[bytes, bytes]]] = None,
              extensions: Any = None, smart_strings: bool = True,
              **_variables) -> List[Element]:
        xpathobject = super().xpath(
            _path, namespaces=namespaces, extensions=extensions,
            smart_strings=smart_strings, **_variables
        )
        return cast(List[Element], xpathobject)
