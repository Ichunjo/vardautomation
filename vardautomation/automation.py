"""Automation module"""
from __future__ import annotations

__all__ = [
    'Parser', 'RunnerConfig', 'SelfRunner',
]

import argparse
from dataclasses import dataclass
from enum import Enum, auto
from os import remove
from typing import List, Optional, Sequence, Set, Tuple, Union, cast

import vapoursynth as vs

from .binary_path import BinaryPath
from .config import FileInfo
from .status import Status
from .tooling import (AudioCutter, AudioEncoder, AudioExtracter, BasicTool,
                      LosslessEncoder, Mux, VideoEncoder)
from .types import AnyPath, T
from .vpathlib import VPath

core = vs.core


class Parser:
    def __init__(self, file: FileInfo) -> None:
        parser = argparse.ArgumentParser(description=f'Encode {file.name}')
        parser.add_argument('-L', '--lossless', action='store_true', default=False,
                            help='Write a lossless file instead of piping the pre-processing.')
        parser.add_argument('-Q', '--qpfile', action='store_true', default=False,
                            help='Write a qpfile from scene changes before encoding')
        parser.add_argument("-S", '--start', nargs='?', type=int, help='Start encode at frame START.')
        parser.add_argument("-E", '--end', nargs='?', type=int, help='Stop encode at frame END (inclusive).')
        self.args = parser.parse_args()
        super().__init__()

    def parsing(self, file: FileInfo, clip: vs.VideoNode) -> Tuple[FileInfo, vs.VideoNode]:
        # Lossless check
        if self.args.lossless:
            file.do_lossless = True

        # Qpfile check
        if self.args.qpfile:
            file.do_qpfile = True

        if self.args.start or self.args.end:
            Status.fail('', exception=NotImplementedError)

        return file, clip


@dataclass(repr=False, eq=False)
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
    a_extracters: Union[AudioExtracter, Sequence[AudioExtracter], None] = None
    """Audio extracter(s)"""
    a_cutters: Union[AudioCutter, Sequence[AudioCutter], None] = None
    """Audio cutter(s)"""
    a_encoders: Union[AudioEncoder, Sequence[AudioEncoder], None] = None
    """Audio encoder(s)"""
    muxer: Optional[Mux] = None
    """Muxer"""

    order: RunnerConfig.Order = Order.VIDEO
    """Priority order"""


class SelfRunner:
    """Self runner interface"""

    clip: vs.VideoNode
    """Clip to be encoded"""

    file: FileInfo
    """FileInfo object"""

    config: RunnerConfig
    """Confif of the runner"""

    cleanup_files: Set[AnyPath]
    """Files to be deleted"""

    def __init__(self, clip: vs.VideoNode, file: FileInfo, /, config: RunnerConfig) -> None:
        """
        :param clip:        Clip to be encoded
        :param file:        FileInfo object
        :param config:      Confif of the runner
        """
        self.clip = clip
        self.file = file
        self.config = config
        self.cleanup_files = set()

    def run(self) -> None:
        """Main tooling chain"""
        self._parsing()

        funcs = [self._encode, self._audio_getter]
        if self.config.order == RunnerConfig.Order.AUDIO:
            funcs.reverse()
        for f in funcs:
            f()

        self._muxer()

    def do_cleanup(self, *extra_files: AnyPath) -> None:
        """
        Delete working files

        :param extra_files:     Additional files to be deleted
        """
        self.cleanup_files.update(extra_files)
        for files in self.cleanup_files:
            remove(files)
        self.cleanup_files.clear()

    def rename_final_file(self, name: AnyPath) -> None:
        """
        Rename the file.name_file_final

        :param name:            New filename
        """
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

    def _parsing(self) -> None:
        parser = Parser(self.file)
        self.file, self.clip = parser.parsing(self.file, self.clip)

    def _encode(self) -> None:
        if self.file.do_lossless and self.config.v_lossless_encoder:
            if not self.file.name_clip_output_lossless.exists():
                self.config.v_lossless_encoder.run_enc(self.clip, self.file)
            self.clip = core.lsmas.LWLibavSource(self.file.name_clip_output_lossless.to_str())

        if not self.file.name_clip_output.exists():
            self.config.v_encoder.run_enc(self.clip, self.file)
            self.cleanup_files.add(self.file.name_clip_output)
            if self.file.do_qpfile:
                self.cleanup_files.add(self.file.qpfile)

    def _audio_getter(self) -> None:  # noqa C901
        if self.config.a_extracters:
            a_extracters = self._check_if_sequence(self.config.a_extracters)
            for a_extracter in a_extracters:
                if self.file.a_src and not any(self.file.a_src.set_track(n).exists() for n in a_extracter.track_out):
                    a_extracter.run()
                    for n in a_extracter.track_out:
                        self.cleanup_files.add(self.file.a_src.set_track(n))

        if self.config.a_cutters:
            a_cutters = self._check_if_sequence(self.config.a_cutters)
            for i, a_cutter in enumerate(a_cutters, start=1):
                if self.file.a_src_cut and not self.file.a_src_cut.set_track(i).exists():
                    a_cutter.run()
                    self.cleanup_files.add(self.file.a_src_cut.set_track(i))

        if self.config.a_encoders:
            a_encoders = self._check_if_sequence(self.config.a_encoders)
            for i, a_encoder in enumerate(a_encoders, start=1):
                if self.file.a_enc_cut and not self.file.a_enc_cut.set_track(i).exists():
                    a_encoder.run()
                    self.cleanup_files.add(self.file.a_enc_cut.set_track(i))

    @staticmethod
    def _check_if_sequence(seq: Union[T, Sequence[T]]) -> Sequence[T]:
        return cast(Sequence[T], seq) if isinstance(seq, Sequence) else cast(Sequence[T], [seq])

    def _muxer(self) -> None:
        if self.config.muxer:
            wfs = self.config.muxer.run()
            self.cleanup_files.update(wfs)
