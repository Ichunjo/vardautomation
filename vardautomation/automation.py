"""Automation module"""

__all__ = [
    'RunnerConfig', 'SelfRunner',

    'Patch'
]

from copy import deepcopy
from dataclasses import dataclass
from enum import Enum, auto
from itertools import chain
from typing import Callable, List, Optional, Sequence, Set, Tuple, TypedDict, cast

import vapoursynth as vs
from typing_extensions import NotRequired
from vardefunc.misc import DebugOutput
from vardefunc.types import Range
from vardefunc.util import normalise_ranges

from ._logging import logger
from .binary_path import BinaryPath
from .config import FileInfo, FileInfo2
from .tooling import (
    AudioCutter, AudioEncoder, AudioExtracter, BasicTool, LosslessEncoder, Mux, Qpfile,
    VideoEncoder, get_keyframes, make_qpfile
)
from .tooling.video import SupportQpfile
from .types import AnyPath, T
from .vpathlib import CleanupSet, VPath

core = vs.core


@dataclass(repr=False, eq=False, order=False, unsafe_hash=False, frozen=True, slots=True)
class RunnerConfig:
    """
    Config for the SelfRunner
    """

    class Order(Enum):
        """Simple enum for priority order"""
        VIDEO = auto()
        AUDIO = auto()

    v_encoder: VideoEncoder
    """Video encoder"""
    v_lossless_encoder: Optional[LosslessEncoder] = None
    """Lossless video encoder"""
    a_extracters: AudioExtracter | Sequence[AudioExtracter] | None = None
    """Audio extracter(s)"""
    a_cutters: AudioCutter | Sequence[AudioCutter] | None = None
    """Audio cutter(s)"""
    a_encoders: AudioEncoder | Sequence[AudioEncoder] | None = None
    """Audio encoder(s)"""
    muxer: Optional[Mux] = None
    """Muxer"""

    order: Order = Order.VIDEO
    """Priority order"""

    clear_outputs: bool = True
    """Clears all clips set for output in the current environment"""


class _QpFileParams(TypedDict):
    qpfile_clip: NotRequired[Optional[vs.VideoNode]]
    qpfile_func: NotRequired[Callable[[vs.VideoNode, AnyPath], Qpfile]]


class SelfRunner:
    """Self runner interface"""

    clip: vs.VideoNode
    """Clip to be encoded"""

    file: FileInfo
    """FileInfo object"""

    config: RunnerConfig
    """Config of the runner"""

    work_files: CleanupSet
    """
    Intermediate working files:

    The SelfRunner class will add everything it can in this set-like,
    meaning if you want to delete the files you can just do::

        runner = SelfRunner(...)
        runner.run()
        runner.work_files.clear()

    The runner will add these attributes to be deleted:
        * :py:attr:`FileInfo.name_clip_output`
        * :py:attr:`FileInfo.a_src`
        * :py:attr:`FileInfo.a_src_cut`
        * :py:attr:`FileInfo.a_enc_cut`
        * :py:attr:`FileInfo.chapter`

    So if you want to keep some of these files, this is possible::

        runner.work_files.discard(self.file.name_clip_output)
        runner.work_files.discard(self.file.chapter)
    """

    _qpfile_params: _QpFileParams

    def __init__(self, clip: vs.VideoNode, file: FileInfo, /, config: RunnerConfig) -> None:
        """
        :param clip:        Clip to be encoded
        :param file:        FileInfo object
        :param config:      Confif of the runner
        """
        self.clip = clip
        self.file = file
        self.config = config
        self.work_files = CleanupSet()
        self._qpfile_params = _QpFileParams()

    def run(self, *, show_logo: bool = True) -> None:
        """
        Main tooling chain

        :param show_logo:   Print vardoto logo.
        """
        if show_logo:
            logger.logo()
        logger.info('SelfRunning...')

        funcs = [self._encode, self._audio_getter]
        if self.config.order == RunnerConfig.Order.AUDIO:
            funcs.reverse()
        funcs.append(self._muxer)
        logger.debug(funcs)
        for f in funcs:
            f()

    def inject_qpfile_params(self, *, qpfile_clip: Optional[vs.VideoNode] = None,
                             qpfile_func: Callable[[vs.VideoNode, AnyPath], Qpfile] = make_qpfile) -> None:
        """
        :param qpfile_clip:         Clip to be used to generate the Qpfile
        :param qpfile_func:         Function to be used to generate the Qpfile
        """
        self._qpfile_params['qpfile_clip'] = qpfile_clip
        self._qpfile_params['qpfile_func'] = qpfile_func
        logger.debug(self._qpfile_params)

    def rename_final_file(self, name: AnyPath) -> None:
        """
        Rename the file.name_file_final

        :param name:            New filename
        """
        logger.debug('Renaming')
        self.file.name_file_final = self.file.name_file_final.replace(VPath(name))

    def upload_ftp(self, ftp_name: str, destination: AnyPath, rclone_args: Optional[List[str]] = None) -> None:
        """
        Upload the ``name_file_final`` to a given FTP using rclone

        :param ftp_name:        FTP name
        :param destination:     Path destination
        :param rclone_args:     Additionnal options, defaults to None
        """
        BasicTool(
            BinaryPath.rclone, ['copy', '--progress'] + (rclone_args if rclone_args else [])
            + [self.file.name_file_final.absolute().as_posix(), f'{ftp_name}:{VPath(destination).to_str()}']
        ).run()

    def _encode(self) -> None:
        if self.config.clear_outputs:
            for k in globals().keys():
                # pylint: disable=eval-used
                if isinstance((debug := eval(k)), DebugOutput):
                    debug.clear()
            vs.clear_outputs()

        if self.config.v_lossless_encoder:
            if not (
                path_lossless
                := self.file.name_clip_output.append_stem(self.config.v_lossless_encoder.suffix_name)
            ).exists():
                self.config.v_lossless_encoder.run_enc(self.clip, self.file)
            self.clip = core.lsmas.LWLibavSource(path_lossless.to_str())

        if not self.file.name_clip_output.exists():
            if isinstance(self.config.v_encoder, SupportQpfile):
                self.config.v_encoder.run_enc(self.clip, self.file, **self._qpfile_params)
            else:
                self.config.v_encoder.run_enc(self.clip, self.file)
        self.work_files.add(self.file.name_clip_output)

    def _audio_getter(self) -> None:  # noqa C901
        if not isinstance(self.file, FileInfo2):
            if self.config.a_extracters and self.file.a_src:
                for a_extracter in _toseq(self.config.a_extracters):
                    all_a_src = [self.file.a_src.set_track(n) for n in a_extracter.track_out]
                    self.work_files.update(all_a_src)
                    if not any(a_src.exists() for a_src in all_a_src):
                        a_extracter.run()
                    else:
                        logger.warning(f'Skipping "{[p.to_str() for p in all_a_src]}" to extract...')

            if self.config.a_cutters and self.file.a_src_cut:
                for i, a_cutter in enumerate(_toseq(self.config.a_cutters), start=1):
                    self.work_files.add(self.file.a_src_cut.set_track(i))
                    if not self.file.a_src_cut.set_track(i).exists():
                        a_cutter.run()
                    else:
                        logger.warning(f'Skipping "{self.file.a_src_cut.set_track(i).to_str()}" to cut...')

        if self.config.a_encoders and self.file.a_enc_cut:
            for i, a_encoder in enumerate(_toseq(self.config.a_encoders), start=1):
                self.work_files.add(self.file.a_enc_cut.set_track(i))
                if not self.file.a_enc_cut.set_track(i).exists():
                    a_encoder.run()
                else:
                    logger.warning(f'Skipping "{self.file.a_enc_cut.set_track(i).to_str()}" to encode...')

    def _muxer(self) -> None:
        if self.config.muxer:
            self.config.muxer.run()
            self.work_files.add(self.file.name_clip_output)
            if (c := self.file.chapter):
                self.work_files.add(c)


def _toseq(seq: T | Sequence[T]) -> Sequence[T]:
    return cast(Sequence[T], seq) if isinstance(seq, Sequence) else cast(Sequence[T], [seq])


class Patch:
    """Easy video patching interface"""

    encoder: VideoEncoder
    """VideoEncoder to be used"""

    clip: vs.VideoNode
    """Clip where the patch will pick the fixed ranges"""

    file: FileInfo
    """
    FileInfo object\n
    The file that will be fixed is the file defined in
     :py:attr:`vardautomation.config.FileInfo.name_file_final`
    """

    ranges: List[Tuple[int, int]]
    """Normalised ranges"""

    debug: bool
    """Debug boolean"""

    workdir: VPath
    """Work directory path"""
    output_filename: VPath
    """Output filename path"""

    _file_to_fix: VPath

    @logger.catch
    def __init__(self, encoder: VideoEncoder, clip: vs.VideoNode, file: FileInfo,
                 ranges: Range | List[Range],
                 output_filename: Optional[str] = None, *, debug: bool = False) -> None:
        """
        :param encoder:             VideoEncoder to be used
        :param clip:                Clip where the patch will pick the fixed ranges
        :param file:                FileInfo object. The file that will be fixed is the file defined
                                    in :py:attr:`vardautomation.config.FileInfo.name_file_final`
        :param ranges:              Ranges of frames that need to be fixed
        :param output_filename:     Optional filename. If not specified a suffix ``_new`` wil be added, defaults to None
        :param debug:               Debug argument, defaults to False
        """
        self.encoder = encoder
        self.clip = clip
        self.file = file

        self.ranges = normalise_ranges(self.clip, ranges)
        self.debug = debug

        self._file_to_fix = self.file.name_file_final

        final = self._file_to_fix.parent

        self.workdir = final / (self.file.name + '_temp')
        if output_filename is not None:
            self.output_filename = VPath(output_filename)
        else:
            self.output_filename = final / f'{self._file_to_fix.stem}_new.mkv'

        if self.workdir.exists():
            raise FileExistsError(f'{self.__class__.__name__}: {self.workdir.resolve().to_str()} already exists!')

    def run(self) -> None:
        """Launch patch"""
        # Local folder
        self.workdir.mkdir()
        self._resolve_range()
        self._encode()
        self._cut_and_merge()

    def do_cleanup(self) -> None:
        """Delete working directory folder"""
        self.workdir.rmtree(ignore_errors=True)

    @logger.catch
    def _resolve_range(self) -> None:
        kf = get_keyframes(self._file_to_fix)
        kfsint = kf.frames + [self.clip.num_frames]

        ranges = self._bound_to_keyframes(kfsint)
        logger.debug(f'Ranges: {str(ranges)}')
        nranges = normalise_ranges(self.clip, ranges, norm_dups=True)
        logger.debug(f'Ranges: {str(nranges)}')

        if len(nranges) == 1 and nranges[0][0] == 0 and nranges[0][1] == self.clip.num_frames:
            raise ValueError(f'{self.__class__.__name__}: Don\'t use Patch, just redo your encode')

        self.ranges = nranges

    def _encode(self) -> None:
        params = deepcopy(self.encoder.params)
        for i, (s, e) in enumerate(self.ranges, start=1):
            logger.debug(str((s, e)))
            fix = self.workdir / f'fix-{i:03.0f}'
            self.file.name_clip_output = fix
            self.encoder.run_enc(self.clip[s:e], self.file)
            self.encoder.params = params

            BasicTool(BinaryPath.mkvmerge, ['-o', fix.with_suffix('.mkv').to_str(), fix.to_str()]).run()

    def _cut_and_merge(self) -> None:
        tmp = self.workdir / 'tmp.mkv'
        tmpnoaudio = self.workdir / 'tmp_noaudio.mkv'

        if (start := (rng := list(chain.from_iterable(self.ranges)))[0]) == 0:
            rng = rng[1:]
        if rng[-1] == self.clip.num_frames:
            rng = rng[:-1]
        split_args = ['--split', 'frames:' + ','.join(map(str, rng))]

        BasicTool(
            BinaryPath.mkvmerge,
            ['-o', tmp.to_str(), '--no-audio', '--no-track-tags', '--no-chapters',
             self._file_to_fix.to_str(), *split_args]
        ).run()

        tmp_files = sorted(self.workdir.glob('tmp-???.mkv'))
        fix_files = sorted(self.workdir.glob('fix-???.mkv'))

        # merge_args: List[str] = []
        # for i, tmp in enumerate(tmp_files):
        #     merge_args += [
        #         fix_files[int(i/2)].to_str()
        #         if i % 2 == (0 if start == 0 else 1) else tmp.to_str()
        #     ] + ['+']
        merge_args = [
            fix_files[int(i/2)].to_str() if i % 2 == (0 if start == 0 else 1) else tmp.to_str()
            for i, tmp in enumerate(tmp_files)
        ]

        BasicTool(
            BinaryPath.mkvmerge,
            ['-o', tmpnoaudio.to_str(),
             '--no-audio', '--no-track-tags', '--no-chapters',
             '[', *merge_args, ']',
             '--append-to', ','.join([f'{i+1}:0:{i}:0' for i in range(len(merge_args) - 1)])]
        ).run()
        BasicTool(
            BinaryPath.mkvmerge,
            ['-o', self.output_filename.to_str(), tmpnoaudio.to_str(), '--no-video', self._file_to_fix.to_str()]
        ).run()

    @logger.catch
    def _bound_to_keyframes(self, kfs: List[int]) -> List[Range]:
        rng_set: Set[Tuple[int, int]] = set()
        for start, end in self.ranges:
            s, e = (None, ) * 2
            for i, kf in enumerate(kfs):
                if kf > start:
                    s = kfs[i-1]
                    break
                if kf == start:
                    s = kf
                    break

            for i, kf in enumerate(kfs):
                if kf >= end:
                    e = kf
                    break

            if s is None or e is None:
                logger.debug(str((s, e)))
                raise ValueError(f'{self.__class__.__name__} Something is wrong in `s` or `e`')

            rng_set.add((s, e))

        return sorted(rng_set)
