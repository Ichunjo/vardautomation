
__all__ = [
    'Qpfile', 'make_qpfile', 'SubProcessAsync'
]

import asyncio
import os
from typing import List, NamedTuple, Optional

import vapoursynth as vs
from lvsfunc.render import SceneChangeMode as SCM
from lvsfunc.render import find_scene_changes

from ..status import Status
from ..types import AnyPath
from ..vpathlib import VPath


class Qpfile(NamedTuple):
    """Simple namedtuple for a qpfile"""

    path: VPath
    """Qpfile path"""

    frames: Optional[List[int]] = None
    """List of keyframes"""


def make_qpfile(clip: vs.VideoNode, path: AnyPath, /, mode: SCM = SCM.WWXD_SCXVID_UNION) -> Qpfile:
    """
    Convenience function for making a qpfile

    :param clip:            Source clip
    :param path:            Path where the qpfile will be written
    :param mode:            Scene change mode. See lvsfunc docs for more information,
                            defaults to SCM.WWXD_SCXVID_UNION
    :return:                A Qpfile
    """
    path = VPath(path)
    if path.exists():
        Status.fail(f'make_qpfile: a qpfile already exists at {path.resolve().to_str()}')

    scenes = find_scene_changes(clip, mode)
    with path.open('w', encoding='utf-8') as file:
        file.writelines(f'{s} K\n' for s in scenes)
    return Qpfile(path, scenes)


class SubProcessAsync:
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
