
__all__ = [
    'VideoEncoder', 'VideoLanEncoder', 'X265', 'X264',
    'LosslessEncoder', 'NVEncCLossless', 'FFV1',
    'progress_update_func'
]

import subprocess
from abc import ABC
from typing import Any, BinaryIO, ClassVar, Dict, Final, List, NoReturn, Optional, Tuple, Union, cast

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

    progress_update: Optional[UpdateFunc] = None
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

        self._update_settings()
        self._do_encode()

    def run(self) -> NoReturn:
        """
        Shouldn't be used in VideoEncoder object.
        Use :py:func:`run_enc` instead
        """
        Status.fail(f'{self.__class__.__name__}: Use `run_enc` instead', exception=NameError)

    @copy_docstring_from(Tool.set_variable, 'o+t')
    def set_variable(self) -> Dict[str, Any]:
        """
        Replaces ``{clip_output:s}`` by ``self.file.name_clip_output``\n
        Replaces ``{filename:s}`` by ``self.file.name``\n
        """
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

    @copy_docstring_from(Tool.set_variable, 'o+t')
    def set_variable(self) -> Dict[str, Any]:
        """
        Replaces ``{clip_output_lossless:s}`` by ``self.file.name_clip_output_lossless``\n
        Replaces ``{bits:s}`` by ``Properties.get_depth(self.clip)``\n
        """
        try:
            return dict(
                clip_output_lossless=self.file.name_clip_output_lossless.to_str(),
                bits=Properties.get_depth(self.clip)
            )
        except AttributeError:
            return {}


class NVEncCLossless(LosslessEncoder):
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


class FFV1(LosslessEncoder):
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

    _vl_binary: ClassVar[AnyPath]
    _bits: int

    @copy_docstring_from(Tool.__init__, 'o+t')
    def __init__(self, settings: Union[AnyPath, List[str], Dict[str, Any]], /,
                 zones: Optional[Dict[Tuple[int, int], Dict[str, Any]]] = None,
                 override_params: Optional[Dict[str, Any]] = None,
                 progress_update: Optional[UpdateFunc] = progress_update_func) -> None:
        """
        :param zones:               Custom zone ranges, defaults to None
        :param override_params:     Parameters to be overrided in ``settings``

        ::

            zones: Dict[Tuple[int, int], Dict[str, Any]] = {
                        (3500, 3600): dict(b=3, subme=11),
                        (4800, 4900): {'psy-rd': '0.40:0.05', 'merange': 48}
                    }
        """
        super().__init__(self._vl_binary, settings)
        if zones:
            zones_settings: str = ''
            for i, ((start, end), opt) in enumerate(zones.items()):
                zones_settings += f'{start},{end}'
                for opt_name, opt_val in opt.items():
                    zones_settings += f',{opt_name}={opt_val}'
                if i != len(zones) - 1:
                    zones_settings += '/'
            self.params.extend(['--zones', zones_settings])

        if override_params:
            nparams = self.params_asdict | override_params
            self.params.clear()
            for k, v in nparams.items():
                self.params.extend([k] + ([str(v)] if v else []))

        self.progress_update = progress_update

    @property
    def params_asdict(self) -> Dict[str, Any]:  # noqa C901
        """
        Get :py:attr:`params` as a dictionnary
        """
        # I know this is ugly
        def _is_number(s: str) -> bool:
            try:
                int(s)
            except ValueError:
                try:
                    float(s)
                except ValueError:
                    return False
                else:
                    return True
            else:
                return True

        dparams: Dict[str, Any] = {}
        i = 0
        while i < len(self.params):
            p = self.params[i]
            if p.startswith(('--', '-')):
                if i == len(self.params) - 1:
                    dparams[p] = None
                    break
                pp = self.params[i + 1]
                if pp.startswith('--'):
                    dparams[p] = None
                    i += 1
                elif pp.startswith('-'):
                    if _is_number(pp):
                        dparams[p] = pp
                        i += 2
                    else:
                        dparams[p] = None
                        i += 1
                else:
                    dparams[p] = pp
                    i += 2

        for k, v in dparams.items():
            try:
                v_int = int(v)
            except (ValueError, TypeError):
                try:
                    v_float = float(v)
                except (ValueError, TypeError):
                    pass
                else:
                    dparams[k] = v_float
            else:
                dparams[k] = v_int

        return dparams

    @copy_docstring_from(Tool.set_variable, 'o+t')
    def set_variable(self) -> Dict[str, Any]:
        """
        Replaces ``{clip_output:s}`` by ``self.file.name_clip_output``\n
        Replaces ``{filename:s}`` by ``self.file.name``\n
        Replaces ``{frames:d}`` by ``self.clip.num_frames``\n
        Replaces ``{fps_num:d}`` by ``self.clip.fps.numerator``\n
        Replaces ``{fps_den:d}`` by ``self.clip.fps.denominator``\n
        Replaces ``{bits:d}`` by ``Properties.get_depth(self.clip)``\n
        Replaces ``{min_keyint:d}`` by ``round(self.clip.fps)``\n
        Replaces ``{keyint:d}`` by ``round(self.clip.fps) * 10``\n
        """
        try:
            bits = Properties.get_depth(self.clip)
        except AttributeError:
            return {}
        else:
            if not hasattr(self, '_bits') and bits > 10:
                Status.warn(f'{self.__class__.__name__}: Bitdepth is > 10. Are you sure about that?')
                self._bits = bits
            return dict(
                clip_output=self.file.name_clip_output.to_str(), filename=self.file.name, frames=self.clip.num_frames,
                fps_num=self.clip.fps.numerator, fps_den=self.clip.fps.denominator, bits=bits,
                min_keyint=round(self.clip.fps), keyint=round(self.clip.fps) * 10
            )


class X265(VideoLanEncoder):
    """Video encoder using x265 for HEVC"""

    _vl_binary = BinaryPath.x265

    @copy_docstring_from(VideoLanEncoder.set_variable, 'o+t')
    def set_variable(self) -> Dict[str, Any]:
        """
        Replaces ``{min_luma:d}`` and ``{max_luma:d}`` by ``Properties.get_colour_range(self.params, self.clip)``\n
        """
        min_luma, max_luma = Properties.get_colour_range(self.params, self.clip)
        return super().set_variable() | dict(min_luma=min_luma, max_luma=max_luma)


class X264(VideoLanEncoder):
    """Video encoder using x264 for AVC"""

    _vl_binary = BinaryPath.x264

    @copy_docstring_from(VideoLanEncoder.set_variable, 'o+t')
    def set_variable(self) -> Dict[str, Any]:
        """
        Replaces ``{csp:s}`` by ``Properties.get_csp(self.clip)``\n
        """
        return super().set_variable() | dict(csp=Properties.get_csp(self.clip))
