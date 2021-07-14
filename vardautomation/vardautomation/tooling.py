"""Tooling module"""

__all__ = [
    'Tool', 'BasicTool',
    'AudioEncoder', 'QAACEncoder', 'OpusEncoder', 'FlacCompressionLevel', 'FlacEncoder',
    'AudioCutter',
    'VideoEncoder', 'X265Encoder', 'X264Encoder', 'LosslessEncoder', 'NvenccEncoder', 'FFV1Encoder',
    'progress_update_func',
    'Mux', 'Stream', 'MediaStream', 'VideoStream', 'AudioStream', 'ChapterStream',
    'Tooling'
]

import re
import subprocess
from abc import ABC, abstractmethod
from enum import IntEnum
from pprint import pformat
from typing import (Any, BinaryIO, Dict, List, NoReturn, Optional, Sequence,
                    Set, Tuple, Type, Union, cast)

import vapoursynth as vs
from acsuite import eztrim
from lvsfunc.render import SceneChangeMode, find_scene_changes
from lxml import etree

from .config import FileInfo
from .language import UNDEFINED, Lang
from .properties import Properties
from .status import Status
from .types import AnyPath, UpdateFunc
from .vpathlib import VPath


class Tool(ABC):
    """Abstract Tool interface"""
    binary: VPath
    settings: Union[AnyPath, List[str], Dict[str, Any]]
    params: List[str]

    def __init__(self, binary: AnyPath, settings: Union[AnyPath, List[str], Dict[str, Any]]) -> None:
        self.binary = VPath(binary)
        self.settings = settings
        self.params = []
        super().__init__()

    @abstractmethod
    def run(self) -> None:
        """Tooling chain"""

    @abstractmethod
    def set_variable(self) -> Dict[str, Any]:
        """Set variables in the settings"""

    def _get_settings(self) -> None:
        if isinstance(self.settings, dict):
            for k, v in self.settings.items():
                self.params += [k] + ([str(v)] if v else [])
        elif isinstance(self.settings, list):
            self.params = self.settings
        else:
            with open(self.settings, 'r') as sttgs:
                self.params = re.split(r'[\n\s]\s*', sttgs.read())

        self.params.insert(0, self.binary.to_str())
        self.params = [p.format(**self.set_variable()) for p in self.params]


class BasicTool(Tool):
    """BasicTool interface"""
    file: Optional[FileInfo]

    def __init__(self, binary: AnyPath, settings: Union[AnyPath, List[str], Dict[str, Any]], /,
                 file: Optional[FileInfo] = None) -> None:
        """Helper allowing the use of CLI programs for basic tasks like video or audio track extraction.

        Args:
            binary (AnyPath):
                Path to your binary file.

            settings (Union[AnyPath, List[str], Dict[str, Any]]):
                Path to your settings file or list of string or a dict containing your settings.

            file (Optional[FileInfo]):
                FileInfo object. Not used in BasicTool implementation.
        """
        self.file = file
        super().__init__(binary, settings)

    def run(self) -> None:
        self._get_settings()
        self._do_tooling()

    def set_variable(self) -> Dict[str, Any]:
        return {}

    def _do_tooling(self) -> None:
        Status.info(f'{self.binary.to_str()} command:' + ' '.join(self.params))
        subprocess.run(self.params, check=True, text=True, encoding='utf-8')


class AudioEncoder(BasicTool):
    """BasicTool interface for audio encoding"""
    track: int
    xml_tag: Optional[AnyPath]

    def __init__(self, binary: AnyPath, settings: Union[AnyPath, List[str], Dict[str, Any]], /,
                 file: FileInfo, *, track: int, xml_tag: Optional[AnyPath] = None) -> None:
        """Helper for audio extraction.

        Args:
            binary (AnyPath):
                Path to your binary file.

            settings (Union[AnyPath, List[str], Dict[str, Any]]):
                Path to your settings file or list of string or a dict containing your settings.

            file (FileInfo):
                FileInfo object. Needed in AudioEncoder implementation.

            track (int):
                Track number.

            xml_tag (Optional[AnyPath], optional):
                XML file path.
                If specified, will write a file containing the encoder info
                to be passed to the muxer.
                Defaults to None.
        """
        super().__init__(binary, settings, file=file)

        if self.file is None:
            raise ValueError('AudioEncoder: `file` is needed!')
        if self.file.a_src_cut is None:
            raise ValueError('AudioEncoder: `file.a_src_cut` is needed!')
        if self.file.a_enc_cut is None:
            raise ValueError('AudioEncoder: `file.a_enc_cut` is needed!')

        if track > 0:
            self.track = track
        else:
            raise ValueError('AudioEncoder: `track` must be > 0')
        self.xml_tag = xml_tag

    def run(self) -> None:
        self._get_settings()
        self._do_tooling()
        if self.xml_tag:
            self._write_encoder_name_file()

    def set_variable(self) -> Dict[str, Any]:
        assert self.file
        assert self.file.a_src_cut
        assert self.file.a_enc_cut
        return dict(a_src_cut=self.file.a_src_cut.format(self.track).to_str(),
                    a_enc_cut=self.file.a_enc_cut.format(self.track).to_str())


    def _write_encoder_name_file(self) -> None:
        assert self.file
        assert (a_enc_sut := self.file.a_enc_cut)

        tags = etree.Element('Tags')
        tag = etree.SubElement(tags, 'Tag')
        _ = etree.SubElement(tag, 'Targets')
        simple = etree.SubElement(tag, 'Simple')
        etree.SubElement(simple, 'Name').text = 'ENCODER'
        etree.SubElement(simple, 'String').text = Properties.get_encoder_name(a_enc_sut.format(self.track))

        assert self.xml_tag
        with open(self.file.workdir / self.xml_tag, 'wb') as f:
            f.write(
                etree.tostring(tags, encoding='utf-8', xml_declaration=True, pretty_print=True)
            )


class QAACEncoder(AudioEncoder):
    """QAAC AudioEncoder"""
    def __init__(self, /, file: FileInfo, *,
                 track: int, xml_tag: Optional[AnyPath] = None,
                 tvbr_quality: int = 127, qaac_args: Optional[List[str]] = None) -> None:
        """
        Args:
            file (FileInfo):
                FileInfo object. Needed in AudioEncoder implementation.

            track (int):
                Track number.

            xml_tag (Optional[AnyPath], optional):
                XML file path. If specified, will write a file containing the encoder info
                to be passed to the muxer.
                Defaults to None.

            tvbr_quality (int, optional):
                Read the QAAC doc. Defaults to 127.

            qaac_args (Optional[List[str]], optional):
                Additionnal arguments. Defaults to None.
        """
        binary = 'qaac'
        settings = ['{a_src_cut:s}', '-V', str(tvbr_quality), '--no-delay', '-o', '{a_enc_cut:s}']
        if qaac_args is not None:
            settings.append(*qaac_args)
        super().__init__(binary, settings, file, track=track, xml_tag=xml_tag)


class OpusEncoder(AudioEncoder):
    """Opus AudioEncoder"""
    def __init__(self, /, file: FileInfo, *,
                 track: int, xml_tag: Optional[AnyPath] = None,
                 bitrate: int = 192,
                 use_ffmpeg: bool = True, opus_args: Optional[List[str]] = None) -> None:
        """
        Args:
            file (FileInfo):
                FileInfo object. Needed in AudioEncoder implementation.

            track (int):
                Track number.

            xml_tag (Optional[AnyPath], optional):
                XML file path. If specified, will write a file containing the encoder info
                to be passed to the muxer.
                Defaults to None.

            bitrate (int, optional):
                Opus bitrate in vbr mode. Defaults to 192.

            use_ffmpeg (bool, optional):
                Will use opusenc if false.
                Defaults to True.

            opus_args (Optional[List[str]], optional):
                Additionnal arguments. Defaults to None.
        """
        if use_ffmpeg:
            binary = 'ffmpeg'
            settings = ['-i', '{a_src_cut:s}', '-c:a', 'libopus', '-b:a', f'{bitrate}k', '-o', '{a_enc_cut:s}']
        else:
            binary = 'opusenc'
            settings = ['--bitrate', str(bitrate), '{a_src_cut:s}', '{a_enc_cut:s}']

        if opus_args is not None:
            settings.append(*opus_args)

        super().__init__(binary, settings, file, track=track, xml_tag=xml_tag)


class FlacCompressionLevel(IntEnum):
    """
        Flac compression level.
        Keep in mind that the max FLAC can handle is 8 and ffmpeg 12
    """
    ZERO = 0
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    ELEVEN = 11
    TWELVE = 12
    FAST = 0
    BEST = 8
    VARDOU = 99


class FlacEncoder(AudioEncoder):
    """Flac AudioEncoder"""
    def __init__(self, file: FileInfo, *,
                 track: int, xml_tag: Optional[AnyPath] = None,
                 level: FlacCompressionLevel = FlacCompressionLevel.VARDOU,
                 use_ffmpeg: bool = True, flac_args: Optional[List[str]] = None) -> None:
        """
        Args:
            file (FileInfo):
                FileInfo object. Needed in AudioEncoder implementation.

            track (int):
                Track number.

            xml_tag (Optional[AnyPath], optional):
                XML file path. If specified, will write a file containing the encoder info
                to be passed to the muxer.
                Defaults to None.

            level (FlacCompressionLevel, optional):
                See FlacCompressionLevel for all levels available.
                Defaults to FlacCompressionLevel.VARDOU.

            use_ffmpeg (bool, optional):
                Will use flac if false.
                Defaults to True.

            flac_args (Optional[List[str]], optional):
                Additionnal arguments. Defaults to None.
        """
        if use_ffmpeg:
            binary = 'ffmpeg'
            if level == FlacCompressionLevel.VARDOU:
                level_args = ['-compression_level', '12', '-lpc_type', 'cholesky',
                              '-lpc_passes', '3', '-exact_rice_parameters', '1']
            else:
                level_args = [f'-compression_level {level}']
            settings = ['-i', '{a_src_cut:s}', *level_args]
            if flac_args is not None:
                settings.append(*flac_args)
            settings += ['{a_enc_cut:s}']
        else:
            binary = 'flac'
            if level <= FlacCompressionLevel.EIGHT:
                if flac_args is not None:
                    settings = [*flac_args]
                else:
                    settings = []
                settings = [f'-{level}', '-o', '{a_enc_cut:s}', '{a_src_cut:s}']
            else:
                raise ValueError('FlacEncoder: "level" must be <= 8 if use_ffmpeg is false')
        super().__init__(binary, settings, file, track=track, xml_tag=xml_tag)


class AudioCutter:
    """Audio cutter using eztrim"""
    file: FileInfo
    track: int
    kwargs: Dict[str, Any]

    def __init__(self, file: FileInfo, /, *, track: int, **kwargs: Any) -> None:
        """
        Args:
            file (FileInfo):
                FileInfo object.

            track (int):
                Track number.
        """
        self.file = file
        if track > 0:
            self.track = track
        else:
            raise ValueError('AudioEncoder: `track` must be > 0')
        self.kwargs = kwargs

    def run(self) -> None:
        """Run eztrim"""
        assert self.file.a_src
        assert self.file.a_src_cut

        if not self.file.frame_start:
            self.file.frame_start = 0

        eztrim(self.file.clip, (self.file.frame_start, self.file.frame_end),
               self.file.a_src.format(self.track).to_str(), self.file.a_src_cut.format(self.track).to_str(),
               **self.kwargs)





def progress_update_func(value: int, endvalue: int) -> None:
    """Callback function used in clip.output"""
    return print(f"\rVapourSynth: {value}/{endvalue} ~ {100 * value // endvalue}% || Encoder: ", end="")


class VideoEncoder(Tool):
    """VideoEncoder interface"""
    progress_update: Optional[UpdateFunc]

    file: FileInfo
    clip: vs.VideoNode

    def __init__(self, binary: AnyPath, settings: Union[AnyPath, List[str], Dict[str, Any]], /,
                 progress_update: Optional[UpdateFunc] = progress_update_func) -> None:
        """Helper intended to facilitate video encoding

        Args:
            binary (str):
                Path to your binary file.

            settings (Union[Path, List[str]]):
                Path to your settings file or list of string containing your settings.

            progress_update (Optional[UpdateFunc], optional):
                Current progress can be reported by passing a callback function
                of the form func(current_frame, total_frames) to progress_update.
                Defaults to progress_update_func.
        """
        self.progress_update = progress_update

        super().__init__(binary, settings)

    def run_enc(self, clip: vs.VideoNode, file: Optional[FileInfo], *, y4m: bool = True) -> None:
        """Run encoding"""
        if file:
            self.file = file

        self.clip = clip

        self._get_settings()

        if file and self.file.do_qpfile:
            self._create_qpfile()
            self.params += ['--qpfile', self.file.qpfile.to_str()]

        self._do_encode(y4m)

    def run(self) -> NoReturn:
        raise NameError('Use `run_enc` instead')

    def set_variable(self) -> Dict[str, Any]:
        try:
            return dict(clip_output=self.file.name_clip_output.to_str(), filename=self.file.name)
        except AttributeError:
            return {}

    def _create_qpfile(self) -> None:
        if not (qpfile := self.file.qpfile).exists():
            scenes = find_scene_changes(self.file.clip_cut, SceneChangeMode.WWXD_SCXVID_UNION)

            with qpfile.open('w') as qpf:
                qpf.writelines([f"{s} K\n" for s in scenes])

    def _do_encode(self, y4m: bool) -> None:
        Status.info('VideoEncoder command: ' + ' '.join(self.params))

        with subprocess.Popen(self.params, stdin=subprocess.PIPE) as process:
            self.clip.output(cast(BinaryIO, process.stdin), y4m=y4m, progress_update=self.progress_update)


class VideoLanEncoder(VideoEncoder, ABC):
    """Abstract VideoEncoder interface for VideoLan based encoders such as x265 and x264"""

    def __init__(self, binary: AnyPath, settings: Union[AnyPath, List[str], Dict[str, Any]], /,
                 zones: Optional[Dict[Tuple[int, int], Dict[str, Any]]] = None,
                 progress_update: Optional[UpdateFunc] = progress_update_func) -> None:
        """
        Args:
            settings (Union[AnyPath, List[str], Dict[str, Any]]):
                Path to your settings file or list of string or a dict containing your settings.

            Example:
                ::

                    # This
                    >>>cat settings
                    >>>-o {clip_output:s} - --y4m --preset slower --crf 51

                    # is equivalent to this:
                    settings: List[str] = ['-o', '{clip_output:s}', '-', '--y4m', '--preset', 'slower', '--crf', '51']

                    # and is equivalent to this:
                    settings: Dict[str, Any] = {
                        '-o': '{clip_output:s}',
                        '-': None,
                        '--y4m': None,
                        '--preset': 'slower',
                        '--crf': 51
                    }

            zones (Optional[Dict[Tuple[int, int], Dict[str, Any]]], optional):
                Custom zone ranges. Defaults to None.
            Example:
                ::

                    zones: Dict[Tuple[int, int], Dict[str, Any]] = {
                        (3500, 3600): dict(b=3, subme=11),
                        (4800, 4900): {'psy-rd': '0.40:0.05', 'merange': 48}
                    }

            progress_update (Optional[UpdateFunc], optional):
                Current progress can be reported by passing a callback function
                of the form func(current_frame, total_frames) to progress_update.
                Defaults to progress_update_func.
        """
        super().__init__(binary, settings, progress_update=progress_update)
        if zones:
            zones_settings: str = ''
            for i, ((start, end), opt) in enumerate(zones.items()):
                zones_settings += f'{start},{end}'
                for opt_name, opt_val in opt.items():
                    zones_settings += f',{opt_name}={opt_val}'
                if i != len(zones) - 1:
                    zones_settings += '/'
            self.params += ['--zones', zones_settings]


class X265Encoder(VideoLanEncoder):
    """Video encoder using x265 in HEVC"""

    def __init__(self, settings: Union[AnyPath, List[str], Dict[str, Any]], /,
                 zones: Optional[Dict[Tuple[int, int], Dict[str, Any]]] = None,
                 progress_update: Optional[UpdateFunc] = progress_update_func) -> None:
        super().__init__('x265', settings, zones, progress_update=progress_update)

    def set_variable(self) -> Dict[str, Any]:
        assert self.clip.format
        min_luma, max_luma = Properties.get_color_range(self.params, self.clip)
        return dict(clip_output=self.file.name_clip_output.to_str(), filename=self.file.name, frames=self.clip.num_frames,
                    fps_num=self.clip.fps.numerator, fps_den=self.clip.fps.denominator,
                    bits=self.clip.format.bits_per_sample,
                    min_luma=min_luma, max_luma=max_luma)


class X264Encoder(VideoLanEncoder):
    """Video encoder using x264 in AVC"""

    def __init__(self, settings: Union[AnyPath, List[str], Dict[str, Any]], /,
                 zones: Optional[Dict[Tuple[int, int], Dict[str, Any]]] = None,
                 progress_update: Optional[UpdateFunc] = progress_update_func) -> None:
        super().__init__('x264', settings, zones, progress_update=progress_update)

    def set_variable(self) -> Dict[str, Any]:
        assert self.clip.format
        csp = Properties.get_csp(self.clip)
        return dict(clip_output=self.file.name_clip_output.to_str(), filename=self.file.name, frames=self.clip.num_frames,
                    fps_num=self.clip.fps.numerator, fps_den=self.clip.fps.denominator,
                    bits=self.clip.format.bits_per_sample, csp=csp)


class LosslessEncoder(VideoEncoder):
    """Video encoder for lossless encoding"""

    def __init__(self, binary: AnyPath, settings: Union[AnyPath, List[str], Dict[str, Any]], /,
                 progress_update: Optional[UpdateFunc] = None) -> None:
        super().__init__(binary, settings, progress_update=progress_update)

    def set_variable(self) -> Dict[str, Any]:
        assert self.clip.format
        return dict(clip_output_lossless=self.file.name_clip_output_lossless.to_str(),
                    bits=self.clip.format.bits_per_sample)


class NvenccEncoder(LosslessEncoder):
    def __init__(self) -> None:
        """"""
        super().__init__(
            'nvencc',
            ['-i', '-', '--y4m',
             '--lossless',
             '-c', 'hevc',
             '--output-depth', '{bits:d}',
             '-o', '{clip_output_lossless:s}'],
            progress_update=None
        )


class FFV1Encoder(LosslessEncoder):
    def __init__(self, *, threads: int = 16) -> None:
        """"""
        super().__init__(
            'ffmpeg',
            ['-i', '-',
             '-vcodec', 'ffv1',
             '-coder', '1', '-context', '0', '-g', '1', '-level', '3',
             '-threads', str(threads), '-slices', '24', '-slicecrc', '1', '-slicecrc', '1',
             '{clip_output_lossless:s}'],
            progress_update=None
        )


class Stream(ABC):
    path: VPath

    def __init__(self, path: AnyPath) -> None:
        self.path = VPath(path)

    def __repr__(self) -> str:
        return pformat(vars(self), indent=1, width=80, sort_dicts=True)


class MediaStream(Stream, ABC):
    name: Optional[str] = None
    lang: Lang = UNDEFINED
    tag_file: Optional[VPath] = None

    def __init__(self, path: AnyPath, name: Optional[str] = None,
                 lang: Lang = UNDEFINED, tag_file: Optional[AnyPath] = None) -> None:
        super().__init__(path)
        self.name = name
        self.lang = lang
        self.tag_file = VPath(tag_file) if tag_file is not None else tag_file


class VideoStream(MediaStream):
    pass


class AudioStream(MediaStream):
    pass


class ChapterStream(Stream):
    lang: Lang = UNDEFINED
    charset: Optional[str] = None

    def __init__(self, path: AnyPath,
                 lang: Lang = UNDEFINED, charset: Optional[str] = None) -> None:
        super().__init__(path)
        self.lang = lang
        self.charset = charset




class Mux:
    """Muxing interface using mkvmerge"""
    output: VPath

    file: FileInfo

    video: VideoStream
    audios: Optional[List[AudioStream]]
    chapters: Optional[ChapterStream]

    mkvmerge_path: VPath = VPath('mkvmerge')

    __workfiles: Set[VPath]

    def __init__(
        self, file: FileInfo,
        streams: Optional[
            Tuple[
                VideoStream,
                Optional[Union[AudioStream, Sequence[AudioStream]]],
                Optional[ChapterStream]
            ]
        ] = None
    ) -> None:
        """
            If `streams` is not specified:
                - Will find `file.name_file_final` as VideoStream
                - Will try to find in this order file.a_enc_cut, file.a_src_cut, file.a_src as long as there is a file.a_xxxx.format(n)
                - All languages are set to `und` and names to None.
            Otherwise will mux the `streams` to `file.name_file_final`.
        """
        self.output = file.name_file_final


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
        cmd = ['-o', self.output.to_str()]

        self.__workfiles = set()


        cmd += self._video_cmd()


        if self.audios is not None:
            cmd += self._audios_cmd()
        else:
            self.audios = []
            i = 1
            while True:
                if self.file.a_enc_cut is not None and self.file.a_enc_cut.format(i).exists():
                    self.audios += [AudioStream(self.file.a_enc_cut.format(i))]
                elif self.file.a_src_cut is not None and self.file.a_src_cut.format(i).exists():
                    self.audios += [AudioStream(self.file.a_src_cut.format(i))]
                elif self.file.a_src is not None and self.file.a_src.format(i).exists():
                    self.audios += [AudioStream(self.file.a_src.format(i))]
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

        BasicTool(self.mkvmerge_path.to_str(), cmd).run()

        return self.__workfiles


    def _video_cmd(self) -> List[str]:
        cmd: List[str] = []
        if self.video.tag_file:
            cmd += ['--tags', '0:' + self.video.tag_file.to_str()]
        if self.video.name:
            cmd += ['--track-name', '0:' + self.video.name]
        cmd += ['--language', '0:' + self.video.lang.iso639, self.video.path.to_str()]
        self.__workfiles.add(self.video.path)
        return cmd

    def _audios_cmd(self) -> List[str]:
        cmd: List[str] = []
        assert self.audios
        for audio in self.audios:
            if audio.tag_file:
                cmd += ['--tags', '0:' + audio.tag_file.to_str()]
            if audio.name:
                cmd += ['--track-name', '0:' + audio.name]
            cmd += ['--language', '0:' + audio.lang.iso639, audio.path.to_str()]
            self.__workfiles.add(audio.path)
        return cmd

    def _chapters_cmd(self) -> List[str]:
        assert self.chapters
        cmd = ['--chapter-language', self.chapters.lang.iso639]
        if self.chapters.charset:
            cmd += ['--chapter-charset', self.chapters.charset]
        cmd += ['--chapters', self.chapters.path.to_str()]
        self.__workfiles.add(self.chapters.path)
        return cmd


class Tooling:
    BasicTool: Type[BasicTool] = BasicTool

    AudioEncoder: Type[AudioEncoder] = AudioEncoder
    QAACEncoder: Type[QAACEncoder] = QAACEncoder
    OpusEncoder: Type[OpusEncoder] = OpusEncoder
    FlacEncoder: Type[FlacEncoder] = FlacEncoder

    AudioCutter: Type[AudioCutter] = AudioCutter
    VideoEncoder: Type[VideoEncoder] = VideoEncoder
    X265Encoder: Type[X265Encoder] = X265Encoder
    X264Encoder: Type[X264Encoder] = X264Encoder
    LosslessEncoder: Type[LosslessEncoder] = LosslessEncoder

    Mux: Type[Mux] = Mux
    VideoStream: Type[VideoStream] = VideoStream
    AudioStream: Type[AudioStream] = AudioStream
    ChapterStream: Type[ChapterStream] = ChapterStream
