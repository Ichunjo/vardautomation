import vapoursynth as vs
from .types import AnyPath
from enum import Enum
from typing import Dict, Optional, Sequence

class Writer(Enum):
    FFMPEG: int
    IMWRI: int

def make_comps(clips: Dict[str, vs.VideoNode], path: AnyPath = ..., num: int = ..., frames: Optional[Sequence[int]] = ..., *, force_bt709: bool = ..., writer: Writer = ..., magick_compare: bool = ..., slowpics: bool = ..., collection_name: str = ..., public: bool = ...) -> None: ...
