
__all__ = ['AnyPath', 'DuplicateFrame', 'Element', 'Trim', 'UpdateFunc', 'VPSIdx', 'ElementTree']

from os import PathLike
from typing import Any, Callable, Dict, List, Optional, Union, cast

from lxml import etree
from vapoursynth import VideoNode
from vardefunc.types import DuplicateFrame as V_DF
from vardefunc.types import Trim as V_Trim

AnyPath = Union[PathLike[str], str]
DuplicateFrame = V_DF
Element = etree._Element
Trim = V_Trim
UpdateFunc = Callable[[int, int], None]
VPSIdx = Callable[[str], VideoNode]


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
