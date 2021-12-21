"""
Configuration module

Contains FileInfo, BlurayShow and the different Presets to pass to them.
"""

from __future__ import annotations

__all__ = [
    'FileInfo', 'FileInfo2',
    'PresetType',
    'Preset', 'NoPreset',
    'PresetGeneric',
    'PresetBD', 'PresetBDWAV64', 'PresetWEB',
    'PresetAAC', 'PresetOpus', 'PresetEAC3', 'PresetFLAC',
    'PresetChapOGM', 'PresetChapXML',
    'BlurayShow'
]

import sys
from dataclasses import dataclass
from enum import IntEnum
from pprint import pformat
from typing import Any, Callable, Dict, List, NamedTuple, Optional, Sequence, Type, TypeVar, Union

import vapoursynth as vs
from lvsfunc.misc import source
from pymediainfo import MediaInfo
from vardefunc.util import adjust_audio_frames, adjust_clip_frames

from .chapterisation import MplsReader
from .language import UNDEFINED, Lang
from .render import audio_async_render
from .status import Status
from .types import AnyPath
from .types import DuplicateFrame as DF
from .types import Trim, VPSIdx
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
    """Vapoursynth indexer callable"""

    a_src: Optional[VPath]
    """Audio source path"""

    a_src_cut: Optional[VPath]
    """Audio trimmed source path"""

    a_enc_cut: Optional[VPath]
    """Audio trimmed encoded source path"""

    chapter: Optional[VPath]
    """Chapter file path"""

    preset_type: PresetType
    """Preset type from :py:class:`PresetType`"""


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

PresetBDWAV64 = Preset(
    idx=core.lsmas.LWLibavSource,
    a_src=VPath('{work_filename:s}_track_{track_number:s}.w64'),
    a_src_cut=VPath('{work_filename:s}_cut_track_{track_number:s}.w64'),
    a_enc_cut=None,
    chapter=None,
    preset_type=PresetType.VIDEO
)
"""
Preset for BD encode.
The indexer is core.lsmas.LWLibavSource and audio sources are .w64
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
The indexer is core.ffms2.Source and a_enc_cut is blocked.
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
    _trims_or_dfs: Union[List[Union[Trim, DF]], Trim, None]

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

            self.name_clip_output = self.workdir / VPath(self.name)
            self.name_file_final = VPath(self.name + '.mkv')

            self.name_clip_output_lossless = self.workdir / VPath(self.name + '_lossless.mkv')
            self.do_lossless = False

        self.__post_init__()

    # pylint: disable=no-self-use
    def __post_init__(self) -> None:
        ...

    def __str__(self) -> str:
        dico = dict(self.__dict__)
        for k in list(dico.keys()):
            if k.startswith('_'):
                del dico[k]
        dico['chapter'] = self.chapter
        dico['trims_or_dfs'] = self.trims_or_dfs
        dico['media_info'] = self.media_info
        dico['num_prop'] = self.num_prop
        return pformat(dico, width=200, sort_dicts=False)

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

    def set_name_clip_output_ext(self, extension: str, /) -> None:
        """
        Set the extension of :attr:`FileInfo.name_clip_output`

        :param extension:       Extension in string format, eg. ".265"
        """
        self.name_clip_output = self.name_clip_output.with_suffix(extension)

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
            self.clip_cut = adjust_clip_frames(self.clip, x)
        else:
            self.clip_cut = self.clip

    @property
    def media_info(self) -> MediaInfo:
        """Get the MediaInfo of the video file loaded"""
        return MediaInfo.parse(self.path)

    @property
    def num_prop(self) -> bool:
        """
        If the frame number is added to props

        :setter:    Add a prop ``FileInfoFrameNumber`` to the frame properties of :attr:`FileInfo.clip` and :attr:`FileInfo.clip_cut`
        """
        return self._num_prop

    @num_prop.setter
    def num_prop(self, x: bool) -> None:
        self._num_prop = x
        if x:
            def _add_frame_num(n: int, f: vs.VideoFrame) -> vs.VideoFrame:
                (fout := f.copy()).props['FileInfoFrameNumber'] = n
                return fout

            self.clip = core.std.ModifyFrame(self.clip, self.clip, _add_frame_num)
            self.trims_or_dfs = self._trims_or_dfs
        else:
            self.clip, self.clip_cut = [
                c.std.RemoveFrameProps('FileInfoFrameNumber') for c in [self.clip, self.clip_cut]
            ]


class FileInfo2(FileInfo):
    """Second version of FileInfo adding audio support"""

    audios: List[vs.AudioNode]
    """List of AudioNode indexed by BestAudioSource in the file"""

    audios_cut: List[vs.AudioNode]
    """List of AudioNode cut with the specified trims"""

    def __post_init__(self) -> None:
        self.audios = []
        self.audios_cut = []

        track = 0
        num_error = 0
        while num_error < 2:
            try:
                audio = core.bas.Source(str(self.path), track=track)
            except vs.Error:
                num_error += 1
            else:
                self.audios.append(audio)
                num_error = 0
            track += 1

        if self.trims_or_dfs:
            for audio in self.audios:
                self.audios_cut.append(
                    adjust_audio_frames(audio, self.trims_or_dfs, ref_fps=self.clip.fps)
                )
        else:
            self.audios_cut = self.audios.copy()

    @property
    def audio(self) -> vs.AudioNode:
        """
        Return the first AudioNode track of the file.

        :return:        AudioNode
        """
        return self.audios[0]

    @property
    def audio_cut(self) -> vs.AudioNode:
        """
        Return the first trimmed AudioNode track of the file.

        :return:        AudioNode
        """
        return self.audios_cut[0]

    def write_a_src(self, index: int, offset: int = -1) -> None:
        """
        Using `audio_async_render` write the AudioNodes of the file
        as a WAV file to `a_src` path
        """
        if self.a_src:
            with self.a_src.set_track(index).open('wb') as binary:
                audio_async_render(
                    self.audios[index + offset], binary,
                    progress=f'Writing a_src to {self.a_src.set_track(index).resolve().to_str()}'
                )
        else:
            Status.fail(f'{self.__class__.__name__}: no a_src VPath found!', exception=ValueError)

    def write_a_src_cut(self, index: int, offset: int = -1) -> None:
        """
        Using `audio_async_render` write the AudioNodes of the file
        as a WAV file to `a_src_cut` path
        """
        if self.a_src_cut:
            with self.a_src_cut.set_track(index).open('wb') as binary:
                audio_async_render(
                    self.audios_cut[index + offset], binary,
                    progress=f'Writing a_src_cut to {self.a_src_cut.set_track(index).resolve().to_str()}'
                )
        else:
            Status.fail(f'{self.__class__.__name__}: no a_src_cut VPath found!', exception=ValueError)


class _File(NamedTuple):
    file: VPath
    chapter: Optional[VPath]


_FileInfoType = TypeVar('_FileInfoType', bound=FileInfo)


class BlurayShow:
    """Helper class for batching shows"""

    _files: List[_File]

    _file_info_args: Dict[str, Any]
    _file_ncops: List[_File]
    _file_nceds: List[_File]

    def __init__(self, episodes: Dict[VPath, List[VPath]], global_trims: Union[List[Union[Trim, DF]], Trim, None] = None, *,
                 idx: Optional[VPSIdx] = None, preset: Union[Sequence[Preset], Preset] = PresetGeneric,
                 lang: Lang = UNDEFINED) -> None:
        """
        :param episodes:            A dictionnary of episodes.
                                    Keys are the path of each bdmv folder.
                                    Values are the episodes inside the current bdmv folder key.
        :param global_trims:        Adjust the clips length by trimming or duplicating frames. Python slicing. Defaults to None
        :param idx:                 Indexer used to index the video track, defaults to None
        :param preset:              Preset used to fill idx, a_src, a_src_cut, a_enc_cut and chapter attributes,
                                    defaults to :py:data:`.PresetGeneric`
        :param lang:                Chapters language, defaults to UNDEFINED
        """
        self._file_info_args = dict(trims_or_dfs=global_trims, idx=idx, preset=preset)
        self._files = []

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
                self._files.append(_File(path / ep, chap_sel))

        self._file_ncops = []
        self._file_nceds = []

    def register_ncops(self, *path: VPath) -> None:
        """
        Add NCOP paths to the class
        """
        for p in path:
            self._file_ncops.append(_File(p, None))

    def register_nceds(self, *path: VPath) -> None:
        """
        Add NCED paths to the class
        """
        for p in path:
            self._file_nceds.append(_File(p, None))

    def ncops(self, /, file_info_t: Type[_FileInfoType]) -> List[_FileInfoType]:
        """
        Get all the NCOPs

        :return:                    List of FileInfo
        """
        return [
            self.ncop(i, start_from=0, file_info_t=file_info_t)
            for i in range(len(self._file_ncops))
        ]

    def ncop(self, num: int, /, file_info_t: Type[_FileInfoType], *, start_from: int = 1) -> _FileInfoType:
        """
        Get a specified NCOP

        :param num:                 Numero of the NCOP
        :param start_from:          Indexing starting value, defaults to 1
        :return:                    FileInfo object
        """
        ncop = self._file_ncops[num - start_from]
        ncop_info = file_info_t(ncop.file, **self._file_info_args)
        return ncop_info

    def nceds(self, /, file_info_t: Type[_FileInfoType]) -> List[_FileInfoType]:
        """
        Get all the NCEDs

        :return:                    List of FileInfo
        """
        return [
            self.nced(i, start_from=0, file_info_t=file_info_t)
            for i in range(len(self._file_nceds))
        ]

    def nced(self, num: int, /, file_info_t: Type[_FileInfoType], *, start_from: int = 1) -> _FileInfoType:
        """
        Get a specified NCED

        :param num:                 Numero of the NCED
        :param start_from:          Indexing starting value, defaults to 1
        :return:                    FileInfo object
        """
        nced = self._file_nceds[num - start_from]
        nced_info = file_info_t(nced.file, **self._file_info_args)
        return nced_info

    def episodes(self, /, file_info_t: Type[_FileInfoType]) -> List[_FileInfoType]:
        """
        Get all the episodes

        :return:                    List of FileInfo
        """
        return [
            self.episode(i, start_from=0, file_info_t=file_info_t)
            for i in range(len(self._files))
        ]

    def episode(self, num: int, /, file_info_t: Type[_FileInfoType], *, start_from: int = 1) -> _FileInfoType:
        """
        Get a specified episode

        :param num:                 Numero of the episode
        :param start_from:          Indexing starting value, defaults to 1
        :return:                    FileInfo object
        """
        file = self._files[num - start_from]
        file_info = file_info_t(file.file, **self._file_info_args)
        file_info.chapter = file.chapter
        return file_info
