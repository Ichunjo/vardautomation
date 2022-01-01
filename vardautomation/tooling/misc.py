
__all__ = [
    'Qpfile', 'make_qpfile', 'get_vs_core', 'SubProcessAsync'
]

import asyncio
import inspect
import os
from typing import Iterable, List, NamedTuple, Optional

import psutil
import vapoursynth as vs

from ..render import SceneChangeMode as SCM
from ..render import find_scene_changes
from ..status import Status
from ..types import AnyPath
from ..vpathlib import VPath


class Qpfile(NamedTuple):
    """Simple namedtuple for a qpfile"""

    path: VPath
    """Qpfile path"""

    frames: Optional[List[int]] = None
    """List of keyframes"""


def make_qpfile(clip: vs.VideoNode, path: Optional[AnyPath] = None, /,
                overwrite: bool = True, mode: SCM = SCM.WWXD_SCXVID_UNION) -> Qpfile:
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
        Status.fail(f'make_qpfile: a qpfile already exists at "{path.resolve().to_str()}"')

    num_threads = vs.core.num_threads
    if (oscpu := os.cpu_count()) is not None:
        vs.core.num_threads = oscpu
    scenes = find_scene_changes(clip, mode)
    vs.core.num_threads = num_threads

    with path.open('w', encoding='utf-8') as file:
        file.writelines(f'{s} K\n' for s in scenes)
    return Qpfile(path, scenes)


def get_vs_core(threads: Optional[Iterable[int]] = None, max_cache_size: Optional[int] = None) -> vs.Core:
    """
    Get the VapourSynth singleton core. Optionaly, set the number of threads used
    and the maximum cache size

    :param threads:         An iteratable of thread numbers, defaults to None.
    :param max_cache_size:  Set the upper framebuffer cache size after which memory is aggressively freed.
                            The value is in megabytes, defaults to None.
    :return:                Vapoursynth Core.
    """
    core = vs.core

    if threads is not None:
        threads = list(threads)
        core.num_threads = len(threads)
        p_handle = psutil.Process()
        p_handle.cpu_affinity(threads)

    if max_cache_size is not None:
        core.max_cache_size = max_cache_size

    return core


class SubProcessAsync:
    __slots__ = ('sem', )

    sem: asyncio.Semaphore

    def __init__(self, cmds: List[str], /, *, nb_cpus: Optional[int] = os.cpu_count()) -> None:
        if nb_cpus:
            self.sem = asyncio.Semaphore(nb_cpus)
        else:
            Status.fail(f'{self.__class__.__name__}: no CPU found!', exception=ValueError)

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
        async with self.sem:
            return await self._run_cmd(cmd)

    @staticmethod
    async def _run_cmd(cmd: str) -> None:
        proc = await asyncio.create_subprocess_shell(cmd)
        await proc.communicate()
