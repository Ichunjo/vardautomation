"""Config module"""
from __future__ import annotations

__all__ = [
    'FileInfo',
    'Preset', 'NoPreset',
    'PresetGeneric',
    'PresetBD', 'PresetWEB',
    'PresetAAC', 'PresetOpus', 'PresetEAC3', 'PresetFLAC',
    'PresetChapOGM', 'PresetChapXML',
    'BlurayShow'
]

import sys
from dataclasses import dataclass
from enum import IntEnum
from pprint import pformat
from typing import (Callable, Dict, List, NamedTuple, Optional, Sequence,
                    Union, cast)

import vapoursynth as vs
from lvsfunc.misc import source
from pymediainfo import MediaInfo
from vardefunc.util import adjust_clip_frames

from .chapterisation import MplsReader
from .language import UNDEFINED, Lang
from .status import Status
from .types import AnyPath
from .types import DuplicateFrame as DF
from .types import Trim, VPSIdx
from .utils import recursive_dict
from .vpathlib import VPath

core = vs.core


class PresetType(IntEnum):
    """Type of preset"""
    NO_PRESET = 0
    """Special type"""
    VIDEO = 10
    """Video type"""
    AUDIO = 20
    """Audio type"""
    CHAPTER = 30
    """Chapter type"""


@dataclass
class Preset:
    """Preset class that fills some attributes of :py:class:`FileInfo`"""
    idx: Optional[Callable[[str], vs.VideoNode]]
    a_src: Optional[VPath]
    a_src_cut: Optional[VPath]
    a_enc_cut: Optional[VPath]
    chapter: Optional[VPath]
    preset_type: PresetType


NoPreset = Preset(
    idx=None,
    a_src=VPath(''),
    a_src_cut=VPath(''),
    a_enc_cut=VPath(''),
    chapter=VPath(''),
    preset_type=PresetType.NO_PRESET
)
"""
Special Preset that won't do anything
"""

PresetGeneric = Preset(
    idx=source,
    a_src=None,
    a_src_cut=None,
    a_enc_cut=None,
    chapter=None,
    preset_type=PresetType.VIDEO
)
"""
Generic preset which index the video using :py:func:`lvsfunc.misc.source`
"""

PresetBD = Preset(
    idx=core.lsmas.LWLibavSource,
    a_src=VPath('{work_filename:s}_track_{track_number:s}.wav'),
    a_src_cut=VPath('{work_filename:s}_cut_track_{track_number:s}.wav'),
    a_enc_cut=None,
    chapter=None,
    preset_type=PresetType.VIDEO
)
"""
Preset for BD encode.
The indexer is core.lsmas.LWLibavSource and audio sources are .wav
"""

PresetWEB = Preset(
    idx=core.ffms2.Source,
    a_src=None,
    a_src_cut=None,
    a_enc_cut=VPath(''),
    chapter=None,
    preset_type=PresetType.VIDEO
)
"""
Preset for WEB encode.
The indexer is core.ffms2.Source and a_enc_cut is blocked
"""

PresetAAC = Preset(
    idx=None,
    a_src=VPath('{work_filename:s}_track_{track_number:s}.aac'),
    a_src_cut=VPath('{work_filename:s}_cut_track_{track_number:s}.aac'),
    a_enc_cut=VPath('{work_filename:s}_cut_enc_track_{track_number:s}.m4a'),
    chapter=None,
    preset_type=PresetType.AUDIO
)
"""
Preset for AAC encode.
"""

PresetOpus = Preset(
    idx=None,
    a_src=VPath('{work_filename:s}_track_{track_number:s}.opus'),
    a_src_cut=VPath('{work_filename:s}_cut_track_{track_number:s}.opus'),
    a_enc_cut=VPath('{work_filename:s}_cut_enc_track_{track_number:s}.opus'),
    chapter=None,
    preset_type=PresetType.AUDIO
)
"""
Preset for Opus encode.
"""


PresetEAC3 = Preset(
    idx=None,
    a_src=VPath('{work_filename:s}_track_{track_number:s}.eac3'),
    a_src_cut=VPath('{work_filename:s}_cut_track_{track_number:s}.eac3'),
    a_enc_cut=VPath('{work_filename:s}_cut_enc_track_{track_number:s}.eac3'),
    chapter=None,
    preset_type=PresetType.AUDIO
)
"""
Preset for EAC3 encode.
"""

PresetFLAC = Preset(
    idx=None,
    a_src=VPath('{work_filename:s}_track_{track_number:s}.flac'),
    a_src_cut=VPath('{work_filename:s}_cut_track_{track_number:s}.flac'),
    a_enc_cut=VPath('{work_filename:s}_cut_enc_track_{track_number:s}.flac'),
    chapter=None,
    preset_type=PresetType.AUDIO
)
"""
Preset for FLAC encode.
"""

PresetChapOGM = Preset(
    idx=None,
    a_src=None,
    a_src_cut=None,
    a_enc_cut=None,
    chapter=VPath('chapters/{name:s}.txt'),
    preset_type=PresetType.CHAPTER
)
"""
Preset for OGM based chapters.
"""

PresetChapXML = Preset(
    idx=None,
    a_src=None,
    a_src_cut=None,
    a_enc_cut=None,
    chapter=VPath('chapters/{name:s}.xml'),
    preset_type=PresetType.CHAPTER
)
"""
Preset for XML based chapters.
"""



class FileInfo:
    """FileInfo object. This is the first thing you should initialise."""
    path: VPath
    """Path of the video file"""
    path_without_ext: VPath
    """Path of the video file without the extension"""
    work_filename: str
    """Work directory filename"""

    idx: Optional[VPSIdx]
    """Vapoursynth Indexer"""
    preset: List[Preset]
    """Preset(s) used"""

    name: str
    """Name of the script"""

    workdir: VPath
    """Work directory"""

    a_src: Optional[VPath]
    """Audio source path"""
    a_src_cut: Optional[VPath]
    """Audio source trimmed/cut path"""
    a_enc_cut: Optional[VPath]
    """Audio source encoded (and trimmed) path"""
    _chapter: Optional[VPath]

    clip: vs.VideoNode
    """VideoNode object loaded by the indexer"""
    _trims_or_dfs: Union[List[Union[Trim, DF]], Trim, None]
    clip_cut: vs.VideoNode
    """Clip trimmed"""

    name_clip_output: VPath
    """Clip output path name"""
    name_file_final: VPath
    """Final file output path"""

    name_clip_output_lossless: VPath
    """Lossless file name path"""
    do_lossless: bool
    """If lossless or not"""

    _num_prop: bool = False
    _num_prop_name: str = 'FileInfoFrameNumber'

    def __init__(
        self, path: AnyPath, /,
        trims_or_dfs: Union[List[Union[Trim, DF]], Trim, None] = None, *,
        idx: Optional[VPSIdx] = None,
        preset: Union[Sequence[Preset], Preset] = PresetGeneric,
        workdir: AnyPath = VPath().cwd()
    ) -> None:
        """
        Helper which allows to store the data related to your file to be encoded

        :param path:            Path to your source file.
        :param trims_or_dfs:    Adjust the clip length by trimming or duplicating frames. Python slicing. Defaults to None
        :param idx:             Indexer used to index the video track, defaults to None
        :param preset:          Preset used to fill idx, a_src, a_src_cut, a_enc_cut and chapter attributes,
                                defaults to :py:data:`.PresetGeneric`
        :param workdir:         Work directory. Default to the current directorie where the script is launched.
        """
        self.workdir = VPath(workdir).resolve()

        self.path = VPath(path)
        self.path_without_ext = self.path.with_suffix('')
        self.work_filename = self.path.stem

        self.idx = idx

        self.name = VPath(sys.argv[0]).stem

        self.a_src, self.a_src_cut, self.a_enc_cut, self._chapter = (None, ) * 4
        if isinstance(preset, Preset):
            self.preset = [preset]
        else:
            self.preset = sorted(preset, key=lambda p: p.preset_type)
        for p in self.preset:
            self._fill_preset(p)

        if self.idx:
            self.clip = self.idx(str(path))
            self.trims_or_dfs = trims_or_dfs

            self.name_clip_output = self.workdir / VPath(self.name + '.265')
            self.name_file_final = VPath(self.name + '.mkv')

            self.name_clip_output_lossless = self.workdir / VPath(self.name + '_lossless.mkv')
            self.do_lossless = False

        super().__init__()

    def __str__(self) -> str:
        return pformat(recursive_dict(self), width=200, sort_dicts=False)

    def _fill_preset(self, p: Preset) -> None:
        if self.idx is None:
            self.idx = p.idx

        if self.a_src is None and p.a_src is not None:
            if p.a_src == VPath():
                self.a_src = VPath()
            else:
                self.a_src = self.workdir / p.a_src.format(
                    work_filename=self.work_filename, track_number='{track_number}'
                )

        if self.a_src_cut is None and p.a_src_cut is not None:
            if p.a_src_cut == VPath():
                self.a_src_cut = VPath()
            else:
                self.a_src_cut = self.workdir / p.a_src_cut.format(
                    work_filename=self.work_filename, track_number='{track_number}'
                )

        if self.a_enc_cut is None and p.a_enc_cut is not None:
            if p.a_enc_cut == VPath():
                self.a_enc_cut = VPath()
            else:
                self.a_enc_cut = self.workdir / p.a_enc_cut.format(
                    work_filename=self.work_filename, track_number='{track_number}'
                )

        if self.chapter is None and p.chapter is not None:
            self._chapter = self.workdir / p.chapter.format(name=self.name)

    @property
    def chapter(self) -> Optional[VPath]:
        """
        Chapter file path

        :setter:                Set the chapter path
        """
        return self._chapter

    @chapter.setter
    def chapter(self, chap: Optional[VPath]) -> None:
        if chap and chap.suffix not in {'.txt', '.xml'}:
            Status.warn(f'{self.__class__.__name__}: Chapter extension "{chap.suffix}" is not recognised!')
        self._chapter = chap

    @chapter.deleter
    def chapter(self) -> None:
        del self._chapter

    @property
    def trims_or_dfs(self) -> Union[List[Union[Trim, DF]], Trim, None]:
        """
        Trims or DuplicateFrame objects of the current FileInfo

        :setter:                Set trims or duplicate frames
        """
        return self._trims_or_dfs

    @trims_or_dfs.setter
    def trims_or_dfs(self, x: Union[List[Union[Trim, DF]], Trim, None]) -> None:
        self._trims_or_dfs = x
        if x:
            self.clip_cut = adjust_clip_frames(self.clip, x if isinstance(x, list) else [x])
        else:
            self.clip_cut = self.clip

    @property
    def media_info(self) -> MediaInfo:
        """Get the MediaInfo of the video file loaded"""
        return cast(MediaInfo, MediaInfo.parse(self.path))

    @property
    def num_prop(self) -> bool:
        """
        If the frame number is added to props

        :setter:    Add a prop :attr:`_num_prop_name` to the frame properties of :attr:`FileInfo.clip` and :attr:`FileInfo.clip_cut`
        """
        return self._num_prop

    @num_prop.setter
    def num_prop(self, x: bool) -> None:
        self._num_prop = x
        if x:
            def _add_frame_num(n: int, f: vs.VideoFrame) -> vs.VideoFrame:
                (fout := f.copy()).props[self._num_prop_name] = n
                return fout

            self.clip = core.std.ModifyFrame(self.clip, self.clip, _add_frame_num)
            self.trims_or_dfs = self._trims_or_dfs
        else:
            self.clip, self.clip_cut = [
                c.std.RemoveFrameProps(self._num_prop_name) for c in [self.clip, self.clip_cut]
            ]


class BlurayShow:
    class _File(NamedTuple):
        file: VPath
        chapter: Optional[VPath]

    def __init__(self, episodes: Dict[VPath, List[VPath]], global_trims: Union[List[Union[Trim, DF]], Trim, None] = None, *,
                 idx: Optional[VPSIdx] = None, preset: Union[Sequence[Preset], Preset] = PresetGeneric,
                 lang: Lang = UNDEFINED) -> None:
        """
        Helper class for batching shows

        :param episodes:            A dictionnary of episodes.
                                    Keys are the path of each bdmv folder.
                                    Values are the episodes inside the current bdmv folder key.
        :param global_trims:        Adjust the clips length by trimming or duplicating frames. Python slicing. Defaults to None
        :param idx:                 Indexer used to index the video track, defaults to None
        :param preset:              Preset used to fill idx, a_src, a_src_cut, a_enc_cut and chapter attributes,
                                    defaults to :py:data:`.PresetGeneric`
        :param lang:                Chapters language, defaults to UNDEFINED
        """
        self.trims = global_trims
        self.idx = idx
        self.preset = preset

        self.files: List[BlurayShow._File] = []

        for path, eps in episodes.items():
            chap_folder = path / 'chapters'
            chap_folder.mkdir(parents=True, exist_ok=True)
            chaps = sorted(chap_folder.glob('*'))

            if not chaps:
                MplsReader(path, lang).write_playlist(chap_folder)
                chaps = sorted(chap_folder.glob('*'))

            for ep in eps:
                chap_sel: Optional[VPath] = None
                for chap in chaps:
                    if chap.stem.split('_')[1] == ep.stem:
                        chap_sel = chap
                        break
                self.files.append(self._File(path / ep, chap_sel))

    def episodes(self) -> List[FileInfo]:
        files_info: List[FileInfo] = []
        for file in self.files:
            file_info = FileInfo(file.file, self.trims, idx=self.idx, preset=self.preset)
            file_info.chapter = file.chapter
            files_info.append(file_info)
        return files_info

    def episode(self, num: int, /, *, start_from: int = 1) -> FileInfo:
        file = self.files[num - start_from]
        file_info = FileInfo(file.file, self.trims, idx=self.idx, preset=self.preset)
        file_info.chapter = file.chapter
        return file_info
