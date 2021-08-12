import abc
import asyncio
import vapoursynth as vs
from .config import FileInfo
from .language import Lang
from .types import AnyPath, DuplicateFrame, Trim, UpdateFunc
from .vpathlib import VPath
from abc import ABC, abstractmethod
from enum import IntEnum
from typing import Any, Dict, List, NoReturn, Optional, Sequence, Set, Tuple, Union

class Tool(ABC, metaclass=abc.ABCMeta):
    binary: VPath
    settings: Union[AnyPath, List[str], Dict[str, Any]]
    params: List[str]
    def __init__(self, binary: AnyPath, settings: Union[AnyPath, List[str], Dict[str, Any]]) -> None: ...
    @abstractmethod
    def run(self) -> None: ...
    @abstractmethod
    def set_variable(self) -> Dict[str, Any]: ...

class BasicTool(Tool):
    file: Optional[FileInfo]
    def __init__(self, binary: AnyPath, settings: Union[AnyPath, List[str], Dict[str, Any]], file: Optional[FileInfo] = ...) -> None: ...
    def run(self) -> None: ...
    def set_variable(self) -> Dict[str, Any]: ...

class AudioEncoder(BasicTool):
    track: int
    xml_tag: Optional[AnyPath]
    def __init__(self, binary: AnyPath, settings: Union[AnyPath, List[str], Dict[str, Any]], file: FileInfo, *, track: int = ..., xml_tag: Optional[AnyPath] = ...) -> None: ...
    def run(self) -> None: ...
    def set_variable(self) -> Dict[str, Any]: ...

class PassthroughAudioEncoder(AudioEncoder):
    def __init__(self, file: FileInfo, *, track: int = ..., xml_tag: Optional[AnyPath] = ...) -> None: ...
    def run(self) -> None: ...

class QAACEncoder(AudioEncoder):
    def __init__(self, file: FileInfo, *, track: int = ..., xml_tag: Optional[AnyPath] = ..., tvbr_quality: int = ..., qaac_args: Optional[List[str]] = ...) -> None: ...

class OpusEncoder(AudioEncoder):
    def __init__(self, file: FileInfo, *, track: int = ..., xml_tag: Optional[AnyPath] = ..., bitrate: int = ..., use_ffmpeg: bool = ..., opus_args: Optional[List[str]] = ...) -> None: ...

class FlacCompressionLevel(IntEnum):
    ZERO: int
    ONE: int
    TWO: int
    THREE: int
    FOUR: int
    FIVE: int
    SIX: int
    SEVEN: int
    EIGHT: int
    NINE: int
    TEN: int
    ELEVEN: int
    TWELVE: int
    FAST: int
    BEST: int
    VARDOU: int

class FlacEncoder(AudioEncoder):
    def __init__(self, file: FileInfo, *, track: int = ..., xml_tag: Optional[AnyPath] = ..., level: FlacCompressionLevel = ..., use_ffmpeg: bool = ..., flac_args: Optional[List[str]] = ...) -> None: ...

class AudioCutter(ABC, metaclass=abc.ABCMeta):
    file: FileInfo
    track: int
    kwargs: Dict[str, Any]
    def __init__(self, file: FileInfo, track: int, **kwargs: Any) -> None: ...
    @abstractmethod
    def run(self) -> None: ...
    @classmethod
    @abstractmethod
    def generate_silence(cls, s: float, output: AnyPath, num_ch: int = ..., sample_rate: int = ..., bitdepth: int = ...) -> None: ...

class EztrimCutter(AudioCutter):
    force_eztrim: bool
    def run(self) -> None: ...
    @classmethod
    def ezpztrim(cls, src: AnyPath, output: AnyPath, trims: Union[Trim, DuplicateFrame, List[Trim], List[Union[Trim, DuplicateFrame]]], ref_clip: vs.VideoNode, *, combine: bool = ..., cleanup: bool = ...) -> None: ...
    @classmethod
    def generate_silence(cls, s: float, output: AnyPath, num_ch: int = ..., sample_rate: int = ..., bitdepth: int = ...) -> None: ...

class SoxCutter(AudioCutter):
    def run(self) -> None: ...
    @classmethod
    def soxtrim(cls, src: AnyPath, output: AnyPath, trims: Union[Trim, DuplicateFrame, List[Trim], List[Union[Trim, DuplicateFrame]]], ref_clip: vs.VideoNode, *, combine: bool = ..., cleanup: bool = ...) -> None: ...
    @classmethod
    def generate_silence(cls, s: float, output: AnyPath, num_ch: int = ..., sample_rate: int = ..., bitdepth: int = ...) -> None: ...

class PassthroughCutter(AudioCutter):
    def run(self) -> None: ...
    @classmethod
    def generate_silence(cls, s: float, output: AnyPath, num_ch: int = ..., sample_rate: int = ..., bitdepth: int = ...) -> NoReturn: ...

def progress_update_func(value: int, endvalue: int) -> None: ...

class VideoEncoder(Tool):
    progress_update: Optional[UpdateFunc]
    file: FileInfo
    clip: vs.VideoNode
    def __init__(self, binary: AnyPath, settings: Union[AnyPath, List[str], Dict[str, Any]], progress_update: Optional[UpdateFunc] = ...) -> None: ...
    def run_enc(self, clip: vs.VideoNode, file: Optional[FileInfo], *, y4m: bool = ...) -> None: ...
    def run(self) -> NoReturn: ...
    def set_variable(self) -> Dict[str, Any]: ...

class LosslessEncoder(VideoEncoder):
    def __init__(self, binary: AnyPath, settings: Union[AnyPath, List[str], Dict[str, Any]], progress_update: Optional[UpdateFunc] = ...) -> None: ...
    def set_variable(self) -> Dict[str, Any]: ...

class NvenccEncoder(LosslessEncoder):
    def __init__(self) -> None: ...

class FFV1Encoder(LosslessEncoder):
    def __init__(self, *, threads: int = ...) -> None: ...

class VideoLanEncoder(VideoEncoder, ABC):
    def __init__(self, binary: AnyPath, settings: Union[AnyPath, List[str], Dict[str, Any]], zones: Optional[Dict[Tuple[int, int], Dict[str, Any]]] = ..., progress_update: Optional[UpdateFunc] = ...) -> None: ...
    def set_variable(self) -> Dict[str, Any]: ...

class X265Encoder(VideoLanEncoder):
    def __init__(self, settings: Union[AnyPath, List[str], Dict[str, Any]], zones: Optional[Dict[Tuple[int, int], Dict[str, Any]]] = ..., progress_update: Optional[UpdateFunc] = ...) -> None: ...
    def set_variable(self) -> Dict[str, Any]: ...

class X264Encoder(VideoLanEncoder):
    def __init__(self, settings: Union[AnyPath, List[str], Dict[str, Any]], zones: Optional[Dict[Tuple[int, int], Dict[str, Any]]] = ..., progress_update: Optional[UpdateFunc] = ...) -> None: ...
    def set_variable(self) -> Dict[str, Any]: ...

class Stream(ABC):
    path: VPath
    def __init__(self, path: AnyPath) -> None: ...

class MediaStream(Stream, ABC):
    name: Optional[str]
    lang: Lang
    tag_file: Optional[VPath]
    def __init__(self, path: AnyPath, name: Optional[str] = ..., lang: Lang = ..., tag_file: Optional[AnyPath] = ...) -> None: ...

class VideoStream(MediaStream): ...
class AudioStream(MediaStream): ...

class ChapterStream(Stream):
    lang: Lang
    charset: Optional[str]
    def __init__(self, path: AnyPath, lang: Lang = ..., charset: Optional[str] = ...) -> None: ...

class Mux:
    output: VPath
    file: FileInfo
    video: VideoStream
    audios: Optional[List[AudioStream]]
    chapters: Optional[ChapterStream]
    deterministic_seed: Optional[Union[int, str]]
    merge_args: Dict[str, Any]
    mkvmerge_path: VPath
    def __init__(self, file: FileInfo, streams: Optional[Tuple[VideoStream, Optional[Union[AudioStream, Sequence[AudioStream]]], Optional[ChapterStream]]] = ..., *, deterministic_seed: Union[int, str, None] = ..., merge_args: Optional[Dict[str, Any]] = ...) -> None: ...
    def run(self) -> Set[VPath]: ...

class SubProcessAsync:
    sem: asyncio.Semaphore
    def __init__(self, cmds: List[str], *, nb_cpus: Optional[int] = ...) -> None: ...
