from __future__ import annotations

# pylint: disable=inconsistent-return-statements
# pylint: disable=keyword-arg-before-vararg

__all__ = [
    'Track', 'MediaTrack', 'VideoTrack', 'AudioTrack', 'SubtitleTrack', 'ChaptersTrack',
    'SplitMode',
    'MatroskaFile'
]

from abc import ABC, abstractmethod
from enum import Enum
from os import PathLike
from pprint import pformat
from typing import Iterable, List, Literal, MutableSequence, NoReturn, Optional, Sequence, Tuple, overload

# from .._logging import logger
from ..binary_path import BinaryPath
from ..language import UNDEFINED, Lang
from ..types import AnyPath
from ..utils import recursive_dict
from ..vpathlib import CleanupSet, VPath
from .base import BasicTool


class _AbstractTrack(Sequence[str], ABC):
    _cmd: List[str]

    @abstractmethod
    def __init__(self) -> None:
        ...

    @overload
    def __getitem__(self, __x: int) -> str:
        ...

    @overload
    def __getitem__(self, __x: slice) -> Tuple[str, ...]:
        ...

    def __getitem__(self, __x: int | slice) -> str | Tuple[str, ...]:
        return self._cmd.__getitem__(__x)  # type: ignore

    def __len__(self) -> int:
        return self._cmd.__len__()

    def __str__(self) -> str:
        return pformat(recursive_dict(self.__dict__), indent=1, width=80, sort_dicts=True)


class Track(_AbstractTrack):
    """Standard Track interface for to be passed to mkvmerge"""

    path: VPath
    """VPath to the file"""

    opts: Tuple[str, ...]
    """Additional options for this track"""

    def __init__(self, path: AnyPath, *opts: str) -> None:
        """
        Register a new track

        :param path:        Path to the file
        :param opts:        Additional options
        """
        self.path = VPath(path)
        self.opts = opts
        self._cmd = [self.path.to_str()]
        self._cmd.extend(reversed(self.opts))
        super().__init__()


class MediaTrack(Track):
    """Interface for medias track based to be passed to mkvmerge"""

    name: Optional[str]
    """Name of the track"""

    lang: Lang
    """Language of the track"""

    def __init__(self, path: AnyPath, name: Optional[str] = None, lang: Lang = UNDEFINED, tid: int = 0, /, *opts: str) -> None:
        """
        Register a new track

        :param path:        Path to the file
        :param name:        Name of the track
        :param lang:        Language of the track
        :param tid:         Track ID
        :param opts:        Additional options
        """
        super().__init__(path, *opts)
        self.name = name
        self.lang = lang
        if self.name:
            self._cmd.extend([f'{tid}:' + self.name, '--track-name'])
        self._cmd.extend([f'{tid}:' + self.lang.iso639, '--language'])


class VideoTrack(MediaTrack):
    ...


class AudioTrack(MediaTrack):
    ...


class SubtitleTrack(MediaTrack):
    ...


class ChaptersTrack(Track):
    """Interface for chapters track based to be passed to mkvmerge"""

    lang: Lang
    """Language of the track"""

    charset: Optional[str]
    """Character set that is used for the conversion to UTF-8 for simple chapter files."""

    def __init__(self, path: AnyPath, lang: Lang = UNDEFINED, charset: Optional[str] = None, /, *opts: str) -> None:
        """
        Register a new chapters track

        :param path:        Path to the file
        :param lang:        Language of the track
        :param charset:     Character set that is used for the conversion to UTF-8 for simple chapter files
        """
        super().__init__(path, *opts)
        self.lang = lang
        self.charset = charset
        self._cmd.insert(1, '--chapters')
        if self.charset:
            self._cmd.extend([self.charset, '--chapter-charset'])
        self._cmd.extend([self.lang.iso639, '--chapter-language'])


class _AbstractMatroskaFile(MutableSequence[Track]):
    _output: VPath
    _tracks: List[Track]

    @abstractmethod
    def __init__(self) -> None:
        ...

    @overload
    def __getitem__(self, index: int) -> Track:
        ...

    @overload
    def __getitem__(self, index: slice) -> MutableSequence[Track]:
        ...

    def __getitem__(self, index: int | slice) -> Track | MutableSequence[Track]:  # type: ignore
        return self._tracks.__getitem__(index)

    @overload
    def __setitem__(self, index: int, value: Track) -> None:
        ...

    @overload
    def __setitem__(self, index: slice, value: Iterable[Track]) -> None:
        ...

    def __setitem__(self, index: int | slice, value: Track | Iterable[Track]) -> None:
        return self._tracks.__setitem__(index, value)  # type: ignore

    def __delitem__(self, index: int | slice) -> None:
        return self._tracks.__delitem__(index)

    def __len__(self) -> int:
        return self._tracks.__len__()

    def insert(self, index: int, value: Track) -> None:
        return self._tracks.insert(index, value)


class SplitMode(str, Enum):
    """MKVMerge split modes"""
    SIZE = 'size'
    """Split by size"""

    DURATION = 'duration'
    """Split by duration"""

    TIMESTAMPS = 'timestamps'
    """Split by timestamps"""

    PARTS = 'parts'
    """Keep specific parts by specifying timestamp ranges while discarding others"""

    PARTS_FRAMES = 'parts-frames'
    """Keep specific parts by specifying frame/field number ranges while discarding others"""

    FRAMES = 'frames'
    """Split by frames"""

    CHAPTERS = 'chapters'
    """Split by chapters"""


class MatroskaFile(_AbstractMatroskaFile):
    """Matroska file interface"""

    global_opts: Tuple[str, ...]
    """Global options and other options that affect the whole process"""

    def __init__(self, output: AnyPath, tracks: AnyPath | Track | Iterable[AnyPath | Track] | None = None, /, *global_opts: str) -> None:
        """
        Register a new matroska file to be merged/splitted/appended

        :param output:          Output path
        :param tracks:          A path or an iterable of path/Track
        :param global_opts:     Global options
        """
        self._output = VPath(output)
        if not tracks:
            self._tracks = []
        elif isinstance(tracks, Track):
            self._tracks = [tracks]
        elif isinstance(tracks, (str, PathLike)):
            self._tracks = [Track(tracks)]
        else:
            self._tracks = [track if isinstance(track, Track) else Track(track) for track in tracks]
        self.global_opts = global_opts
        super().__init__()

    @property
    def command(self) -> List[str]:
        """Get the mkvmerge command"""
        cmd = list[str]()
        for track in reversed(self._tracks):
            cmd.extend(track)
        cmd.extend(reversed(self.global_opts))
        cmd.extend([self._output.to_str(), '-o'])
        cmd.reverse()
        return cmd

    @overload
    def mux(self, return_workfiles: Literal[True] = ...) -> CleanupSet:
        ...

    @overload
    def mux(self, return_workfiles: Literal[False]) -> None:
        ...

    def mux(self, return_workfiles: bool = True) -> CleanupSet | None:
        """
        Launch a merge command

        :return:        Return worksfiles if True
        """
        BasicTool(BinaryPath.mkvmerge, self.command).run()

        if return_workfiles:
            return CleanupSet(t.path for t in self._tracks)
        return None

    def split(self, mode: SplitMode, param: str) -> None:
        """
        Split function ruled by "mode"

        :param mode:        Split mode
        :param param:       Full command after the mode
        """
        cmd = self.command
        cmd.extend(['--split', mode.value + ':' + param])
        BasicTool(BinaryPath.mkvmerge, cmd).run()

    def split_size(self, size: str) -> None:
        """
        Split the output file after a given size

        :param size:        d[k|m|g]
        """
        self.split(SplitMode.SIZE, size)

    def split_duration(self, duration: str) -> None:
        """
        Split the output file after a given duration

        :param duration:    HH:MM:SS.nnnnnnnnn|ds
        """
        self.split(SplitMode.DURATION, duration)

    def split_timestamps(self, timestamps: Iterable[str]) -> None:
        """
        Split the output file after specific timestamps

        :param timestamps:  A[,B[,C...]]
        """
        self.split(SplitMode.TIMESTAMPS, ','.join(timestamps))

    def split_parts(self, parts: List[Tuple[str | None, str | None]]) -> None:
        """
        Keep specific parts by specifying timestamp ranges while discarding others

        :param parts:       start1-end1[,[+]start2-end2[,[+]start3-end3...]]
        """
        nparts = list[str]()
        for part in parts:
            s, e = part
            if not s:
                s = ''
            if not e:
                e = ''
            pr = s + '-' + e
            nparts.append(pr)
        self.split(SplitMode.PARTS, ','.join(nparts))

    def split_parts_frames(self, parts: List[Tuple[int | None, int | None]]) -> None:
        """
        Keep specific parts by specifying frame/field number ranges while discarding others

        :param parts:       start1-end1[,[+]start2-end2[,[+]start3-end3...]]
        """
        nparts = list[str]()
        for part in parts:
            s, e = part
            ss = '' if not s else str(s)
            ee = '' if not e else str(e)
            pr = ss + '-' + ee
            nparts.append(pr)

        self.split(SplitMode.PARTS_FRAMES, ','.join(nparts))

    def split_frames(self, frames: int | Iterable[int]) -> None:
        """
        Split after specific frames/fields

        :param frames:      A[,B[,C...]]
        """
        self.split(SplitMode.FRAMES, str(frames) if isinstance(frames, int) else ','.join(map(str, frames)))

    def split_chapters(self, indices: Literal['all'] | Iterable[int]) -> None:
        """
        Split before specific chapters

        :param indices:     "all" or A[,B[,C...]]
        """
        if isinstance(indices, str):
            return self.split(SplitMode.CHAPTERS, indices)
        self.split(SplitMode.CHAPTERS, ','.join(map(str, indices)))

    def append_to(self, files: Iterable[AnyPath], ids: Iterable[Tuple[int, int, int, int]] | None = None) -> None:
        """
        Enable append mode

        :param files:       Files to be appended
        :param ids:         Controls to which track another track is appended.
        """
        cmd = self.command
        cmd.append('[')
        cmd.extend(map(str, files))
        cmd.append(']')
        if ids:
            cmd.append('--append-to')
            cmd.append(','.join(':'.join(map(str, id_)) for id_ in ids))
        BasicTool(BinaryPath.mkvmerge, cmd).run()

    def add_attachments(self) -> NoReturn:
        raise NotImplementedError
