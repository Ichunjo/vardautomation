import vapoursynth as vs
from .status import Status as Status
from .types import AnyPath as AnyPath
from typing import Any, Callable, Dict, List, Tuple, TypeVar, Union

core: Any

class Properties:
    @classmethod
    def get_color_range(cls, params: List[str], clip: vs.VideoNode) -> Tuple[int, int]: ...
    @staticmethod
    def get_depth(clip: vs.VideoNode) -> int: ...
    @staticmethod
    def get_csp(clip: vs.VideoNode) -> str: ...
    @staticmethod
    def get_encoder_name(path: AnyPath) -> str: ...

def recursive_dict(obj: object) -> Union[Dict[str, Any], str]: ...
F = TypeVar('F', bound=Callable[..., Any])

def copy_docstring_from(original: Callable[..., Any], mode: str = ...) -> Callable[[F], F]: ...
