"""Automation module"""

__all__ = [
    'Parser', 'RunnerConfig', 'SelfRunner',
]

import argparse
from os import remove
from typing import NamedTuple, Optional, Sequence, Set, Tuple, Union

import vapoursynth as vs

from .config import FileInfo
from .status import Status
from .tooling import (AudioCutter, AudioEncoder, AudioExtracter,
                      LosslessEncoder, Mux, VideoEncoder)
from .types import AnyPath

core = vs.core


class Parser:
    """Parser implementation. Still WIP"""

    def __init__(self, file: FileInfo) -> None:
        """[summary]

        :param file: [description]
        :type file: FileInfo
        """
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
        """Parse the args from the constructor"""
        # Lossless check
        if self.args.lossless:
            file.do_lossless = True

        # Qpfile check
        if self.args.qpfile:
            file.do_qpfile = True

        if self.args.start or self.args.end:
            Status.fail('', exception=NotImplementedError)

        return file, clip


class RunnerConfig(NamedTuple):
    """Config for the SelfRunner"""
    v_encoder: VideoEncoder
    v_lossless_encoder: Optional[LosslessEncoder] = None
    a_extracters: Union[AudioExtracter, Sequence[AudioExtracter], None] = None
    a_cutters: Union[AudioCutter, Sequence[AudioCutter], None] = None
    a_encoders: Union[AudioEncoder, Sequence[AudioEncoder], None] = None
    muxer: Optional[Mux] = None


class SelfRunner:
    """Self runner interface"""
    clip: vs.VideoNode
    file: FileInfo
    config: RunnerConfig

    cleanup_files: Set[AnyPath]

    def __init__(self, clip: vs.VideoNode, file: FileInfo, /, config: RunnerConfig) -> None:
        self.clip = clip
        self.file = file
        self.config = config
        self.cleanup_files = set()


    def run(self) -> None:
        """Tool chain"""
        self._parsing()
        self._encode()
        self._audio_getter()
        self._muxer()

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

    def _audio_getter(self) -> None:
        if a_extracters := self.config.a_extracters:
            a_extracters = a_extracters if isinstance(a_extracters, Sequence) else [a_extracters]
            for i, a_extracter in enumerate(a_extracters, start=1):
                if self.file.a_src and not self.file.a_src.set_track(i).exists():
                    a_extracter.run()
                    self.cleanup_files.add(self.file.a_src.set_track(i))

        if a_cutters := self.config.a_cutters:
            a_cutters = a_cutters if isinstance(a_cutters, Sequence) else [a_cutters]
            for i, a_cutter in enumerate(a_cutters, start=1):
                if self.file.a_src_cut and not self.file.a_src_cut.set_track(i).exists():
                    a_cutter.run()
                    self.cleanup_files.add(self.file.a_src_cut.set_track(i))

        if a_encoders := self.config.a_encoders:
            a_encoders = a_encoders if isinstance(a_encoders, Sequence) else [a_encoders]
            for i, a_encoder in enumerate(a_encoders, start=1):
                if self.file.a_enc_cut and not self.file.a_enc_cut.set_track(i).exists():
                    a_encoder.run()
                    self.cleanup_files.add(self.file.a_enc_cut.set_track(i))

    def _muxer(self) -> None:
        if self.config.muxer:
            wfs = self.config.muxer.run()
            self.cleanup_files.update(wfs)

    def do_cleanup(self, *extra_files: AnyPath) -> None:
        """Delete working files"""
        self.cleanup_files.update(extra_files)
        for files in self.cleanup_files:
            remove(files)
        self.cleanup_files.clear()
