import vapoursynth as vs
from .types import AnyPath, DuplicateFrame as DF, Trim, VPSIdx
from .vpathlib import VPath
from enum import IntEnum
from pymediainfo import MediaInfo
from typing import Any, Callable, List, Optional, Sequence, Union

class PresetType(IntEnum):
    NO_PRESET: int
    VIDEO: int
    AUDIO: int
    CHAPTER: int

class Preset:
    idx: Optional[Callable[[str], vs.VideoNode]]
    a_src: Optional[VPath]
    a_src_cut: Optional[VPath]
    a_enc_cut: Optional[VPath]
    chapter: Optional[VPath]
    preset_type: PresetType

NoPreset: Any
PresetGeneric: Any
PresetBD: Any
PresetWEB: Any
PresetAAC: Any
PresetOpus: Any
PresetEAC3: Any
PresetFLAC: Any
PresetChapOGM: Any
PresetChapXML: Any

class FileInfo:
    path: VPath
    path_without_ext: VPath
    work_filename: str
    idx: Optional[VPSIdx]
    preset: List[Preset]
    name: str
    workdir: VPath
    a_src: Optional[VPath]
    a_src_cut: Optional[VPath]
    a_enc_cut: Optional[VPath]
    chapter: Optional[VPath]
    clip: vs.VideoNode
    clip_cut: vs.VideoNode
    name_clip_output: VPath
    name_file_final: VPath
    name_clip_output_lossless: VPath
    do_lossless: bool
    qpfile: VPath
    do_qpfile: bool
    def __init__(self, path: AnyPath, trims_or_dfs: Union[List[Union[Trim, DF]], Trim, None] = ..., *, idx: Optional[VPSIdx] = ..., preset: Union[Sequence[Preset], Preset] = ..., workdir: AnyPath = ...): ...
    @property
    def trims_or_dfs(self) -> Union[List[Union[Trim, DF]], Trim, None]: ...
    @trims_or_dfs.setter
    def trims_or_dfs(self, x: Union[List[Union[Trim, DF]], Trim, None]) -> None: ...
    @property
    def media_info(self) -> MediaInfo: ...
    @property
    def num_prop(self) -> bool: ...
    @num_prop.setter
    def num_prop(self, x: bool) -> None: ...
