"""Path module"""

__all__ = ['Patch']

import shutil
from itertools import chain
from typing import List, Optional, Set, Tuple, Union

import vapoursynth as vs
from vardefunc.types import Range
from vardefunc.util import normalise_ranges

from .binary_path import BinaryPath
from .config import FileInfo
from .status import Status
from .tooling import BasicTool, VideoEncoder
from .vpathlib import VPath


class Patch:
    """Allow easy video patching"""
    encoder: VideoEncoder
    clip: vs.VideoNode
    file: FileInfo
    ranges: List[Tuple[int, int]]
    debug: bool

    workdir: VPath
    output_filename: VPath

    _file_to_fix: VPath

    def __init__(self, encoder: VideoEncoder, clip: vs.VideoNode, file: FileInfo,
                 ranges: Union[Range, List[Range]],
                 output_filename: Optional[str] = None, *, debug: bool = False) -> None:
        """Patching your videos has never been so easy!"""
        self.encoder = encoder
        self.clip = clip
        self.file = file
        self.file.do_qpfile = False

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
            Status.fail(f'{self.__class__.__name__}: {self.workdir.resolve().to_str()} already exists!', exception=FileExistsError)

    def run(self) -> None:
        """Launch patch"""
        # Local folder
        self.workdir.mkdir()
        self._resolve_range()
        self._encode()
        self._cut_and_merge()

    def do_cleanup(self) -> None:
        """Delete workdir folder"""
        shutil.rmtree(self.workdir, ignore_errors=True)

    def _resolve_range(self) -> None:
        idx_file = self.workdir / 'index.ffindex'
        kf_file = idx_file.with_suffix(idx_file.suffix + '_track00.kf.txt')

        BasicTool(
            BinaryPath.ffmsindex,
            ['-k', '-f', self._file_to_fix.to_str(), idx_file.to_str()]
        ).run()

        with kf_file.open('r', encoding='utf-8') as f:
            kfsstr = f.read().splitlines()

        # Convert to int and add the last frame
        kfsint = [int(x) for x in kfsstr[2:]] + [self.clip.num_frames]

        ranges = self._bound_to_keyframes(kfsint)
        if self.debug:
            print('--------------------------------')
            print('_bound_to_keyframes', ranges)
            print('--------------------------------')
        nranges = normalise_ranges(self.clip, ranges, norm_dups=True)
        if self.debug:
            print('--------------------------------')
            print('norm_dups', ranges)
            print('--------------------------------')

        if len(nranges) == 1:
            if nranges[0][0] == 0 and nranges[0][1] == self.clip.num_frames:
                Status.fail(f'{self.__class__.__name__}: Don\'t use Patch, just redo your encode', exception=ValueError)

        self.ranges = nranges

    def _encode(self) -> None:
        for i, (s, e) in enumerate(self.ranges, start=1):
            if self.debug:
                print('--------------------------------')
                print((s, e))
                print('--------------------------------')
            fix = self.workdir / f'fix-{i:03.0f}'
            self.file.name_clip_output = fix
            self.encoder.run_enc(self.clip[s:e], self.file)

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
                Status.fail('_bound_to_keyframes: Something is wrong in `s` or `e`', exception=ValueError)

            rng_set.add((s, e))

        return sorted(rng_set)
