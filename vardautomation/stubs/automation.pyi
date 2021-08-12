import vapoursynth as vs
from .config import FileInfo
from .tooling import AudioCutter, AudioEncoder, BasicTool, LosslessEncoder, Mux, VideoEncoder
from .types import AnyPath
from typing import Any, NamedTuple, Optional, Sequence, Set, Tuple, Union

class Parser:
    args: Any
    def __init__(self, file: FileInfo) -> None: ...
    def parsing(self, file: FileInfo, clip: vs.VideoNode) -> Tuple[FileInfo, vs.VideoNode]: ...

class RunnerConfig(NamedTuple):
    v_encoder: VideoEncoder
    v_lossless_encoder: Optional[LosslessEncoder]
    a_extracters: Union[BasicTool, Sequence[BasicTool], None]
    a_cutters: Union[AudioCutter, Sequence[AudioCutter], None]
    a_encoders: Union[AudioEncoder, Sequence[AudioEncoder], None]
    muxer: Optional[Mux]

class SelfRunner:
    clip: vs.VideoNode
    file: FileInfo
    config: RunnerConfig
    cleanup: Set[AnyPath]
    def __init__(self, clip: vs.VideoNode, file: FileInfo, config: RunnerConfig) -> None: ...
    def run(self) -> None: ...
    def do_cleanup(self, *extra_files: AnyPath) -> None: ...
