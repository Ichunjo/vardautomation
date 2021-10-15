
__all__ = [
    'AudioExtracter', 'MKVAudioExtracter', 'Eac3toAudioExtracter', 'FFmpegAudioExtracter',

    'AudioEncoder', 'BitrateMode', 'QAACEncoder', 'OpusEncoder', 'FDKAACEncoder', 'FlacCompressionLevel', 'FlacEncoder',
    'PassthroughAudioEncoder',

    'AudioCutter', 'EztrimCutter', 'SoxCutter', 'PassthroughCutter',
]

import os
from abc import ABC, abstractmethod
from enum import Enum, IntEnum, auto
from shutil import copyfile
from typing import (Any, Dict, List, Literal, NoReturn, Optional, Sequence,
                    Set, Union)

import numpy as np
import vapoursynth as vs
from acsuite import eztrim
from lxml import etree
from numpy.typing import NDArray
from pymediainfo import MediaInfo
from typing_extensions import TypeGuard
from vardefunc.util import normalise_ranges

from ..binary_path import BinaryPath
from ..config import FileInfo
from ..status import FileError, Status
from ..timeconv import Convert
from ..types import AnyPath, DuplicateFrame, Trim
from ..utils import Properties
from ..vpathlib import VPath
from .base import BasicTool


class AudioExtracter(BasicTool):
    """Audio base extracter interface for audio extration"""

    file: FileInfo
    """FileInfo object"""

    track_in: Sequence[int]
    """Track number(s) of the input file"""

    track_out: Sequence[int]
    """Track number(s) of the output file"""

    def __init__(self, binary: AnyPath, settings: Union[AnyPath, List[str], Dict[str, Any]], /, file: FileInfo) -> None:
        """
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
        self._set_tracks_number()
        self._do_tooling()

    @abstractmethod
    def _set_tracks_number(self) -> None:
        """Internal function for setting the track(s) number"""

    def set_variable(self) -> Dict[str, Any]:
        return dict(path=self.file.path.to_str())


class _SimpleSetTrack(_AutoSetTrack, ABC):
    def _set_tracks_number(self) -> None:
        assert self.file.a_src
        # Set the tracks for eac3to and mkvmerge since they share the same pattern
        for t_in, t_out in zip(self.track_in, self.track_out):
            self.params.append(f'{t_in}:{self.file.a_src.set_track(t_out).to_str():s}')


class _FfmpegSetTrack(_AutoSetTrack, ABC):
    def _set_tracks_number(self) -> None:
        # ffmpeg is a bit more annoying since it can't guess the bitdepth
        # I'm using mediainfo here because it's already implemented in FileInfo
        # but I guess using ffprobe could be nice too.

        # TODO: yes I should use FFprobe because of weird bugs Light reported where
        # indexing was different between mediainfo and ffmpeg
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


class FFmpegAudioExtracter(_FfmpegSetTrack):
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
    """BasicTool interface helper for audio encoding"""

    file: FileInfo
    """FileInfo object"""

    track: int
    """Track number"""

    xml_tag: Optional[AnyPath]
    """
    XML tags suitable for mkvmerge\n
    Curently only write the encoder name\n
    More info here: https://mkvtoolnix.download/doc/mkvmerge.html#mkvmerge.tags
    """

    _ffmpeg_info = ['-hide_banner', '-loglevel', 'info']

    def __init__(self, binary: AnyPath, settings: Union[AnyPath, List[str], Dict[str, Any]], /,
                 file: FileInfo, *, track: int = -1, xml_tag: Optional[AnyPath] = None) -> None:
        """
        :param binary:          See :py:attr:`Tool.binary`
        :param settings:        See :py:attr:`Tool.settings`
        :param file:            FileInfo object, needed.
        :param track:           Track number
        :param xml_tag:         See :py:attr:`AudioEncoder.xml_tag`, defaults to None\n
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
        with open(self.xml_tag, 'wb', encoding='utf-8') as f:
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
    """AudioEncoder using QAAC, an open-source wrapper for Core Audio's AAC and ALAC encoder."""

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
        # There is a Literal type but just in case never underestimate people's stupidity
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
    """AudioEncoder using Opus, open, royalty-free, highly versatile audio codec."""

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
    AudioEncoder using fdkaac.\n
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
        :param cutoff:          Set cutoff frequency. If not specified (or explicitly set to 0)
                                it will use a value automatically computed by the library.
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
    Flac compression level.\n
    Keep in mind that the max FLAC can handle is 8 and ffmpeg 12
    """
    ZERO = 0
    """
    ffmpeg: compression_level 0\n
    flac: --compression-level-0
    """
    ONE = 1
    """
    ffmpeg: compression_level 1\n
    flac: --compression-level-1
    """
    TWO = 2
    """
    ffmpeg: compression_level 2\n
    flac: --compression-level-2
    """
    THREE = 3
    """
    ffmpeg: compression_level 3\n
    flac: --compression-level-3
    """
    FOUR = 4
    """
    ffmpeg: compression_level 4\n
    flac: --compression-level-4
    """
    FIVE = 5
    """
    ffmpeg: compression_level 5\n
    flac: --compression-level-5\n
    This is the default for both ffmpeg and flac encoders
    """
    SIX = 6
    """
    ffmpeg: compression_level 6\n
    flac: --compression-level-6
    """
    SEVEN = 7
    """
    ffmpeg: compression_level 7\n
    flac: --compression-level-7
    """
    EIGHT = 8
    """
    ffmpeg: compression_level 8\n
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
    Fastest compression. Currently synonymous with 0\n
    ffmpeg: compression_level 0\n
    flac: --compression-level-0
    """
    BEST = 8
    """
    Highest compression. Currently synonymous with -8\n
    ffmpeg: compression_level 0\n
    flac: --compression-level-0
    """
    VARDOU = 99
    """
    My custom ffmpeg command\n

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
                level_args = [
                    '-compression_level', '12', '-lpc_type', 'cholesky',
                    '-lpc_passes', '3', '-exact_rice_parameters', '1'
                ]
            else:
                level_args = [f'-compression_level {level}']
            settings = ['-i', '{a_src_cut:s}'] + level_args
            if flac_args is not None:
                settings.extend(flac_args)
            settings.append('{a_enc_cut:s}')
        else:
            binary = BinaryPath.flac
            if level <= FlacCompressionLevel.EIGHT:
                settings = flac_args if flac_args is not None else []
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

    def _passthrough(self) -> None:
        Status.warn(f'{self.__class__.__name__}: no trims detected; use PassthroughCutter...')
        PassthroughCutter(self.file, track=self.track).run()

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


class ScipyCutter(AudioCutter):
    """Audio cutter using scipy.io.wavfile module"""

    _BITDEPTH: Dict[int, Any] = {
        32: np.int32,
        16: np.int16,
        8: np.uint8
    }

    def __init__(self, file: FileInfo, /, *, track: int, **kwargs: Any) -> None:
        try:
            import scipy as _  # type: ignore  # noqa F401
        except ImportError as imp_err:
            Status.fail(
                f'{self.__class__.__name__}: you need to install scipy to use this cutter!',
                exception=ImportError, chain_err=imp_err
            )
        super().__init__(file, track=track, **kwargs)

    def run(self) -> None:
        assert self.file.a_src
        assert self.file.a_src_cut

        trims = self.file.trims_or_dfs

        if trims:
            Status.info(f'{self.__class__.__name__}: trimming audio...')
            self.scipytrim(
                self.file.a_src.set_track(self.track),
                self.file.a_src_cut.set_track(self.track),
                trims, self.file.clip
            )
        else:
            self._passthrough()

    @classmethod
    def scipytrim(
        cls, src: AnyPath, output: AnyPath, /,
        trims: Union[Trim, DuplicateFrame, List[Trim], List[Union[Trim, DuplicateFrame]]],
        ref_clip: vs.VideoNode, *, combine: bool = True
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
        """
        try:
            from scipy.io import wavfile  # type: ignore
        except ImportError as imp_err:
            Status.fail(
                f'{cls.__name__}: you need to install scipy to use this cutter!',
                exception=ImportError, chain_err=imp_err
            )

        src, output = map(VPath, (src, output))

        if not isinstance(trims, list):
            trims = [trims]

        try:
            sample_rate, array = wavfile.read(src, False)
        except ValueError as val_err:
            Status.fail(
                f'{cls.__name__}: this file is not a wav!',
                exception=FileError, chain_err=val_err
            )

        parent = output.parent
        tmp_name = output.name + '_tmp_{track_number}' + src.suffix
        tmp = parent / tmp_name

        fps = ref_clip.fps
        f2samples = Convert.f2samples

        arrays: List[NDArray[Any]] = []
        for trim in trims:
            if isinstance(trim, tuple):
                start, end = normalise_ranges(ref_clip, trim).pop()
                # Just trim
                arrays.append(
                    array[f2samples(start, fps, sample_rate), f2samples(end, fps, sample_rate)]
                )
            else:
                # Handle DuplicateFrame
                df = trim
                _, channels = array.shape
                arrays.append(
                    np.zeros((f2samples(df.dup, fps, sample_rate), channels), array.dtype)  # type: ignore
                )

        if combine:
            narray = arrays.pop() if len(arrays) == 1 else np.concatenate(arrays, axis=0)  # type: ignore
            wavfile.write(output, sample_rate, narray)
            del narray
        else:
            for i, arr in enumerate(arrays):
                wavfile.write(tmp.set_track(i), sample_rate, arr)
        del arrays

    @classmethod
    def generate_silence(
        cls, s: float, output: AnyPath,
        num_ch: int = 2, sample_rate: int = 48000, bitdepth: int = 16
    ) -> None:
        try:
            from scipy.io import wavfile  # type: ignore
        except ImportError as imp_err:
            Status.fail(
                f'{cls.__name__}: you need to install scipy to use this cutter!',
                exception=ImportError, chain_err=imp_err
            )

        silence_arr = np.array(  # type: ignore
            [(0, ) * num_ch] * Convert.seconds2samples(s, sample_rate), cls._BITDEPTH[bitdepth]
        )
        wavfile.write(output, sample_rate, silence_arr)


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
    AudioCutter using :py:func:`acsuite.eztrim`.\n
    It fallbacks on :py:func:`EztrimCutter.ezpztrim` if some DuplicateFrame objects are detected
    in the FileInfo object specified.
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

            if self._are_trims_only(trims):
                self.kwargs.setdefault('quiet', True)
                eztrim(
                    self.file.clip, trims,
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
            self._passthrough()

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

        media_info = MediaInfo.parse(src).to_data()
        try:
            ext = media_info['tracks'][0]['file_extension']
            srate = media_info['tracks'][1]['sampling_rate']
            bitrate = media_info['tracks'][0]['overall_bit_rate']
            nb_ch = media_info['tracks'][1]['channel_s']
        except (AttributeError, KeyError) as att_err:
            Status.fail(
                f'{cls.__name__}: file extension, sampling rate, bitrate or num channels not found',
                exception=FileError, chain_err=att_err
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
            cls.combine(concat_files, output)

        if cleanup:
            cls._cleanup(*tmp_files)

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

    @classmethod
    def combine(cls, files: List[VPath], output: AnyPath) -> None:
        # Write a config concat file
        # paths should be in poxix format and space character escaped
        # this is so annoying
        with open('_conf_concat.txt', 'w', encoding='utf-8') as _conf_concat:
            _conf_concat.writelines(
                # pylint: disable=consider-using-f-string
                'file file:{}\n'.format(af.as_posix().replace(" ", "\\ "))
                for af in files
            )
        BasicTool(
            BinaryPath.ffmpeg,
            cls._ffmpeg_warning
            + ['-f', 'concat', '-safe', '0', '-i', '_conf_concat.txt', '-c', 'copy', str(output)]
        ).run()

        cls._cleanup('_conf_concat.txt')

    @staticmethod
    def _are_trims_only(trims_or_dfs: Union[List[Trim], List[Union[Trim, DuplicateFrame]]]) -> TypeGuard[List[Trim]]:
        return not any(isinstance(t, DuplicateFrame) for t in trims_or_dfs)


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
            self._passthrough()

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

        media_info = MediaInfo.parse(src).to_data()
        try:
            srate = media_info['tracks'][1]['sampling_rate']
            bitdepth = media_info['tracks'][1]['bit_depth']
            nb_ch = media_info['tracks'][1]['channel_s']
        except (AttributeError, KeyError) as att_err:
            Status.fail(
                f'{cls.__name__}: sampling rate, bit_depth or channel_s not found',
                exception=FileError, chain_err=att_err
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
    """
    Special AudioCutter that will copy :py:attr:`vardautomation.config.FileInfo.a_src`
    to :py:attr:`vardautomation.config.FileInfo.a_src_cut`
    """

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
