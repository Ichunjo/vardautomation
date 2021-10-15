
__all__ = [
    'VideoEncoder', 'VideoLanEncoder', 'X265Encoder', 'X264Encoder', 'LosslessEncoder', 'NvenccEncoder', 'FFV1Encoder',
    'progress_update_func'
]

import subprocess
from abc import ABC
from typing import (Any, BinaryIO, Dict, List, NoReturn, Optional, Tuple,
                    Union, cast)

import vapoursynth as vs

from ..binary_path import BinaryPath
from ..config import FileInfo
from ..status import Status
from ..types import AnyPath, UpdateFunc
from ..utils import Properties, copy_docstring_from
from .abstract import Tool


def progress_update_func(value: int, endvalue: int) -> None:
    """
    Callback function used in clip.output

    :param value:       Current value
    :param endvalue:    End value
    """
    # pylint: disable=consider-using-f-string
    return print(
        "\rVapourSynth: %i/%i ~ %.2f%% || Encoder: " % (
            value, endvalue, 100 * value / endvalue
        ),
        end=""
    )


class VideoEncoder(Tool):
    """General VideoEncoder interface"""

    file: FileInfo
    """FileInfo object"""

    clip: vs.VideoNode
    """Your filtered VideoNode clip"""

    y4m: bool = True
    """
    YUV4MPEG2 headers\n
    More informations http://www.vapoursynth.com/doc/pythonreference.html#VideoNode.output
    """

    progress_update: Optional[UpdateFunc] = progress_update_func
    """Progress update function to be used in `vapoursynth.VideoNode.output`"""

    prefetch: int = 0
    """Max number of concurrent rendered frames"""

    backlog: int = -1
    """
    Defines how many unconsumed frames (including those that did not finish rendering yet)
    vapoursynth buffers at most before it stops rendering additional frames.\n
    This argument is there to limit the memory this function uses storing frames.
    """

    def run_enc(self, clip: vs.VideoNode, file: Optional[FileInfo]) -> None:
        """
        Run encoding toolchain

        :param clip:            Clip to be encoded
        :param file:            FileInfo object
        """
        if file:
            self.file = file

        self.clip = clip

        self._get_settings()
        self._do_encode()

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

    def _do_encode(self) -> None:
        Status.info(f'{self.__class__.__name__} command: ' + ' '.join(self.params))
        with subprocess.Popen(self.params, stdin=subprocess.PIPE) as process:
            self.clip.output(cast(BinaryIO, process.stdin), self.y4m, self.progress_update, self.prefetch, self.backlog)


class LosslessEncoder(VideoEncoder):
    """Video encoder for lossless encoding"""

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
    """Built-in NvencC encoder."""

    def __init__(self) -> None:
        """
        Use NvencC to output a lossless encode in HEVC
        """
        super().__init__(
            BinaryPath.nvencc,
            ['-i', '-', '--y4m', '--lossless', '-c', 'hevc', '--output-depth', '{bits:d}', '-o', '{clip_output_lossless:s}'],
        )
        self.progress_update = None


class FFV1Encoder(LosslessEncoder):
    """Built-in FFV1 encoder."""

    def __init__(self, *, threads: int = 0) -> None:
        """
        Use FFmpeg to output a lossless encode in FFV1

        :param threads:         Number of threads to be used, defaults to 0 (auto selection)
        """
        super().__init__(
            BinaryPath.ffmpeg,
            ['-i', '-', '-vcodec', 'ffv1', '-coder', '1', '-context', '0', '-g', '1', '-level', '3',
             '-threads', str(threads), '-slices', '24', '-slicecrc', '1', '-slicecrc', '1',
             '{clip_output_lossless:s}'],
        )
        self.progress_update = None


class VideoLanEncoder(VideoEncoder, ABC):
    """Abstract VideoEncoder interface for VideoLan based encoders such as x265 and x264."""

    @copy_docstring_from(Tool.__init__, 'o+t')
    def __init__(self, binary: AnyPath, settings: Union[AnyPath, List[str], Dict[str, Any]], /,
                 zones: Optional[Dict[Tuple[int, int], Dict[str, Any]]] = None) -> None:
        """
        :param zones:       Custom zone ranges, defaults to None

        .. code-block:: python

            zones: Dict[Tuple[int, int], Dict[str, Any]] = {
                        (3500, 3600): dict(b=3, subme=11),
                        (4800, 4900): {'psy-rd': '0.40:0.05', 'merange': 48}
                    }
        """
        super().__init__(binary, settings)
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
    """Video encoder using x265 for HEVC"""

    @copy_docstring_from(VideoLanEncoder.__init__)
    def __init__(self, settings: Union[AnyPath, List[str], Dict[str, Any]], /,
                 zones: Optional[Dict[Tuple[int, int], Dict[str, Any]]] = None) -> None:
        super().__init__(BinaryPath.x265, settings, zones)

    def set_variable(self) -> Dict[str, Any]:
        min_luma, max_luma = Properties.get_colour_range(self.params, self.clip)
        return super().set_variable() | dict(min_luma=min_luma, max_luma=max_luma)


class X264Encoder(VideoLanEncoder):
    """Video encoder using x264 for AVC"""

    @copy_docstring_from(VideoLanEncoder.__init__)
    def __init__(self, settings: Union[AnyPath, List[str], Dict[str, Any]], /,
                 zones: Optional[Dict[Tuple[int, int], Dict[str, Any]]] = None) -> None:
        super().__init__(BinaryPath.x264, settings, zones)

    def set_variable(self) -> Dict[str, Any]:
        return super().set_variable() | dict(csp=Properties.get_csp(self.clip))
