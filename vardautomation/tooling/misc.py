
__all__ = [
    'Qpfile', 'make_qpfile',
    'KeyframesFile', 'get_keyframes',
    'get_vs_core', 'SubProcessAsync'
]

import asyncio
import inspect
import os
from fractions import Fraction
from itertools import accumulate
from typing import Iterable, List, NamedTuple, Optional, Union

import psutil
import vapoursynth as vs
from pytimeconv import Convert

from .._logging import logger
from ..binary_path import BinaryPath
from ..render import SceneChangeMode as SCM
from ..render import find_scene_changes
from ..types import AnyPath
from ..vpathlib import VPath
from .base import BasicTool


class Qpfile(NamedTuple):
    """Simple namedtuple for a qpfile"""

    path: VPath
    """Qpfile path"""

    frames: Optional[List[int]] = None
    """List of keyframes"""


def make_qpfile(clip: vs.VideoNode, path: Optional[AnyPath] = None, /,
                overwrite: bool = True, mode: Union[int, SCM] = SCM.WWXD | SCM.SCXVID) -> Qpfile:
    """
    Convenience function for making a qpfile

    :param clip:            Source clip
    :param path:            Path where the qpfile will be written.
                            Default to the name of the script that run this function with the ".log" extension
    :param overwrite:       If True, will overwrite the file
    :param mode:            Scene change mode, defaults to SCM.WWXD_SCXVID_UNION
    :return:                A Qpfile
    """
    path = VPath(inspect.stack()[-1].filename).with_suffix('.log') if not path else VPath(path)

    if not overwrite and path.exists():
        logger.critical(f'make_qpfile: a qpfile already exists at "{path.resolve().to_str()}"')

    num_threads = vs.core.num_threads
    if (oscpu := os.cpu_count()) is not None:
        vs.core.num_threads = oscpu
    scenes = find_scene_changes(clip, mode)
    vs.core.num_threads = num_threads

    with path.open('w', encoding='utf-8') as file:
        file.writelines(f'{s} K\n' for s in scenes)
    return Qpfile(path, scenes)


class KeyframesFile(NamedTuple):
    """Simple namedtuple for a keyframes file"""

    path: VPath
    """Keyframe file path"""

    frames: List[int]
    """List of keyframes"""


def get_keyframes(path: AnyPath) -> KeyframesFile:
    """
    Get the keyframes of a video using ffmsindex

    :param path:        Path of the video
    :return:            A KeyframesFile
    """
    logger.debug(path)
    path = VPath(path)

    idx_file = path.parent / 'index.ffindex'
    kf_file = idx_file.with_suffix(idx_file.suffix + '_track00.kf.txt')

    BasicTool(BinaryPath.ffmsindex, ['-p', '-k', '-f', path.to_str(), idx_file.to_str()]).run()
    idx_file.rm()

    with kf_file.open('r', encoding='utf-8') as kfio:
        file = KeyframesFile(
            kf_file,
            [int(kf) for kf in kfio.read().splitlines()[2:]]
        )
    return file


def get_vs_core(threads: Optional[Iterable[int]] = None, max_cache_size: Optional[int] = None) -> vs.Core:
    """
    Get the VapourSynth singleton core. Optionaly, set the number of threads used
    and the maximum cache size

    :param threads:         An iteratable of thread numbers, defaults to None.
    :param max_cache_size:  Set the upper framebuffer cache size after which memory is aggressively freed.
                            The value is in megabytes, defaults to None.
    :return:                Vapoursynth Core.
    """
    core = vs.core.core

    if threads is not None:
        threads = list(threads)
        core.num_threads = len(threads)
        p_handle = psutil.Process()
        p_handle.cpu_affinity(threads)

    if max_cache_size is not None:
        core.max_cache_size = max_cache_size

    return core


def make_tcfile(clips: Iterable[vs.VideoNode], path: Optional[AnyPath] = None, precision: int = 6) -> VPath:
    """
    Convenience function for making a tcfile

    :param clips:       Source clips
    :param path:        tcfile path
    :param precision:   Precision of fps
    :return:            tcfile path
    """
    num_frames, fpss, times = list[int](), list[Fraction](), list[float]()

    for clip in clips:
        num_frames.append(clip.num_frames)
        fpss.append(clip.fps)
        times.append(Convert.f2seconds(clip.num_frames, clip.fps))

    start_frames = accumulate(num_frames[:-1], lambda x, y: x + y, initial=0)
    end_frames = accumulate(num_frames[1:], lambda x, y: x + y, initial=num_frames[0] - 1)

    path = VPath(inspect.stack()[-1].filename).with_suffix('.tcfile') if not path else VPath(path)

    with path.open('w', encoding='utf-8') as file:
        file.write('# timestamp format v1\n')
        file.write(f'assume {round(sum(num_frames) / sum(times), precision)}\n')  # type: ignore[arg-type]
        file.writelines(
            f'{s},{e},{round(float(fps), precision)}\n'
            for s, e, fps in zip(start_frames, end_frames, fpss)
        )

    return path


class SubProcessAsync:
    __slots__ = ('sem', )

    sem: asyncio.Semaphore

    @logger.catch
    def __init__(self, cmds: List[str], /, *, nb_cpus: Optional[int] = os.cpu_count()) -> None:
        if nb_cpus:
            self.sem = asyncio.Semaphore(nb_cpus)
        else:
            raise ValueError(f'{self.__class__.__name__}: no CPU found!')

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
        logger.debug(cmd)
        async with self.sem:
            return await self._run_cmd(cmd)

    @staticmethod
    async def _run_cmd(cmd: str) -> None:
        proc = await asyncio.create_subprocess_shell(cmd)
        logger.debug(cmd)
        await proc.communicate()
