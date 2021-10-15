
__all__ = [
    'Mux', 'Stream', 'MediaStream', 'VideoStream', 'AudioStream', 'ChapterStream',
]

from abc import ABC
from pprint import pformat
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple, Union

from ..binary_path import BinaryPath
from ..config import FileInfo
from ..language import UNDEFINED, Lang
from ..status import Status
from ..types import AnyPath
from ..utils import recursive_dict
from ..vpathlib import VPath
from .base import BasicTool


class Stream(ABC):
    """Abstract class representing a stream to be passed to mkvmerge"""

    path: VPath
    """Stream's path"""

    def __init__(self, path: AnyPath) -> None:
        """
        :param path:        Stream's path
        """
        self.path = VPath(path)

    def __str__(self) -> str:
        return pformat(recursive_dict(self), indent=1, width=80, sort_dicts=True)


class MediaStream(Stream, ABC):
    """Class representing a media stream to be passed to mkvmerge."""

    name: Optional[str] = None
    """Stream's name"""

    lang: Lang = UNDEFINED
    """Stream's language"""

    tag_file: Optional[VPath] = None
    """XML tag file"""

    def __init__(self, path: AnyPath, name: Optional[str] = None,
                 lang: Lang = UNDEFINED, tag_file: Optional[AnyPath] = None) -> None:
        """
        Register a MediaStream with its associated informations:

        :param path:        Stream's path
        :param name:        Stream's name, defaults to None
        :param lang:        Stream's language, defaults to UNDEFINED
        :param tag_file:    XML tag file, defaults to None
        """
        super().__init__(path)
        self.name = name
        self.lang = lang
        if tag_file is not None:
            self.tag_file = VPath(tag_file)


class VideoStream(MediaStream):
    ...


class AudioStream(MediaStream):
    ...


class ChapterStream(Stream):
    """Class representing a chapter stream to be passed to mkvmerge"""

    lang: Lang
    """Chapter's language"""

    charset: Optional[str] = None
    """
    Sets the character set that is used for the conversion to UTF-8 for simple chapter files.\n
    See https://mkvtoolnix.download/doc/mkvmerge.html#mkvmerge.description.chapter_charset
    """

    def __init__(self, path: AnyPath,
                 lang: Lang = UNDEFINED, charset: Optional[str] = None) -> None:
        """
        Register a ChapterStream with its associated informations

        :param path:        Stream's path
        :param lang:        Stream's language, defaults to UNDEFINED
        :param charset:     :py:attr:`charset`, defaults to None
        """
        super().__init__(path)
        self.lang = lang
        self.charset = charset



class Mux:
    """Muxing interface using mkvmerge."""

    output: VPath
    """Output path"""
    file: FileInfo
    """FileInfo object"""

    video: VideoStream
    """VideoStream object"""
    audios: Optional[List[AudioStream]]
    """AudioStream object list"""
    chapters: Optional[ChapterStream]
    """ChapterStream object"""
    deterministic_seed: Optional[Union[int, str]]
    """https://mkvtoolnix.download/doc/mkvmerge.html#mkvmerge.description.deterministic"""
    merge_args: Dict[str, Any]
    """Additional arguments to be passed to mkvmerge"""

    __workfiles: Set[VPath]

    def __init__(
        self, file: FileInfo, /,
        streams: Optional[
            Tuple[
                VideoStream,
                Optional[Union[AudioStream, Sequence[AudioStream]]],
                Optional[ChapterStream]
            ]
        ] = None, *,
        deterministic_seed: Union[int, str, None] = None,
        merge_args: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        If ``streams`` is not specified:

            - Will set :py:attr:`vardautomation.config.FileInfo.name_file_final` as VideoStream
            - Will try to find in this order as long as there is a ``file.a_xxxx.set_track(n)``:

                - :py:attr:`vardautomation.config.FileInfo.a_enc_cut`
                - :py:attr:`vardautomation.config.FileInfo.a_src_cut`
                - :py:attr:`vardautomation.config.FileInfo.a_src`

            - All languages are set to ``und`` and names to ``None``.

        Otherwise will mux the ``streams`` to :py:attr:`vardautomation.config.FileInfo.name_file_final`.

        :param file:                :py:attr:`file`
        :param streams:             A tuple of :py:attr:`video`, :py:attr:`audios` and :py:attr:`chapters`, defaults to None
        :param deterministic_seed:  :py:attr:`deterministic_seed`, defaults to None
        :param merge_args:          :py:attr:`merge_args`, defaults to None
        """
        self.output = file.name_file_final
        self.deterministic_seed = deterministic_seed
        self.merge_args = merge_args if merge_args is not None else {}

        if streams is not None:
            self.file = file
            self.video, audios, self.chapters = streams
            if not audios:
                self.audios = []
            else:
                self.audios = [audios] if isinstance(audios, AudioStream) else list(audios)
        else:
            self.file = file
            self.video = VideoStream(file.name_clip_output)
            self.audios = None
            self.chapters = None

    def run(self) -> Set[VPath]:
        """Make and launch the command"""
        self.__workfiles = set()

        cmd = ['-o', self.output.to_str()]

        if self.deterministic_seed is not None:
            cmd += ['--deterministic', str(self.deterministic_seed)]

        cmd += self._video_cmd()

        if self.audios is not None:
            cmd += self._audios_cmd()
        else:
            self.audios = []
            i = 1
            while True:
                if self.file.a_enc_cut is not None and self.file.a_enc_cut.set_track(i).exists():
                    self.audios.append(AudioStream(self.file.a_enc_cut.set_track(i)))
                elif self.file.a_src_cut is not None and self.file.a_src_cut.set_track(i).exists():
                    self.audios.append(AudioStream(self.file.a_src_cut.set_track(i)))
                elif self.file.a_src is not None and self.file.a_src.set_track(i).exists():
                    self.audios.append(AudioStream(self.file.a_src.set_track(i)))
                else:
                    break
                i += 1
            cmd += self._audios_cmd()

        if self.chapters is not None:
            cmd += self._chapters_cmd()
        else:
            if (chap := self.file.chapter) and chap.exists():
                self.chapters = ChapterStream(chap)
                cmd += self._chapters_cmd()

        for k, v in self.merge_args.items():
            cmd += [k] + ([str(v)] if v else [])

        BasicTool(BinaryPath.mkvmerge, cmd).run()

        return self.__workfiles


    def _video_cmd(self) -> List[str]:
        cmd: List[str] = []

        if self.video.tag_file:
            if self.video.tag_file.exists():
                cmd += ['--tags', '0:' + self.video.tag_file.to_str()]
            else:
                Status.fail(f'{self.__class__.__name__}: "{self.video.tag_file}" not found!')

        if self.video.name:
            cmd += ['--track-name', '0:' + self.video.name]

        if self.video.path.exists():
            cmd += ['--language', '0:' + self.video.lang.iso639, self.video.path.to_str()]
        else:
            Status.fail(f'{self.__class__.__name__}: "{self.video.path}" not found!')

        self.__workfiles.add(self.video.path)
        return cmd

    def _audios_cmd(self) -> List[str]:
        cmd: List[str] = []
        assert self.audios
        for audio in self.audios:
            if audio.tag_file:
                if audio.tag_file.exists():
                    cmd += ['--tags', '0:' + audio.tag_file.to_str()]
                else:
                    Status.fail(f'{self.__class__.__name__}: "{audio.tag_file} not found!')
            if audio.name:
                cmd += ['--track-name', '0:' + audio.name]

            if audio.path.exists():
                cmd += ['--language', '0:' + audio.lang.iso639, audio.path.to_str()]
            else:
                i = 1
                while True:
                    if (a_good_path := audio.path.set_track(i)).exists():
                        Status.warn(f'{self.__class__.__name__}: "{audio.path}" not found, found "{a_good_path}"" instead.')
                        cmd += ['--language', '0:' + audio.lang.iso639, a_good_path.to_str()]
                        break
                    i += 1
                    if i > 10:
                        Status.fail(f'{self.__class__.__name__}: "{audio.path}" not found!')

            self.__workfiles.add(audio.path)
        return cmd

    def _chapters_cmd(self) -> List[str]:
        assert self.chapters
        cmd = ['--chapter-language', self.chapters.lang.iso639]
        if self.chapters.charset:
            cmd += ['--chapter-charset', self.chapters.charset]

        if self.chapters.path.exists():
            cmd += ['--chapters', self.chapters.path.to_str()]
        else:
            Status.fail(f'{self.__class__.__name__}: "{self.chapters.path}" not found!')
        self.__workfiles.add(self.chapters.path)
        return cmd
