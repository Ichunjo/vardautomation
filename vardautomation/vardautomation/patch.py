"""Path module"""

__all__ = ['Patch']

import platform
import shutil
from subprocess import call
from typing import NoReturn, Optional, Tuple

import vapoursynth as vs

from .automation import BasicTool, VideoEncoder
from .config import FileInfo
from .vpathlib import AnyPath, VPath


class Patch():  # noqa
    """Allow easy video patching"""
    ffmsindex: str = 'ffmsindex'
    mkvmerge: str = 'mkvmerge'

    workdir: VPath
    fix_raw: VPath
    fix_mkv: VPath

    file_to_fix: VPath
    filtered_clip: vs.VideoNode
    frame_start: int
    frame_end: int
    encoder: VideoEncoder
    file: FileInfo
    output_filename: Optional[str]

    def __init__(self,
                 file_to_fix: AnyPath, filtered_clip: vs.VideoNode,
                 frame_start: int, frame_end: int,
                 encoder: VideoEncoder, file: FileInfo, *,
                 output_filename: Optional[str] = None) -> None:
        """TODO: Make a proper docstring

        Args:
            file_to_fix (AnyPath): [description]
            filtered_clip (vs.VideoNode): [description]
            frame_start (int): [description]
            frame_end (int): [description]
            encoder (VideoEncoder): [description]
            file (FileInfo): [description]
            output_filename (Optional[str], optional): [description]. Defaults to None.
        """
        self.file_to_fix = VPath(file_to_fix).resolve()
        self.filtered_clip = filtered_clip
        self.frame_start = frame_start
        self.frame_end = frame_end
        self.encoder = encoder
        self.file = file
        self.output_filename = output_filename

        whech = self._where_which()
        if call([whech, self.ffmsindex]) != 0:
            self._throw_error(self.ffmsindex)
        if call([whech, self.mkvmerge]) != 0:
            self._throw_error(self.mkvmerge)

    def run(self) -> None:
        """Launch patch"""
        # Local folder
        self.workdir = self.file_to_fix.parent / (self.file.name + '_temp')
        self.workdir.mkdir()
        self.fix_raw = self.workdir / 'fix'
        self.fix_mkv = self.workdir / 'fix.mkv'

        start, end = self._generate_keyframes()
        self._encode(self.filtered_clip[start:end])
        self._cut_and_merge(start, end)

    def cleanup(self) -> None:
        """Delete workdir folder"""
        shutil.rmtree(self.workdir, ignore_errors=True)

    def _generate_keyframes(self) -> Tuple[int, int]:
        idx_file = f'{self.workdir}/index.ffindex'
        kf_file = f'{idx_file}_track00.kf.txt'

        idxing = BasicTool(self.ffmsindex, ['-k', '-f', str(self.file_to_fix), idx_file])
        idxing.run()

        with open(kf_file, 'r', encoding='utf-8') as f:
            kfsstr = f.read().splitlines()

        kfsint = list(map(int, kfsstr[2:]))
        # Add the last frame
        kfsint.append(self.filtered_clip.num_frames)


        fra_s, fra_e = None, None

        for i, kf in enumerate(kfsint):
            if kf > self.frame_start:
                fra_s = kfsint[i-1]
                break
            if kf == self.frame_start:
                fra_s = kf
                break

        for i, kf in enumerate(kfsint):
            if kf >= self.frame_end:
                fra_e = kf
                break

        if fra_s is None or fra_e is None:
            raise ValueError('Something is wrong in frame_start or frame_end')

        return fra_s, fra_e

    def _encode(self, clip: vs.VideoNode) -> None:
        self.file.name_clip_output = self.fix_raw

        self.encoder.run_enc(clip, self.file)

        merge = BasicTool('mkvmerge', ['-o', str(self.fix_mkv), str(self.fix_raw)])
        merge.run()

    def _cut_and_merge(self, start: int, end: int) -> None:
        name = self.file_to_fix.stem
        tmp = self.workdir / f'{name}_tmp.mkv'
        tmpnoaudio = self.workdir / f'{name}_tmp_noaudio.mkv'

        final = self.file_to_fix.parent
        if self.output_filename is not None:
            final /= self.output_filename
        else:
            final /= f'{name}_new.mkv'


        if start == 0:
            split_args = ['--split', f'frames:{end}']
        else:
            split_args = ['--split', f'frames:{start},{end}']
        merge = BasicTool(self.mkvmerge, ['-o', str(tmp), '--no-audio', '--no-track-tags', '--no-chapters', str(self.file_to_fix), *split_args])
        merge.run()


        tmp001 = self.workdir / f'{tmp.stem}-001.mkv'
        tmp002 = self.workdir / f'{tmp.stem}-002.mkv'
        tmp003 = self.workdir / f'{tmp.stem}-003.mkv'

        if start == 0:
            merge_args = [str(self.fix_mkv), '+', str(tmp002)]
        elif end == self.filtered_clip.num_frames:
            merge_args = [str(tmp001), '+', str(self.fix_mkv)]
        else:
            merge_args = [str(tmp001), '+', str(self.fix_mkv), '+', str(tmp003)]

        merge = BasicTool(self.mkvmerge, ['-o', str(tmpnoaudio), '--no-audio', '--no-track-tags', '--no-chapters', *merge_args])
        merge.run()
        merge = BasicTool(self.mkvmerge, ['-o', str(final), str(tmpnoaudio), '--no-video', str(self.file_to_fix)])
        merge.run()

    @staticmethod
    def _where_which() -> str:
        return 'where' if platform.system() == 'Windows' else 'which'

    @staticmethod
    def _throw_error(file_not_found: str) -> NoReturn:
        raise FileNotFoundError(f'{file_not_found} not found!')
