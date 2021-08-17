"""Tooling module"""

from __future__ import annotations

__all__ = [
    'Tool', 'BasicTool',
    'AudioExtracter', 'MKVAudioExtracter', 'Eac3toAudioExtracter', 'FfmpegAudioExtracter',

    'AudioEncoder', 'BitrateMode', 'QAACEncoder', 'OpusEncoder', 'FDKAACEncoder', 'FlacCompressionLevel', 'FlacEncoder',
    'PassthroughAudioEncoder',

    'AudioCutter', 'EztrimCutter', 'SoxCutter', 'PassthroughCutter',
    'VideoEncoder', 'X265Encoder', 'X264Encoder', 'LosslessEncoder', 'NvenccEncoder', 'FFV1Encoder',
    'progress_update_func',
    'Mux', 'Stream', 'MediaStream', 'VideoStream', 'AudioStream', 'ChapterStream',
]

import asyncio
import os
import re
import subprocess
import sys
import traceback
from abc import ABC, abstractmethod
from enum import Enum, IntEnum, auto
from pprint import pformat
from shutil import copyfile
from typing import (Any, BinaryIO, Dict, List, Literal, NoReturn, Optional,
                    Sequence, Set, Tuple, Union, cast)

import vapoursynth as vs
from acsuite import eztrim
from lvsfunc.render import SceneChangeMode, find_scene_changes
from lxml import etree
from pymediainfo import MediaInfo
from vardefunc.util import normalise_ranges

from .binary_path import BinaryPath
from .config import FileInfo
from .language import UNDEFINED, Lang
from .status import Status
from .timeconv import Convert
from .types import AnyPath, DuplicateFrame, Trim, UpdateFunc
from .utils import Properties, copy_docstring_from, recursive_dict
from .vpathlib import VPath


class Tool(ABC):
    """
    Abstract Tool interface
    Most of the tools inherit from it
    """

    binary: VPath
    """Binary path"""

    settings: Union[AnyPath, List[str], Dict[str, Any]]
    """
    Path to your settings file or list of string or a dict containing your settings.

    .. code-block:: python

        # This
        >>> cat settings
        -o {clip_output:s} - --y4m --preset slower --crf 51

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
    """

    params: List[str]
    """Settings normalised and parsed"""

    def __init__(self, binary: AnyPath, settings: Union[AnyPath, List[str], Dict[str, Any]]) -> None:
        """
        :param binary:
        :param settings:
        """
        self.binary = VPath(binary)
        self.settings = settings
        self.params = []
        super().__init__()

    @abstractmethod
    def run(self) -> Union[None, NoReturn]:
        """Tooling chain"""

    @abstractmethod
    def set_variable(self) -> Dict[str, Any]:
        """Set variables in the settings"""

    def _get_settings(self) -> None:
        if isinstance(self.settings, dict):
            for k, v in self.settings.items():
                self.params += [k] + ([str(v)] if v else [])
        elif isinstance(self.settings, list):
            self.params += self.settings
        else:
            try:
                with open(self.settings, 'r') as sttgs:
                    params_re = re.split(r'[\n\s]\s*', sttgs.read())
            except FileNotFoundError as file_err:
                Status.fail(
                    f'{self.__class__.__name__}: settings file not found',
                    exception=FileNotFoundError, chain_err=file_err
                )
            self.params += [p for p in params_re if isinstance(p, str)]

        self._check_binary()

        params_parsed: List[str] = []
        for p in self.params:
            # pylint: disable=W0702
            try:
                p = p.format(**self.set_variable())
            except AttributeError:
                Status.warn(f'{self.__class__.__name__}: param {p} is not a str object; trying to convert to str...')
                p = str(p).format(**self.set_variable())
            except:  # noqa: E722
                excp_type, excp_val, trback = sys.exc_info()
                Status.fail(
                    f'{self.__class__.__name__}: Unexpected exception from the following traceback:\n'
                    + ''.join(traceback.format_tb(trback))
                    + (excp_type.__name__ if excp_type else Exception.__name__) + ': '
                    + str(excp_val), exception=Exception, chain_err=excp_val
                )
            params_parsed.append(p)
        self.params.clear()
        self.params = [self.binary.to_str()] + params_parsed

    def _check_binary(self) -> None:
        try:
            subprocess.call(self.binary.to_str(), stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        except FileNotFoundError as file_not_found:
            Status.fail(
                f'{self.__class__.__name__}: "{self.binary.to_str()}" was not found!',
                exception=FileNotFoundError, chain_err=file_not_found
            )


class BasicTool(Tool):
    """BasicTool interface"""

    file: Optional[FileInfo]
    """FileInfo object."""

    def __init__(self, binary: AnyPath, settings: Union[AnyPath, List[str], Dict[str, Any]], /,
                 file: Optional[FileInfo] = None) -> None:
        """
        Helper allowing the use of CLI programs for basic tasks like video or audio track extraction.

        :param binary:          See :py:attr:`Tool.binary`
        :param settings:        See :py:attr:`Tool.settings`
        :param file:            Not used in BasicTool implementation, defaults to None
        """
        self.file = file
        super().__init__(binary, settings)

    def run(self) -> None:
        self._get_settings()
        self._do_tooling()

    def set_variable(self) -> Dict[str, Any]:
        return {}

    def _do_tooling(self) -> None:
        Status.info(f'{self.binary.to_str()} command: ' + ' '.join(self.params))
        subprocess.run(self.params, check=True, text=True, encoding='utf-8')


class AudioExtracter(BasicTool):
    """Audio extracter interface"""

    file: FileInfo
    """FileInfo object"""

    track_in: Sequence[int]
    """Track number of the input file"""

    track_out: Sequence[int]
    """Track number of the output file"""

    def __init__(self, binary: AnyPath, settings: Union[AnyPath, List[str], Dict[str, Any]], /, file: FileInfo) -> None:
        """
        Base class for audio extration

        :param binary:          See :py:attr:`Tool.binary`
        :param settings:        See :py:attr:`Tool.settings`
        :param file:            FileInfo object, needed
        """
        if file.a_src is None:
            Status.fail(f'{self.__class__.__name__}: `file.a_src` is needed!', exception=ValueError)
        super().__init__(binary, settings, file=file)


class _AutoSetTrack(AudioExtracter, ABC):
    def __init__(self, binary: AnyPath, settings: List[str], /, file: FileInfo,
                 track_in: Union[int, Sequence[int]] = -1, track_out: Union[int, Sequence[int]] = -1) -> None:

        track_in = [track_in] if isinstance(track_in, int) else track_in
        track_out = [track_out] if isinstance(track_out, int) else track_out

        if len(track_in) != len(track_out):
            Status.fail(f'{self.__class__.__name__}: number of `track_in` and `track_out` must be the same!')
        if any(t < 0 for t in track_in) or any(t < 0 for t in track_out):
            Status.fail(f'{self.__class__.__name__}: `track_in` and `track_out` must be > 0', exception=ValueError)

        self.track_in = track_in
        self.track_out = track_out

        super().__init__(binary, settings, file=file)

    def run(self) -> None:
        self._get_settings()
        self.set_tracks_number()
        self._do_tooling()

    @abstractmethod
    def set_tracks_number(self) -> None:
        """Internal function for setting the track(s) number"""

    def set_variable(self) -> Dict[str, Any]:
        return dict(path=self.file.path.to_str())


class _SimpleSetTrack(_AutoSetTrack, ABC):
    def set_tracks_number(self) -> None:
        assert self.file.a_src
        # Set the tracks for eac3to and mkvmerge since they share the same pattern
        for t_in, t_out in zip(self.track_in, self.track_out):
            self.params.append(f'{t_in}:{self.file.a_src.set_track(t_out).to_str():s}')


class _FfmpegSetTrack(_AutoSetTrack, ABC):
    def set_tracks_number(self) -> None:
        # ffmpeg is a bit more annoying since it can't guess the bitdepth
        # I'm using mediainfo here because it's already implemented in FileInfo
        # but I guess using ffprobe could be nice too.
        acodecs = {24: 'pcm_s24le', 16: 'pcm_s16le'}

        assert self.file.a_src

        media_info = self.file.media_info.to_data()
        try:
            mi_tracks = media_info['tracks']
        except AttributeError as attr_err:
            Status.fail(
                f'{self.__class__.__name__}: can\'t find any tracks in this file',
                exception=AttributeError, chain_err=attr_err
            )

        for t_in, t_out in zip(self.track_in, self.track_out):
            if mi_tracks[1 + t_in]['track_type'] == 'Audio':
                try:
                    t_format = mi_tracks[1 + t_in]['format']
                except AttributeError as attr_err:
                    Status.fail(
                        f'{self.__class__.__name__}: can\'t find the format of the track number "{t_in}"!',
                        exception=AttributeError, chain_err=attr_err
                    )
                if t_format in {'PCM', 'DTS'}:
                    ac = acodecs[int(mi_tracks[1 + t_in]['bit_depth'])]
                else:
                    ac = 'copy'
                self.params += ['-map', f'0:{t_in}', '-acodec', ac, self.file.a_src.set_track(t_out).to_str()]
            else:
                Status.fail(
                    f'{self.__class__.__name__}: specified track number "{t_in}" is not a audio type track!',
                    exception=ValueError
                )


class MKVAudioExtracter(_SimpleSetTrack):
    """AudioExtracter using MKVExtract"""

    def __init__(self, file: FileInfo, /, *,
                 track_in: Union[int, Sequence[int]] = -1, track_out: Union[int, Sequence[int]] = -1,
                 mkvextract_args: Optional[List[str]] = None) -> None:
        """
        :param file:                FileInfo object, needed
        :param track_in:            Input track(s) number
        :param track_out:           Output track(s) number
        :param mkvextract_args:     https://mkvtoolnix.download/doc/mkvextract.html, defaults to None
        """
        settings = ['{path:s}', '--abort-on-warnings', 'tracks'] + (mkvextract_args if mkvextract_args is not None else [])
        super().__init__(BinaryPath.mkvextract, settings, file, track_in=track_in, track_out=track_out)


class Eac3toAudioExtracter(_SimpleSetTrack):
    """AudioExtracter using Eac3to"""

    def __init__(self, file: FileInfo, /, *,
                 track_in: Union[int, Sequence[int]] = -1, track_out: Union[int, Sequence[int]] = -1,
                 eac3to_args: Optional[List[str]] = None) -> None:
        """
        :param file:                FileInfo object, needed
        :param track_in:            Input track(s) number
        :param track_out:           Output track(s) number
        :param eac3to_args:         https://en.wikibooks.org/wiki/Eac3to/How_to_Use, defaults to None
        """
        settings = ['{path:s}']
        super().__init__(BinaryPath.eac3to, settings, file, track_in=track_in, track_out=track_out)
        self.params.extend(eac3to_args if eac3to_args else [])


class FfmpegAudioExtracter(_FfmpegSetTrack):
    """AudioExtracter using Ffmpeg"""

    _ffmpeg_warning = ['-hide_banner', '-loglevel', 'info']

    def __init__(self, file: FileInfo, /, *,
                 track_in: Union[int, Sequence[int]] = -1, track_out: Union[int, Sequence[int]] = -1) -> None:
        """
        :param file:                FileInfo object, needed
        :param track_in:            Input track(s) number
        :param track_out:           Output track(s) number
        """
        settings = self._ffmpeg_warning + ['-i', '{path:s}', '-y']
        super().__init__(BinaryPath.ffmpeg, settings, file, track_in=track_in, track_out=track_out)


class AudioEncoder(BasicTool):
    """BasicTool interface for audio encoding"""

    file: FileInfo
    """FileInfo object"""

    track: int
    """Track number"""

    xml_tag: Optional[AnyPath]
    """
    XML tags suitable for mkvmerge
    Curently only write the encoder name
    More info here: https://mkvtoolnix.download/doc/mkvmerge.html#mkvmerge.tags
    """

    _ffmpeg_info = ['-hide_banner', '-loglevel', 'info']

    def __init__(self, binary: AnyPath, settings: Union[AnyPath, List[str], Dict[str, Any]], /,
                 file: FileInfo, *, track: int = -1, xml_tag: Optional[AnyPath] = None) -> None:
        """
        Helper for audio extraction.

        :param binary:          See :py:attr:`Tool.binary`
        :param settings:        See :py:attr:`Tool.settings`
        :param file:            FileInfo object, needed.
        :param track:           Track number
        :param xml_tag:         See :py:attr:`AudioEncoder.xml_tag`, defaults to None
                                If specified, will write a file containing the encoder info to be passed to the muxer.
        """
        super().__init__(binary, settings, file=file)

        if self.file.a_src_cut is None:
            Status.fail(f'{self.__class__.__name__}: `file.a_src_cut` is needed!', exception=ValueError)
        if self.file.a_enc_cut is None:
            Status.fail(f'{self.__class__.__name__}: `file.a_enc_cut` is needed!', exception=ValueError)

        if track > 0:
            self.track = track
        else:
            Status.fail(f'{self.__class__.__name__}: `track` must be > 0', exception=ValueError)
        self.xml_tag = xml_tag

    def run(self) -> None:
        self._get_settings()
        self._do_tooling()
        if self.xml_tag:
            self._write_encoder_name_file()

    def set_variable(self) -> Dict[str, Any]:
        assert self.file.a_src_cut
        assert self.file.a_enc_cut
        return dict(
            a_src_cut=self.file.a_src_cut.set_track(self.track).to_str(),
            a_enc_cut=self.file.a_enc_cut.set_track(self.track).to_str()
        )

    def _write_encoder_name_file(self) -> None:
        assert (a_enc_cut := self.file.a_enc_cut)

        tags = etree.Element('Tags')
        tag = etree.SubElement(tags, 'Tag')
        _ = etree.SubElement(tag, 'Targets')
        simple = etree.SubElement(tag, 'Simple')
        etree.SubElement(simple, 'Name').text = 'ENCODER'
        etree.SubElement(simple, 'String').text = Properties.get_encoder_name(a_enc_cut.set_track(self.track))

        assert self.xml_tag
        with open(self.xml_tag, 'wb') as f:
            f.write(
                etree.tostring(tags, encoding='utf-8', xml_declaration=True, pretty_print=True)
            )


class PassthroughAudioEncoder(AudioEncoder):
    """Special AudioEncoder that will copy :py:attr:`FileInfo.a_src_cut` to :py:attr:`FileInfo.a_enc_cut`"""

    def __init__(self, /, file: FileInfo, *, track: int = -1) -> None:
        """
        :param file:        FileInfo object
        :param track:       Track number
        :param xml_tag:     See :py:attr:`AudioEncoder.xml_tag`, defaults to None
        """
        super().__init__('', [''], file, track=track)

    def run(self) -> None:
        assert self.file.a_src_cut
        assert self.file.a_enc_cut

        Status.info(f'{self.__class__.__name__}: copying audio...')
        copyfile(
            self.file.a_src_cut.set_track(self.track).absolute().to_str(),
            self.file.a_enc_cut.set_track(self.track).absolute().to_str()
        )


class BitrateMode(Enum):
    """Common bitrate mode enumeration"""

    ABR = auto()
    """Average BitRate"""

    CBR = auto()
    """Constant BitRate"""

    VBR = auto()
    """Variable BitRate"""

    CVBR = auto()
    """Constrained Variable BitRate"""

    TVBR = auto()
    """True Variable BitRate"""

    HARD_CBR = CBR
    """Hard Constant BitRate"""

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}.{self.name}>'


QAAC_BITRATE_MODE = Literal[BitrateMode.ABR, BitrateMode.CBR, BitrateMode.CVBR, BitrateMode.TVBR]
OPUS_BITRATE_MODE = Literal[BitrateMode.VBR, BitrateMode.CVBR, BitrateMode.HARD_CBR]
FDK_BITRATE_MODE = Literal[BitrateMode.CBR, BitrateMode.VBR]


class QAACEncoder(AudioEncoder):
    """AudioEncoder using QAAC, an open-source wrapper for Core Audio's AAC and ALAC encoder"""

    _bitrate_mode_map: Dict[BitrateMode, str] = {
        BitrateMode.ABR: '--abr',
        BitrateMode.CBR: '--cbr',
        BitrateMode.CVBR: '--cvbr',
        BitrateMode.TVBR: '--tvbr'
    }

    def __init__(self, /, file: FileInfo, *,
                 track: int = -1, mode: QAAC_BITRATE_MODE = BitrateMode.TVBR, bitrate: int = 127,
                 xml_tag: Optional[AnyPath] = None, qaac_args: Optional[List[str]] = None) -> None:
        """
        These following options are automatically added:

            - ``--no-delay --no-optimize --threading``

        :param file:            FileInfo object
        :param track:           Track number
        :param mode:            Bitrate mode. QAAC supports ABR, CBR, CVBR and TVBR, defaults to BitrateMode.TVBR
        :param bitrate:         Matches the bitrate for ABR, CBR and CVBR in kbit/s and quality Q for TVBR, defaults to 127
        :param xml_tag:         See :py:attr:`AudioEncoder.xml_tag`, defaults to None
        :param qaac_args:       Additional options, see https://github.com/nu774/qaac/wiki/Command-Line-Options, defaults to None
        """
        settings = ['{a_src_cut:s}']
        # There is a Literal type but just in case never underestimate the people's stupidity
        try:
            settings += [self._bitrate_mode_map[mode]]
        except AttributeError as attr_err:
            Status.fail(
                f'{self.__class__.__name__}: The mode "{mode._name_}" is not supported!',
                exception=TypeError, chain_err=attr_err
            )
        settings += [str(bitrate), '--no-delay', '--no-optimize', '--threading', '-o', '{a_enc_cut:s}']

        if qaac_args is not None:
            settings += qaac_args

        super().__init__(BinaryPath.qaac, settings, file, track=track, xml_tag=xml_tag)


class OpusEncoder(AudioEncoder):
    """AudioEncoder using Opus, open, royalty-free, highly versatile audio codec """

    _bitrate_mode_opusenc_map: Dict[BitrateMode, str] = {
        BitrateMode.VBR: '--vbr',
        BitrateMode.CVBR: '--cvbr',
        BitrateMode.HARD_CBR: '--hard-cbr',
    }
    _bitrate_mode_ffmpeg_map: Dict[BitrateMode, str] = {
        BitrateMode.VBR: 'on',
        BitrateMode.CVBR: 'constrained',
        BitrateMode.HARD_CBR: 'off',
    }

    def __init__(self, /, file: FileInfo, *,
                 track: int = -1, mode: OPUS_BITRATE_MODE = BitrateMode.VBR, bitrate: int = 160,
                 xml_tag: Optional[AnyPath] = None, use_ffmpeg: bool = True, opus_args: Optional[List[str]] = None) -> None:
        """
        :param file:            FileInfo object
        :param track:           Track number
        :param mode:            Bitrate mode. libopus supports VBR, CVBR, and HARD_CBR (aka CBR), defaults to BitrateMode.VBR
        :param bitrate:         Target bitrate in kbit/s, defaults to 160
        :param xml_tag:         See :py:attr:`AudioEncoder.xml_tag`, defaults to None
        :param use_ffmpeg:      Use ``opusenc`` if False, defaults to True
        :param opus_args:       Additionnal arguments, defaults to None
        """
        if use_ffmpeg:
            binary = BinaryPath.ffmpeg
            settings = self._ffmpeg_info + ['-i', '{a_src_cut:s}', '-c:a', 'libopus', '-b:a', f'{bitrate}k', '-vbr']
            settings += self._set_mode(self._bitrate_mode_ffmpeg_map, mode, opus_args)
            settings += ['-o', '{a_enc_cut:s}']
        else:
            binary = BinaryPath.opusenc
            settings = ['--bitrate', str(bitrate)]
            settings += self._set_mode(self._bitrate_mode_opusenc_map, mode, opus_args)
            settings += ['{a_src_cut:s}', '{a_enc_cut:s}']
        super().__init__(binary, settings, file, track=track, xml_tag=xml_tag)

    def _set_mode(self, layout_map: Dict[BitrateMode, str], mode: OPUS_BITRATE_MODE, opus_args: Optional[List[str]]) -> List[str]:
        settings: List[str] = []
        # There is a Literal type but just in case never underestimate the people's stupidity
        try:
            settings += [layout_map[mode]]
        except AttributeError as attr_err:
            Status.fail(
                f'{self.__class__.__name__}: The mode "{mode._name_}" is not supported!',
                exception=TypeError, chain_err=attr_err
            )
        if opus_args is not None:
            settings += opus_args
        return settings


class FDKAACEncoder(AudioEncoder):
    """
    AudioEncoder using fdkaac.
    The libfdk-aac library is based on the Fraunhofer FDK AAC code from the Android project
    """

    def __init__(self, /, file: FileInfo, *,
                 track: int = -1, mode: FDK_BITRATE_MODE = BitrateMode.CBR, bitrate: int = 256, cutoff: int = 20000,
                 xml_tag: Optional[AnyPath] = None, use_ffmpeg: bool = True, fdk_args: Optional[List[str]] = None) -> None:
        # pylint: disable=line-too-long
        """
        :param file:            FileInfo object
        :param track:           Track number
        :param mode:            Bitrate mode, fdkaac supports CBR and VBR, defaults to BitrateMode.CBR
        :param bitrate:         Matches the bitrate for CBR in kbit/s and quality Q for VBR, defaults to 256
        :param cutoff:          Set cutoff frequency. If not specified (or explicitly set to 0) it will use a value automatically computed by the library.  # noqa: E501
                                Correspond to frequency bandwidth in Hz in fdkaac library, defaults to 20000
        :param xml_tag:         See :py:attr:`AudioEncoder.xml_tag`, defaults to None
        :param use_ffmpeg:      Use ``fdkaac`` if False, defaults to True
        :param fdk_args:        Additional options see https://www.ffmpeg.org/ffmpeg-codecs.html#Options-11
                                or https://github.com/nu774/fdkaac/blob/master/README, defaults to None
        """
        # pylint: enable=line-too-long
        if use_ffmpeg:
            binary = BinaryPath.ffmpeg
            settings = self._ffmpeg_info + ['-i', '{a_src_cut:s}', '-c:a', 'libfdk_aac', '-cutoff', str(cutoff)]
            settings += self._set_mode(mode, bitrate, fdk_args, ['-b:a', f'{bitrate}k'], ['-vbr', f'{bitrate}'])
            settings += ['{a_enc_cut:s}']
        else:
            binary = BinaryPath.fdkaac
            settings = ['{a_src_cut:s}', '--bandwidth', str(cutoff)]
            settings += self._set_mode(mode, bitrate, fdk_args, ['--bitrate', str(bitrate)], ['--bitrate-mode', str(bitrate)])
            settings += ['-o', '{a_enc_cut:s}']

        super().__init__(binary, settings, file, track=track, xml_tag=xml_tag)

    def _set_mode(self, mode: FDK_BITRATE_MODE, bitrate: int, fdk_args: Optional[List[str]],
                  cbr_settings: List[str], vbr_settings: List[str]) -> List[str]:
        settings: List[str] = []
        # CBR Mode
        if mode == BitrateMode.CBR:
            settings += cbr_settings
        # VBR Mode
        elif mode == BitrateMode.VBR:
            if bitrate in range(1, 6):
                settings += vbr_settings
            else:
                Status.fail(
                    f'{self.__class__.__name__}: when using vbr mode, quality should be > 0 and <= 5!',
                    exception=ValueError
                )
        # Pretty sure this is useless
        else:
            Status.fail(f'{self.__class__.__name__}: mode not supported!', exception=TypeError)
        # Additional argument
        if fdk_args is not None:
            settings += fdk_args
        return settings


class FlacCompressionLevel(IntEnum):
    """
    Flac compression level.
    Keep in mind that the max FLAC can handle is 8 and ffmpeg 12
    """
    ZERO = 0
    """
    ffmpeg: compression_level 0
    flac: --compression-level-0
    """
    ONE = 1
    """
    ffmpeg: compression_level 1
    flac: --compression-level-1
    """
    TWO = 2
    """
    ffmpeg: compression_level 2
    flac: --compression-level-2
    """
    THREE = 3
    """
    ffmpeg: compression_level 3
    flac: --compression-level-3
    """
    FOUR = 4
    """
    ffmpeg: compression_level 4
    flac: --compression-level-4
    """
    FIVE = 5
    """
    ffmpeg: compression_level 5
    flac: --compression-level-5
    This is default for both ffmpeg and flac encoders
    """
    SIX = 6
    """
    ffmpeg: compression_level 6
    flac: --compression-level-6
    """
    SEVEN = 7
    """
    ffmpeg: compression_level 7
    flac: --compression-level-7
    """
    EIGHT = 8
    """
    ffmpeg: compression_level 8
    flac: --compression-level-8
    """
    NINE = 9
    """
    ffmpeg: compression_level 9
    """
    TEN = 10
    """
    ffmpeg: compression_level 10
    """
    ELEVEN = 11
    """
    ffmpeg: compression_level 11
    """
    TWELVE = 12
    """
    ffmpeg: compression_level 12
    """
    FAST = 0
    """
    Fastest compression. Currently synonymous with 0
    ffmpeg: compression_level 0
    flac: --compression-level-0
    """
    BEST = 8
    """
    Highest compression. Currently synonymous with -8
    ffmpeg: compression_level 0
    flac: --compression-level-0
    """
    VARDOU = 99
    """
    My custom ffmpeg command
    .. code-block:: python

        ['-compression_level', '12', '-lpc_type', 'cholesky', '-lpc_passes', '3', '-exact_rice_parameters', '1']

    """


class FlacEncoder(AudioEncoder):
    """AudioEncoder using FLAC, Free Lossless Audio Codec"""

    def __init__(self, file: FileInfo, *,
                 track: int = -1, xml_tag: Optional[AnyPath] = None,
                 level: FlacCompressionLevel = FlacCompressionLevel.VARDOU,
                 use_ffmpeg: bool = True, flac_args: Optional[List[str]] = None) -> None:
        """
        :param file:            FileInfo object
        :param track:           Track number
        :param xml_tag:         See :py:attr:`AudioEncoder.xml_tag`, defaults to None
        :param level:           See :py:class:`FlacCompressionLevel` for all levels available,
                                defaults to FlacCompressionLevel.VARDOU
        :param use_ffmpeg:      Will use flac if false, defaults to True
        :param flac_args:       Additionnal arguments, defaults to None
        """
        if use_ffmpeg:
            binary = BinaryPath.ffmpeg
            if level == FlacCompressionLevel.VARDOU:
                level_args = ['-compression_level', '12', '-lpc_type', 'cholesky',
                              '-lpc_passes', '3', '-exact_rice_parameters', '1']
            else:
                level_args = [f'-compression_level {level}']
            settings = ['-i', '{a_src_cut:s}'] + level_args
            if flac_args is not None:
                settings.extend(flac_args)
            settings.append('{a_enc_cut:s}')
        else:
            binary = BinaryPath.flac
            if level <= FlacCompressionLevel.EIGHT:
                settings = [*flac_args] if flac_args is not None else []
                settings.extend([f'-{level}', '-o', '{a_enc_cut:s}', '{a_src_cut:s}'])
            else:
                Status.fail(f'{self.__class__.__name__}: "level" must be <= 8 if "use_ffmpeg" is false', exception=ValueError)
        super().__init__(binary, settings, file, track=track, xml_tag=xml_tag)


class AudioCutter(ABC):
    """Abstract interface implementing audio trimming"""

    file: FileInfo
    """FileInfo object"""
    track: int
    """Track number"""
    kwargs: Dict[str, Any]
    """Additionnal arguments"""

    def __init__(self, file: FileInfo, /, *, track: int, **kwargs: Any) -> None:
        """
        :param file:        FileInfo object
        :param track:       Track number
        :param kwargs:      Additionnal arguments
        """
        self.file = file

        if not self.file.a_src:
            Status.fail(f'{self.__class__.__name__}: `file.a_src` is not a valid path!', exception=ValueError)
        if not self.file.a_src_cut:
            Status.fail(f'{self.__class__.__name__}: `file.a_src_cut` is not a valid path!', exception=ValueError)

        if track > 0:
            self.track = track
        else:
            Status.fail(f'{self.__class__.__name__}: `track` must be > 0', exception=ValueError)
        self.kwargs = kwargs

    @abstractmethod
    def run(self) -> None:
        """Trimming toolchain"""

    @classmethod
    @abstractmethod
    def generate_silence(
        cls, s: float, output: AnyPath,
        num_ch: int = 2, sample_rate: int = 48000, bitdepth: int = 16
    ) -> Union[None, NoReturn]:
        """
        Generate silence if supported by the current interface

        :param s:               Seconds
        :param output:          Output file path
        :param num_ch:          Number of channels, defaults to 2
        :param sample_rate:     Sample rate in Hz, defaults to 48000
        :param bitdepth:        Bit depth, defaults to 16
        """

    @staticmethod
    def _cleanup(*files: AnyPath) -> None:
        for f in files:
            try:
                os.remove(f)
            except FileNotFoundError:
                pass



FFMPEG_CHANNEL_LAYOUT_MAP: Dict[int, str] = {
    1: 'mono',
    2: 'stereo',
    6: '5.1'
}
"""
Dictionary containing the channel layout map of ffmpeg
More information here: https://ffmpeg.org/doxygen/1.2/channel__layout_8c_source.html
Only "mono", "stereo" and "5.1" are currently supported
"""


class EztrimCutter(AudioCutter):
    """
    AudioCutter using :py:func:`acsuite.eztrim`
    It fallbacks on :py:func:`EztrimCutter.ezpztrim` if some DuplicateFrame objects are detected
    in the FileInfo object specified.
    """
    force_eztrim: bool = False
    """
    Force using :py:func:`acsuite.eztrim`
    Keep in mind that if you don't specify DuplicateFrame objects in the FileInfo object
    eztrim will be used anyway.
    """

    _ffmpeg_warning = ['-hide_banner', '-loglevel', 'warning']

    def run(self) -> None:
        assert self.file.a_src
        assert self.file.a_src_cut

        trims = self.file.trims_or_dfs

        if trims:
            if isinstance(trims, tuple):
                trims = [trims]
            Status.info(f'{self.__class__.__name__}: trimming audio...')

            if self.force_eztrim or not any(isinstance(t, DuplicateFrame) for t in trims):
                self.kwargs.setdefault('quiet', True)
                eztrim(
                    self.file.clip, cast(List[Trim], trims),
                    self.file.a_src.set_track(self.track).to_str(),
                    self.file.a_src_cut.set_track(self.track).to_str(),
                    **self.kwargs
                )
            else:
                Status.warn(f'{self.__class__.__name__}: DuplicateFrame(s) detected...')
                self.ezpztrim(
                    self.file.a_src.set_track(self.track),
                    self.file.a_src_cut.set_track(self.track),
                    trims, self.file.clip
                )
        else:
            Status.warn(f'{self.__class__.__name__}: no trims detected; use PassthroughCutter...')
            PassthroughCutter(self.file, track=self.track).run()

    @classmethod
    def ezpztrim(
        cls, src: AnyPath, output: AnyPath, /,
        trims: Union[Trim, DuplicateFrame, List[Trim], List[Union[Trim, DuplicateFrame]]],
        ref_clip: vs.VideoNode, *,
        combine: bool = True, cleanup: bool = True
    ) -> None:
        """
        Simple trimming function that follows VapourSynth/Python slicing syntax.
        End frame is NOT inclusive.

        :param src:             Input file
        :param output:          Output file
        :param trims:           Either a list of 2-tuples, one tuple of 2 ints, a DuplicateFrame object
                                or a list of of 2-tuples and/or DuplicateFrame object.
        :param ref_clip:        Vapoursynth clip used to determine framerate AND the number of frames.
        :param combine:         Keep all performed trims in the same file, defaults to True
        :param cleanup:         Delete temporary files, defaults to True
        """
        src, output = map(VPath, (src, output))

        if not isinstance(trims, list):
            trims = [trims]

        media_info = cast(MediaInfo, MediaInfo.parse(src)).to_data()
        try:
            ext = media_info['tracks'][0]['file_extension']
            srate = media_info['tracks'][1]['sampling_rate']
            bitrate = media_info['tracks'][0]['overall_bit_rate']
            nb_ch = media_info['tracks'][1]['channel_s']
        except AttributeError as att_err:
            Status.fail(
                f'{cls.__name__}: file extension, sampling rate, bitrate or num channels not found',
                exception=AttributeError, chain_err=att_err
            )

        parent = output.parent
        tmp_name = output.name + '_tmp_{track_number}' + src.suffix
        tmp = parent / tmp_name

        tmp_files: Set[AnyPath] = set()
        fps = ref_clip.fps
        f2ts = Convert.f2ts

        for i, trim in enumerate(trims):
            if isinstance(trim, tuple):
                start, end = normalise_ranges(ref_clip, trim).pop()
                # Just trim
                BasicTool(
                    BinaryPath.ffmpeg,
                    cls._ffmpeg_warning
                    + ['-i', src.to_str(), '-vn', '-ss', f2ts(start, fps), '-to', f2ts(end, fps)]
                    + ['-c:a', 'copy', '-rf64', 'auto']
                    + [tmp.set_track(i).to_str()]
                ).run()
                tmp_files.add(tmp.set_track(i))
            else:
                # Handle DuplicateFrame
                df = trim
                tmp_silence = tmp.with_name(tmp.name + '_silence.wav')
                # Generate silence
                cls.generate_silence(
                    Convert.f2seconds(df.dup, fps), tmp_silence.set_track(i),
                    nb_ch, srate
                )
                tmp_files.add(tmp_silence.set_track(i))
                # Encode in source format
                BasicTool(
                    BinaryPath.ffmpeg,
                    cls._ffmpeg_warning
                    + ['-i', tmp_silence.set_track(i).to_str()]
                    + ['-acodec', str(ext), '-ab', str(bitrate), tmp.set_track(i).to_str()]
                ).run()
                tmp_files.add(tmp.set_track(i))

        if combine:
            # Get the trimmed files
            concat_files = sorted(output.parent.glob(tmp_name.format(track_number='?')))
            # Write a config concat file
            # paths should be in poxix format and space character escaped
            # this is so annoying
            with open('_conf_concat.txt', 'w') as _conf_concat:
                _conf_concat.writelines(
                    'file file:{}\n'.format(af.as_posix().replace(" ", "\\ "))
                    for af in concat_files
                )
            BasicTool(
                BinaryPath.ffmpeg,
                cls._ffmpeg_warning
                + ['-f', 'concat', '-safe', '0', '-i', '_conf_concat.txt', '-c', 'copy', output.to_str()]
            ).run()

        if cleanup:
            cls._cleanup(*tmp_files, '_conf_concat.txt')

        del tmp_files

    @classmethod
    def generate_silence(
        cls, s: float, output: AnyPath,
        num_ch: int = 2, sample_rate: int = 48000, bitdepth: int = 16
    ) -> None:
        try:
            channel_layout = FFMPEG_CHANNEL_LAYOUT_MAP[num_ch]
        except AttributeError as att_err:
            Status.fail(f'{cls.__name__}: channel layout unknown!', exception=ValueError, chain_err=att_err)

        BasicTool(
            BinaryPath.ffmpeg,
            cls._ffmpeg_warning
            + ['-f', 'lavfi', '-i', f'anullsrc=channel_layout={channel_layout}:sample_rate={sample_rate}']
            + ['-t', str(s), VPath(output).with_suffix('.wav').to_str()]
        ).run()


class SoxCutter(AudioCutter):
    """Audio cutter using Sox"""

    def run(self) -> None:
        assert self.file.a_src
        assert self.file.a_src_cut

        trims = self.file.trims_or_dfs

        if trims:
            Status.info(f'{self.__class__.__name__}: trimming audio...')
            self.soxtrim(
                self.file.a_src.set_track(self.track),
                self.file.a_src_cut.set_track(self.track),
                trims, self.file.clip
            )
        else:
            Status.warn(f'{self.__class__.__name__}: no detected trims; use PassthroughCutter...')
            PassthroughCutter(self.file, track=self.track).run()

    @classmethod
    def soxtrim(
        cls, src: AnyPath, output: AnyPath, /,
        trims: Union[Trim, DuplicateFrame, List[Trim], List[Union[Trim, DuplicateFrame]]],
        ref_clip: vs.VideoNode, *,
        combine: bool = True, cleanup: bool = True
    ) -> None:
        """
        Simple trimming function that follows VapourSynth/Python slicing syntax.
        End frame is NOT inclusive.

        :param src:             Input file
        :param output:          Output file
        :param trims:           Either a list of 2-tuples, one tuple of 2 ints, a DuplicateFrame object
                                or a list of of 2-tuples and/or DuplicateFrame object.
        :param ref_clip:        Vapoursynth clip used to determine framerate AND the number of frames.
        :param combine:         Keep all performed trims in the same file, defaults to True
        :param cleanup:         Delete temporary files, defaults to True
        """
        src, output = map(VPath, (src, output))

        if not isinstance(trims, list):
            trims = [trims]

        media_info = cast(MediaInfo, MediaInfo.parse(src)).to_data()
        try:
            srate = media_info['tracks'][1]['sampling_rate']
            bitdepth = media_info['tracks'][1]['bit_depth']
            nb_ch = media_info['tracks'][1]['channel_s']
        except AttributeError as att_err:
            Status.fail(
                f'{cls.__name__}: sampling rate, bit_depth or channel_s not found',
                exception=AttributeError, chain_err=att_err
            )

        parent = output.parent
        tmp_name = output.name + '_tmp_{track_number}.wav'
        tmp = parent / tmp_name

        tmp_files: Set[AnyPath] = set()
        fps = ref_clip.fps
        f2s = Convert.f2seconds

        for i, trim in enumerate(trims):
            if isinstance(trim, tuple):
                start, end = normalise_ranges(ref_clip, trim).pop()
                BasicTool(
                    BinaryPath.sox,
                    [src.to_str(), tmp.set_track(i).to_str(),
                     'trim', str(f2s(start, fps)), str(f2s(end - start, fps))]
                ).run()
                tmp_files.add(tmp.set_track(i))
            else:
                df = trim
                # Generate silence
                cls.generate_silence(
                    Convert.f2seconds(df.dup, fps), tmp.set_track(i).to_str(),
                    nb_ch, srate, bitdepth
                )
                tmp_files.add(tmp.set_track(i).to_str())

        if combine:
            tmps = sorted(output.parent.glob(tmp_name.format(track_number='?')))
            BasicTool(
                BinaryPath.sox,
                ['--combine', 'concatenate', *[t.to_str() for t in tmps], output.to_str()]
            ).run()

        if cleanup:
            cls._cleanup(*tmp_files)

        del tmp_files

    @classmethod
    def generate_silence(
        cls, s: float, output: AnyPath,
        num_ch: int = 2, sample_rate: int = 48000, bitdepth: int = 16
    ) -> None:
        BasicTool(
            BinaryPath.sox,
            ['-n', '-r', str(sample_rate), '-c', str(num_ch), '-b', str(bitdepth),
             VPath(output).with_suffix('.wav').to_str(), 'trim', '0.0', str(s)]
        ).run()


class PassthroughCutter(AudioCutter):
    """Special AudioCutter that will copy :py:attr:`FileInfo.a_src` to :py:attr:`FileInfo.a_src_cut`"""

    def run(self) -> None:
        assert self.file.a_src
        assert self.file.a_src_cut
        Status.info(f'{self.__class__.__name__}: copying audio...')
        copyfile(
            self.file.a_src.set_track(self.track).absolute().to_str(),
            self.file.a_src_cut.set_track(self.track).absolute().to_str()
        )

    @classmethod
    def generate_silence(
        cls, s: float, output: AnyPath,
        num_ch: int = 2, sample_rate: int = 48000, bitdepth: int = 16
    ) -> NoReturn:
        """You can't generate silence from this class"""
        raise NotImplementedError



def progress_update_func(value: int, endvalue: int) -> None:
    """
    Callback function used in clip.output

    :param value:       Current value
    :param endvalue:    End value
    """
    return print(f"\rVapourSynth: {value}/{endvalue} ~ {100 * value // endvalue}% || Encoder: ", end="")


class VideoEncoder(Tool):
    """General VideoEncoder interface"""

    progress_update: Optional[UpdateFunc]
    """"Progress update function to be used in `vapoursynth.VideoNode.output`"""

    file: FileInfo
    """FileInfo object"""

    clip: vs.VideoNode
    """Your filtered VideoNode clip"""

    def __init__(self, binary: AnyPath, settings: Union[AnyPath, List[str], Dict[str, Any]], /,
                 progress_update: Optional[UpdateFunc] = progress_update_func) -> None:
        """
        :param binary:              Path to your binary file.
        :param settings:            Path to your settings file or list of string or a dict containing your settings.
                                    See :py:attr:`Tool.settings`
        :param progress_update:     Current progress can be reported by passing a callback function
                                    of the form func(current_frame, total_frames) to progress_update,
                                    defaults to progress_update_func
        """
        self.progress_update = progress_update
        super().__init__(binary, settings)

    def run_enc(self, clip: vs.VideoNode, file: Optional[FileInfo], *, y4m: bool = True) -> None:
        """
        Run encoding toolchain

        :param clip:            Clip to be encoded
        :param file:            FileInfo object
        :param y4m:             Add YUV4MPEG2 headers, defaults to True
                                More informations http://www.vapoursynth.com/doc/pythonreference.html#VideoNode.output
        """
        if file:
            self.file = file

        self.clip = clip

        self._get_settings()

        if file and self.file.do_qpfile:
            self._create_qpfile()
            self.params += ['--qpfile', self.file.qpfile.to_str()]

        self._do_encode(y4m)

    def run(self) -> NoReturn:
        """
        Shouldn't be used in VideoEncoder object.
        Use :py:func:`run_enc` instead
        """
        Status.fail(f'{self.__class__.__name__}: Use `run_enc` instead', exception=NameError)

    def set_variable(self) -> Dict[str, Any]:
        try:
            return dict(clip_output=self.file.name_clip_output.to_str(), filename=self.file.name)
        except AttributeError:
            return {}

    def _create_qpfile(self) -> None:
        if not (qpfile := self.file.qpfile).exists():
            scenes = find_scene_changes(self.file.clip_cut, SceneChangeMode.WWXD_SCXVID_UNION)

            with qpfile.open('w') as qpf:
                qpf.writelines(f"{s} K\n" for s in scenes)
        else:
            Status.warn(f'{self.__class__.__name__}: a qpfile already exists at {self.file.qpfile.resolve().to_str()}')

    def _do_encode(self, y4m: bool) -> None:
        Status.info(f'{self.__class__.__name__} command: ' + ' '.join(self.params))

        with subprocess.Popen(self.params, stdin=subprocess.PIPE) as process:
            self.clip.output(cast(BinaryIO, process.stdin), y4m=y4m, progress_update=self.progress_update)


class LosslessEncoder(VideoEncoder):
    """Video encoder for lossless encoding"""

    @copy_docstring_from(VideoEncoder.__init__)
    def __init__(self, binary: AnyPath, settings: Union[AnyPath, List[str], Dict[str, Any]], /,
                 progress_update: Optional[UpdateFunc] = None) -> None:
        super().__init__(binary, settings, progress_update=progress_update)

    def set_variable(self) -> Dict[str, Any]:
        assert self.clip.format
        try:
            return dict(
                clip_output_lossless=self.file.name_clip_output_lossless.to_str(),
                bits=self.clip.format.bits_per_sample
            )
        except AttributeError:
            return {}


class NvenccEncoder(LosslessEncoder):
    def __init__(self) -> None:
        """
        Built-in NvencC encoder
        Lossless mode in HEVC. Hardcoded path: 'nvencc'
        """
        super().__init__(
            BinaryPath.nvencc,
            ['-i', '-', '--y4m',
             '--lossless',
             '-c', 'hevc',
             '--output-depth', '{bits:d}',
             '-o', '{clip_output_lossless:s}'],
            progress_update=None
        )


class FFV1Encoder(LosslessEncoder):
    def __init__(self, *, threads: int = 16) -> None:
        """
        Built-in FFV1 encoder. Lossless mode in FFV1.
        """
        super().__init__(
            BinaryPath.ffmpeg,
            ['-i', '-',
             '-vcodec', 'ffv1',
             '-coder', '1', '-context', '0', '-g', '1', '-level', '3',
             '-threads', str(threads), '-slices', '24', '-slicecrc', '1', '-slicecrc', '1',
             '{clip_output_lossless:s}'],
            progress_update=None
        )


class VideoLanEncoder(VideoEncoder, ABC):
    """Abstract VideoEncoder interface for VideoLan based encoders such as x265 and x264"""

    @copy_docstring_from(VideoEncoder.__init__, 'o+t')
    def __init__(self, binary: AnyPath, settings: Union[AnyPath, List[str], Dict[str, Any]], /,
                 zones: Optional[Dict[Tuple[int, int], Dict[str, Any]]] = None,
                 progress_update: Optional[UpdateFunc] = progress_update_func) -> None:
        """
        :param zones:       Custom zone ranges, defaults to None

        .. code-block:: python

            zones: Dict[Tuple[int, int], Dict[str, Any]] = {
                        (3500, 3600): dict(b=3, subme=11),
                        (4800, 4900): {'psy-rd': '0.40:0.05', 'merange': 48}
                    }
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

    def set_variable(self) -> Dict[str, Any]:
        if (bits := Properties.get_depth(self.clip)) > 10:
            Status.warn(f'{self.__class__.__name__}: Bitdepth is > 10. Are you sure about that?')
        try:
            return dict(
                clip_output=self.file.name_clip_output.to_str(), filename=self.file.name, frames=self.clip.num_frames,
                fps_num=self.clip.fps.numerator, fps_den=self.clip.fps.denominator, bits=bits
            )
        except AttributeError:
            return {}


class X265Encoder(VideoLanEncoder):
    """Video encoder using x265 in HEVC"""

    @copy_docstring_from(VideoLanEncoder.__init__)
    def __init__(self, settings: Union[AnyPath, List[str], Dict[str, Any]], /,
                 zones: Optional[Dict[Tuple[int, int], Dict[str, Any]]] = None,
                 progress_update: Optional[UpdateFunc] = progress_update_func) -> None:
        super().__init__(BinaryPath.x265, settings, zones, progress_update=progress_update)

    def set_variable(self) -> Dict[str, Any]:
        min_luma, max_luma = Properties.get_color_range(self.params, self.clip)
        return super().set_variable() | dict(min_luma=min_luma, max_luma=max_luma)



class X264Encoder(VideoLanEncoder):
    """Video encoder using x264 in AVC"""

    @copy_docstring_from(VideoLanEncoder.__init__)
    def __init__(self, settings: Union[AnyPath, List[str], Dict[str, Any]], /,
                 zones: Optional[Dict[Tuple[int, int], Dict[str, Any]]] = None,
                 progress_update: Optional[UpdateFunc] = progress_update_func) -> None:
        super().__init__(BinaryPath.x264, settings, zones, progress_update=progress_update)

    def set_variable(self) -> Dict[str, Any]:
        return super().set_variable() | dict(csp=Properties.get_csp(self.clip))


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
    """Class representing a media stream to be passed to mkvmerge"""

    name: Optional[str] = None
    """Stream's name"""

    lang: Lang = UNDEFINED
    """Stream's language"""

    tag_file: Optional[VPath] = None
    """XML tag file"""

    def __init__(self, path: AnyPath, name: Optional[str] = None,
                 lang: Lang = UNDEFINED, tag_file: Optional[AnyPath] = None) -> None:
        """
        Register a MediaStream with its associated informations

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
    """Muxing interface using mkvmerge"""

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

            - Will find :py:attr:`FileInfo.name_file_final` as VideoStream
            - Will try to find in this order :py:attr:`FileInfo.a_enc_cut`, :py:attr:`FileInfo.a_src_cut`,
              :py:attr:`FileInfo.a_src` as long as there is a ``file.a_xxxx.set_track(n)``
            - All languages are set to ``und`` and names to ``None``.

        Otherwise will mux the ``streams`` to :py:attr:`FileInfo.name_file_final`.

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



class SubProcessAsync:
    sem: asyncio.Semaphore

    def __init__(self, cmds: List[str], /, *, nb_cpus: Optional[int] = os.cpu_count()) -> None:
        if nb_cpus:
            self.sem = asyncio.Semaphore(nb_cpus)
        else:
            Status.fail(f'{self.__class__.__name__}: no CPU found!', exception=ValueError)

        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(self._processing(cmds))
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

    async def _processing(self, all_cmds: List[str]) -> None:
        await asyncio.gather(
            *(asyncio.ensure_future(self._safe_processing(cmd)) for cmd in all_cmds)
        )

    async def _safe_processing(self, cmd: str) -> None:
        async with self.sem:
            return await self._run_cmd(cmd)

    @staticmethod
    async def _run_cmd(cmd: str) -> None:
        proc = await asyncio.create_subprocess_shell(cmd)
        await proc.communicate()
