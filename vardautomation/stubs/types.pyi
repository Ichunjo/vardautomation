from lxml import etree
from os import PathLike
from typing import Any, Callable, Dict, List, Optional, Union
from vapoursynth import VideoNode
from vardefunc.types import DuplicateFrame as DuplicateFrame, Trim as Trim

AnyPath = Union[PathLike[str], str]
Element: Any
UpdateFunc = Callable[[int, int], None]
VPSIdx = Callable[[str], VideoNode]

class ElementTree(etree._ElementTree):
    def xpath(self, _path: Union[str, bytes], namespaces: Optional[Union[Dict[str, str], Dict[bytes, bytes]]] = ..., extensions: Any = ..., smart_strings: bool = ..., **_variables: Any) -> List[Element]: ...
