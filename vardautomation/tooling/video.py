
__all__ = [
    'VideoEncoder', 'VideoLanEncoder', 'X265', 'X264',
    'LosslessEncoder', 'NVEncCLossless', 'FFV1',
    'progress_update_func'
]

import subprocess

from abc import ABC
from typing import (
    Any, BinaryIO, Callable, ClassVar, Dict, List, NoReturn, Optional, Sequence, Set, Tuple, cast,
    overload
)

import vapoursynth as vs

from .._logging import logger
from ..binary_path import BinaryPath
from ..config import FileInfo
from ..utils import Properties, copy_docstring_from
from ..vpathlib import VPath
from ..vtypes import AnyPath, UpdateFunc
from .abstract import Tool
from .base import BasicTool
from .misc import Qpfile, get_keyframes, make_qpfile, make_tcfile
from .mux import MatroskaFile


def progress_update_func(value: int, endvalue: int) -> None:
    """
    Callback function used in clip.output

    :param value:       Current value
    :param endvalue:    End value
    """
    # pylint: disable=consider-using-f-string
    if value == 0:
        return
    logger.logger.opt(raw=True).info(
        "\rVapourSynth: %i/%i ~ %.2f%% || Encoder: " % (value, endvalue, 100 * value / endvalue)
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

    def __init__(self, binary: AnyPath, settings: AnyPath | List[str] | Dict[str, Any]) -> None:
        """
        ::

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

        :param binary:              Path to your binary file.
        :param settings:            Path to your settings file or list of string or a dict containing your settings
                                    Special variable names can be specified and are replaced at runtime.
                                    Supported variable names are defined in :py:func:`set_variable` docstring.
        """
        super().__init__(binary, settings)

    @overload
    def run_enc(self, clip: vs.VideoNode, file: FileInfo) -> None:
        ...

    @overload
    def run_enc(self, clip: vs.VideoNode, file: None) -> None:
        ...

    @logger.catch
    def run_enc(self, clip: vs.VideoNode, file: FileInfo | None) -> None:
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

    @logger.catch
    def run(self) -> NoReturn:
        """
        Shouldn't be used in VideoEncoder object.
        Use :py:func:`run_enc` instead
        """
        raise NameError(f'{self.__class__.__name__}: Use `run_enc` instead')

    @copy_docstring_from(Tool.set_variable, 'o+t')
    def set_variable(self) -> Dict[str, Any]:
        """
        Replaces ``{clip_output:s}`` by ``self.file.name_clip_output``\n
        Replaces ``{filename:s}`` by ``self.file.name``\n
        """
        try:
            return dict(clip_output=self.file.name_clip_output.to_str(), filename=self.file.name)
        except AttributeError as attr_err:
            logger.warning(f'{self.__class__.__name__}: couldn\'t retrieve some attributes;')
            logger.debug(str(attr_err))
            return {}

    def _do_encode(self) -> None:
        logger.info(f'{self.__class__.__name__} command: ' + ' '.join(self.params))
        with logger.catch_ctx(), subprocess.Popen(self.params, stdin=subprocess.PIPE) as process:
            self.clip.output(cast(BinaryIO, process.stdin), self.y4m, self.progress_update, self.prefetch, self.backlog)


class LosslessEncoder(VideoEncoder):
    """Video encoder for lossless encoding"""

    suffix_name: str = '_lossless'
    """Suffix name for the lossless output"""

    @copy_docstring_from(Tool.set_variable, 'o+t')
    def set_variable(self) -> Dict[str, Any]:
        """
        Replaces ``{clip_output_lossless:s}`` by ``self.file.name_clip_output.append_stem(self.suffix_name)``\n
        Replaces ``{bits:s}`` by ``Properties.get_depth(self.clip)``\n
        """
        try:
            return dict(
                clip_output_lossless=self.file.name_clip_output.append_stem(self.suffix_name).to_str(),
                bits=Properties.get_depth(self.clip)
            )
        except AttributeError as attr_err:
            logger.warning(f'{self.__class__.__name__}: couldn\'t retrieve some attributes;')
            logger.debug(str(attr_err))
            return {}


class NVEncCLossless(LosslessEncoder):
    """Built-in NvencC encoder."""

    suffix_name: str = '_lossless.mkv'

    def __init__(self, *, hevc: bool = True) -> None:
        """
        Use NvencC to output a lossless encode in HEVC

        :param hevc:            If True use HEVC codec for output.
                                Keep in mind that 10 bit support depends on your NVEnc, driver and CUDA version
        """
        super().__init__(
            BinaryPath.nvencc,
            ['-i', '-', '--y4m', '--lossless',
             '--codec', 'hevc' if hevc else 'avc',
             '--output-depth', '{bits:d}', '-o', '{clip_output_lossless:s}'],
        )
        self.progress_update = None


class FFV1(LosslessEncoder):
    """Built-in FFV1 encoder."""

    suffix_name: str = '_lossless.mkv'

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


class SupportQpfile(VideoEncoder, ABC):
    # pylint: disable=arguments-differ

    @overload
    def run_enc(self, clip: vs.VideoNode, file: FileInfo) -> None:
        ...

    @overload
    def run_enc(self, clip: vs.VideoNode, file: None) -> None:
        ...

    @overload
    def run_enc(self, clip: vs.VideoNode, file: FileInfo, *,
                qpfile_clip: vs.VideoNode,
                qpfile_func: Callable[[vs.VideoNode, AnyPath], Qpfile] = ...) -> None:
        ...

    @overload
    def run_enc(self, clip: vs.VideoNode, file: None, *,
                qpfile_clip: None = ...,
                qpfile_func: Callable[[vs.VideoNode, AnyPath], Qpfile] = ...) -> None:
        ...

    @logger.catch
    @copy_docstring_from(VideoEncoder.run_enc, 'o+t')
    def run_enc(self, clip: vs.VideoNode, file: FileInfo | None, *,
                qpfile_clip: 'vs.VideoNode | None' = None,
                qpfile_func: Callable[[vs.VideoNode, AnyPath], Qpfile] = make_qpfile) -> None:
        """
        :param qpfile_clip:         Clip to be used to generate the Qpfile
        :param qpfile_func:         Function to be used to generate the Qpfile
        """
        _craps: List[VPath] = []
        if qpfile_clip:
            logger.info('Qpfiling is enabled...')
            if qpfile_clip.num_frames != clip.num_frames:
                raise ValueError(f'{self.__class__.__name__}: the ``qpfile_clip`` should have the same length than the ``clip``')
            if not file:
                raise ValueError(f'{self.__class__.__name__}: a FileInfo file is needed when a qpfile_clip is provided')
            qpfile = qpfile_func(
                qpfile_clip,
                file.name_clip_output.append_stem('_qpfile').with_suffix('.log')
            )
            logger.trace(str(qpfile._asdict()))
            self.params.extend(['--qpfile', qpfile.path.to_str()])
            _craps.append(qpfile.path)

        super().run_enc(clip, file)

        for crap in _craps:
            crap.rm(ignore_errors=True)


class SupportResume(SupportQpfile, ABC):
    # pylint: disable=arguments-differ
    resumable = False

    @overload
    def run_enc(self, clip: vs.VideoNode, file: FileInfo) -> None:
        ...

    @overload
    def run_enc(self, clip: vs.VideoNode, file: None) -> None:
        ...

    @overload
    def run_enc(self, clip: vs.VideoNode, file: FileInfo, *,
                qpfile_clip: vs.VideoNode,
                qpfile_func: Callable[[vs.VideoNode, AnyPath], Qpfile] = ...) -> None:
        ...

    @overload
    def run_enc(self, clip: vs.VideoNode, file: None, *,
                qpfile_clip: None = ...,
                qpfile_func: Callable[[vs.VideoNode, AnyPath], Qpfile] = ...) -> None:
        ...

    @logger.catch
    def run_enc(self, clip: vs.VideoNode, file: FileInfo | None, *,  # noqa C901
                qpfile_clip: 'vs.VideoNode | None' = None,
                qpfile_func: Callable[[vs.VideoNode, AnyPath], Qpfile] = make_qpfile) -> None:
        if not self.resumable:
            return super().run_enc(clip, file, **dict(qpfile_clip=qpfile_clip, qpfile_func=qpfile_func))

        logger.info('Resumable encode is enabled...')

        if not file:
            raise ValueError(f'{self.__class__.__name__}: a FileInfo file is needed when `resumable` is enabled')
        self.file = file

        # Copy original name
        _output = VPath(self.file.name_clip_output)

        pattern = self.file.name_clip_output.resolve().append_stem('_part_???')
        _parts = sorted(pattern.parent.glob(pattern.name))

        logger.info(f'{len(_parts)} existing part(s) have been detected')

        # Get the last keyframes where you can encode from
        _kfs = list[int]()
        for part in _parts:
            try:
                kfnt = get_keyframes(part)
                logger.trace(str(kfnt._asdict()))
                kf = kfnt.frames[-1]
                # If the last keyframe is 0 then we can just overwrite the last encode
                if kf == 0:
                    del _parts[-1]
                else:
                    _kfs.append(kf)
                kfnt.path.rm()
            # If subprocess throws an error the file is probably corrupted.
            # Let the encoder overwrite it
            except subprocess.CalledProcessError as err:
                logger.debug(str(err))
                del _parts[-1]
        logger.debug(str(_parts))

        self.file.name_clip_output = self.file.name_clip_output.append_stem(f'_part_{len(_parts):03.0f}')
        _parts.append(self.file.name_clip_output)

        start_frame = sum(_kfs)
        logger.info(f'Start frame of the clip is now {start_frame}')
        clip = clip[start_frame:]
        if qpfile_clip:
            logger.info(f'Start frame of the qpfile_clip is now {start_frame}')
            qpfile_clip = qpfile_clip[start_frame:]

        super().run_enc(clip, self.file, **dict(qpfile_clip=qpfile_clip, qpfile_func=qpfile_func))

        logger.info('Resumable encode; merging...')

        # Files to delete
        _craps: Set[VPath] = set()
        # Split the files until the last keyframe
        mkv_parts: List[VPath] = []
        logger.debug('Merging the parts...')
        for kf, part in zip(_kfs, _parts):
            p_mkv = part.with_suffix('.mkv')
            logger.trace('p_mkv: ' + p_mkv.to_str())
            logger.trace('part: ' + part.to_str())
            MatroskaFile(p_mkv, part, ('--quiet' if self._quiet else '')).split_frames(kf)
            # Mkv files
            p_mkv001 = p_mkv.append_stem('-001')
            p_mkv002 = p_mkv.append_stem('-002')
            # We need them
            mkv_parts.append(p_mkv001)
            # Those are crappy
            _craps.update([p_mkv001, p_mkv002])
        _craps.update(_parts)
        logger.trace('mkv_parts: ' + str(mkv_parts))
        logger.trace('craps: ' + str(_craps))

        # Also merge the last encoded part
        logger.debug('Merging the last encoded part...')
        last = self.file.name_clip_output.with_suffix('.mkv')
        logger.trace('last: ' + last.to_str())
        logger.trace('output: ' + self.file.name_clip_output.to_str())
        MatroskaFile(last, self.file.name_clip_output, ('--quiet' if self._quiet else '')).mux()
        mkv_parts.append(last)
        _craps.add(last)
        _craps.add(self.file.name_clip_output)
        logger.trace('mkv_parts: ' + str(mkv_parts))
        logger.trace('craps: ' + str(_craps))

        # Restore original name
        self.file.name_clip_output = _output
        output = self.file.name_clip_output.append_stem('_tmp').with_suffix('.mkv')
        if len(mkv_parts) > 1:
            # Merge the splitted files
            logger.debug('Merge the splitted files')
            MatroskaFile(output, None, ('--quiet' if self._quiet else '')).append_to(mkv_parts)
        else:
            logger.debug('One part detected')
            mkvp = mkv_parts.pop(0)
            mkvp.rename(output)
            _craps.remove(mkvp)
        _craps.add(output)
        logger.trace('craps: ' + str(_craps))

        # Extract the merged file
        BasicTool(BinaryPath.mkvextract, [output.to_str(), 'tracks', f'0:{self.file.name_clip_output.to_str()}']).run()
        # Delete working files
        pattern_qpfile = self.file.name_clip_output.resolve().append_stem('_part_???_qpfile').with_suffix('.log')
        _craps.update(pattern_qpfile.parent.glob(pattern_qpfile.name))
        for crap in _craps:
            crap.rm()
        del _craps

        return None


class SupportManualVFR(SupportResume, ABC):
    # pylint: disable=arguments-differ
    tcfile: VPath

    @overload
    def run_enc(self, clip: vs.VideoNode, file: FileInfo) -> None:
        ...

    @overload
    def run_enc(self, clip: vs.VideoNode, file: None) -> None:
        ...

    @overload
    def run_enc(self, clip: vs.VideoNode, file: FileInfo, *,
                qpfile_clip: vs.VideoNode,
                qpfile_func: Callable[[vs.VideoNode, AnyPath], Qpfile] = ...) -> None:
        ...

    @overload
    def run_enc(self, clip: vs.VideoNode, file: None, *,
                qpfile_clip: None = ...,
                qpfile_func: Callable[[vs.VideoNode, AnyPath], Qpfile] = ...) -> None:
        ...

    @overload
    def run_enc(self, clip: Sequence[vs.VideoNode], file: FileInfo) -> None:
        ...

    @overload
    def run_enc(self, clip: Sequence[vs.VideoNode], file: FileInfo, *,
                qpfile_clip: vs.VideoNode,
                qpfile_func: Callable[[vs.VideoNode, AnyPath], Qpfile] = ...) -> None:
        ...

    @logger.catch
    def run_enc(self, clip: vs.VideoNode | Sequence[vs.VideoNode], file: FileInfo | None, *,
                qpfile_clip: 'vs.VideoNode | None' = None,
                qpfile_func: Callable[[vs.VideoNode, AnyPath], Qpfile] = make_qpfile) -> None:
        if isinstance(clip, vs.VideoNode):
            return super().run_enc(clip, file, **dict(qpfile_clip=qpfile_clip, qpfile_func=qpfile_func))

        logger.info('Manual VFR encode is enabled...')
        if not file:
            raise ValueError(f'{self.__class__.__name__}: a FileInfo file is needed when enabling manual VFR encode')

        base_name = VPath(file.name_clip_output)
        outputs = list[VPath]()

        for i, c in enumerate(clip):
            params = self.params.copy()
            file.name_clip_output = base_name.append_stem(f'_vfr_{i:03.0f}_{c.fps.numerator}_{c.fps.denominator}')
            outputs.append(file.name_clip_output)
            if self.resumable and file.name_clip_output.exists():
                continue
            super().run_enc(c, file, **dict(qpfile_clip=qpfile_clip, qpfile_func=qpfile_func))
            self.params = params

        self.tcfile = make_tcfile(clip, file.name_file_final.with_suffix('.tcfile'))
        MatroskaFile(base_name, None, ('--quiet' if self._quiet else ''), '--timestamps', f'0:{self.tcfile.to_str()}').append_to(outputs)

        return None


class HasOverrideParams(VideoEncoder, ABC):
    @copy_docstring_from(VideoEncoder.__init__, 'o+t')
    def __init__(self, binary: AnyPath, settings: AnyPath | List[str] | Dict[str, Any],
                 override_params: Optional[Dict[str, Any]] = None) -> None:
        """
        ::

            override_params: Dict[str, Any] = {'--crf': 10, '--preset': 'ultrafast'}

        :param override_params:     Parameters to be overrided in ``settings``
        """
        super().__init__(binary, settings)

        if override_params:
            nparams = self.params_asdict | override_params
            self.params.clear()
            for k, v in nparams.items():
                self.params.extend([k] + ([str(v)] if v is not None else []))

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
            else:
                dparams[p] = None
                i += 1

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


class HasZone(HasOverrideParams, ABC):
    # pylint: disable=return-in-init
    # pylint: disable=inconsistent-return-statements
    @copy_docstring_from(HasOverrideParams.__init__, 'o+t')
    def __init__(self, binary: AnyPath, settings: AnyPath | List[str] | Dict[str, Any],
                 zones: Optional[Dict[Tuple[int, int], Dict[str, Any]]] = None,
                 override_params: Optional[Dict[str, Any]] = None) -> None:
        """
        :param zones:               Custom zone ranges, defaults to None

        ::

            zones: Dict[Tuple[int, int], Dict[str, Any]] = {
                        (3500, 3600): dict(b=3, subme=11),
                        (4800, 4900): {'psy-rd': '0.40:0.05', 'merange': 48}
                    }
        """
        if not zones:
            return super().__init__(binary, settings, override_params)

        zones_settings: str = ''
        for i, ((start, end), opt) in enumerate(zones.items()):
            zones_settings += f'{start},{end}'
            for opt_name, opt_val in opt.items():
                zones_settings += f',{opt_name}={opt_val}'
            if i != len(zones) - 1:
                zones_settings += '/'
        zones_d = {'--zones': zones_settings}

        super().__init__(
            binary, settings,
            (override_params | zones_d if override_params else zones_d)
        )


class VideoLanEncoder(SupportManualVFR, SupportResume, SupportQpfile, HasZone, HasOverrideParams, VideoEncoder, ABC):
    """Abstract VideoEncoder interface for VideoLan based encoders such as x265 and x264."""

    resumable: bool
    """Enable resumable encodes"""

    _vl_binary: ClassVar[AnyPath]
    _bits: int

    @copy_docstring_from(HasOverrideParams.__init__)
    def __init__(self, settings: AnyPath | List[str] | Dict[str, Any], /,
                 zones: Optional[Dict[Tuple[int, int], Dict[str, Any]]] = None,
                 override_params: Optional[Dict[str, Any]] = None,
                 progress_update: Optional[UpdateFunc] = progress_update_func) -> None:
        super().__init__(self._vl_binary, settings, zones, override_params)
        self.progress_update = progress_update

    @copy_docstring_from(Tool.set_variable, 'o+t')
    def set_variable(self) -> Dict[str, Any]:
        """
        Replaces ``{clip_output:s}`` with ``self.file.name_clip_output``\n
        Replaces ``{filename:s}`` with ``self.file.name``\n
        Replaces ``{frames:d}`` with ``self.clip.num_frames``\n
        Replaces ``{fps_num:d}`` with ``self.clip.fps.numerator``\n
        Replaces ``{fps_den:d}`` with ``self.clip.fps.denominator``\n
        Replaces ``{bits:d}`` with ``Properties.get_depth(self.clip)``\n
        Replaces ``{min_keyint:d}`` with ``round(self.clip.fps)``\n
        Replaces ``{keyint:d}`` with ``round(self.clip.fps) * 10``\n
        """
        try:
            bits = Properties.get_depth(self.clip)
        except AttributeError as attr_err:
            logger.warning(f'{self.__class__.__name__}: couldn\'t retrieve bit depth')
            logger.debug(str(attr_err))
            return {}
        if not hasattr(self, '_bits') and bits > 10:
            logger.warning(f'{self.__class__.__name__}: Bitdepth is > 10. Are you sure about that?')
            self._bits = bits
        logger.debug(self.file.name_clip_output.to_str())
        return dict(
            clip_output=self.file.name_clip_output.to_str(), filename=self.file.name, frames=self.clip.num_frames,
            fps_num=self.clip.fps.numerator, fps_den=self.clip.fps.denominator, bits=bits,
            min_keyint=round(self.clip.fps), keyint=round(self.clip.fps) * 10
        )


class X265(VideoLanEncoder):
    """Video encoder using x265 for HEVC"""

    _vl_binary = BinaryPath.x265

    resumable: bool
    """Enable resumable encodes"""

    @copy_docstring_from(VideoLanEncoder.set_variable, 'o+t')
    def set_variable(self) -> Dict[str, Any]:
        """
        Replaces ``{min_luma:d}`` and ``{max_luma:d}`` with ``Properties.get_colour_range(self.params, self.clip)``\n
        Replaces ``{matrix:d}`` with ``Properties.get_prop(self.clip.get_frame(0), '_Matrix', int)``\n
        Replaces ``{primaries:d}`` with ``Properties.get_prop(self.clip.get_frame(0), '_Primaries', int)``\n
        Replaces ``{transfer:d}`` with ``Properties.get_prop(self.clip.get_frame(0), '_Transfer', int)``\n
        """
        min_luma, max_luma = Properties.get_colour_range(self.params, self.clip)

        with self.clip.get_frame(0) as frame:
            matrix = Properties.get_prop(frame, '_Matrix', int)
            primaries = Properties.get_prop(frame, '_Primaries', int)
            transfer = Properties.get_prop(frame, '_Transfer', int)

        if len({matrix, primaries, transfer}) != 1:
            logger.warning(f'{self.__class__.__name__}: Matrix/Primaries/Transfer mismatch '
                           f'({matrix}/{primaries}/{transfer})! Make sure this is what you want!')

        logger.debug('min_luma, max_luma: ' + str((min_luma, max_luma)))
        logger.debug('matrix, primaries, transfer: ' + str((matrix, primaries, transfer)))
        return super().set_variable() | dict(
            min_luma=min_luma, max_luma=max_luma,
            matrix=matrix, primaries=primaries, transfer=transfer
        )


class X264(VideoLanEncoder):
    """Video encoder using x264 for AVC"""

    _vl_binary = BinaryPath.x264

    resumable: bool
    """Enable resumable encodes"""

    @copy_docstring_from(VideoLanEncoder.set_variable, 'o+t')
    def set_variable(self) -> Dict[str, Any]:
        """
        Replaces ``{csp:s}`` with ``Properties.get_csp(self.clip)``\n
        Replaces ``{matrix:s}`` with ``Properties.get_prop(self.clip.get_frame(0), '_Matrix', int)``\n
        Replaces ``{primaries:s}`` with ``Properties.get_prop(self.clip.get_frame(0), '_Primaries', int)``\n
        Replaces ``{transfer:s}`` with ``Properties.get_prop(self.clip.get_frame(0), '_Transfer', int)``\n
        """
        csp = Properties.get_csp(self.clip)

        with self.clip.get_frame(0) as frame:
            matrix = Properties.get_matrix_name(frame, '_Matrix')
            primaries = Properties.get_matrix_name(frame, '_Primaries')
            transfer = Properties.get_matrix_name(frame, '_Transfer')

        if len({matrix, primaries, transfer}) != 1:
            logger.warning(f'{self.__class__.__name__}: Matrix/Primaries/Transfer mismatch '
                           f'({matrix}/{primaries}/{transfer})! Make sure this is what you want!')

        logger.debug('csp: ' + str(csp))
        logger.debug('matrix, primaries, transfer: ' + str((matrix, primaries, transfer)))
        return super().set_variable() | dict(
            csp=csp, matrix=matrix, primaries=primaries, transfer=transfer
        )
