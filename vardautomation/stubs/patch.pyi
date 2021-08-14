import vapoursynth as vs
from .config import FileInfo
from .tooling import VideoEncoder
from .vpathlib import VPath
from typing import List, Optional, Tuple, Union
from vardefunc.types import Range

class Patch:
    encoder: VideoEncoder
    clip: vs.VideoNode
    file: FileInfo
    ranges: List[Tuple[int, int]]
    debug: bool
    workdir: VPath
    output_filename: VPath
    def __init__(self, encoder: VideoEncoder, clip: vs.VideoNode, file: FileInfo, ranges: Union[Range, List[Range]], output_filename: Optional[str] = ..., *, debug: bool = ...) -> None: ...
    def run(self) -> None: ...
    def do_cleanup(self) -> None: ...
