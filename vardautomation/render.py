"""Node rendering helpers"""

from enum import IntEnum

import vapoursynth as vs
from rich.progress import BarColumn, Progress, TextColumn, TimeRemainingColumn
from vstools import clip_async_render

from .utils import Properties

__all__ = ["clip_async_render"]


def get_render_progress() -> Progress:
    return Progress(
        TextColumn("{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        TextColumn("{task.percentage:>3.02f}%"),
        TimeRemainingColumn(),
    )


class SceneChangeMode(IntEnum):
    WWXD = 11
    SCXVID = 22
    MV = 44


def find_scene_changes(
    clip: vs.VideoNode,
    mode: int | SceneChangeMode = SceneChangeMode.WWXD,
    *,
    scxvid_use_slices: bool = False,
    mv_vectors: vs.VideoNode | None = None,
    mv_thscd1: int | None = None,
    mv_thscd2: int | None = None,
) -> list[int]:
    """
    Generate a list of scene changes (keyframes).

    Dependencies:

    * vapoursynth-wwxd
    * vapoursynth-scxvid (Optional: scxvid mode)

    :param clip:   Clip to search for scene changes. Will be rendered in its entirety.
    :param mode:   Scene change detection mode:

                   * WWXD: Use wwxd
                   * SCXVID: Use scxvid
                   * WWXD_SCXVID_UNION: Union of wwxd and sxcvid (must be detected by at least one)
                   * WWXD_SCXVID_INTERSECTION: Intersection of wwxd and scxvid (must be detected by both)

    :return:       List of scene changes.
    """
    frames: list[int] = []
    props: list[str] = []
    clip = clip.resize.Bilinear(640, 360, format=vs.YUV420P8)
    scm = SceneChangeMode
    wwxd_unions = {scm.WWXD | scm.SCXVID, scm.WWXD | scm.MV, scm.WWXD | scm.SCXVID | scm.MV}
    wwxd_inters = {scm.WWXD & scm.SCXVID, scm.WWXD & scm.MV, scm.WWXD & scm.SCXVID & scm.MV}
    scxvid_unions = {scm.SCXVID | scm.WWXD, scm.SCXVID | scm.MV, scm.SCXVID | scm.WWXD | scm.MV}
    scxvid_inters = {scm.SCXVID & scm.WWXD, scm.SCXVID & scm.MV, scm.SCXVID & scm.WWXD & scm.MV}
    mv_unions = {scm.MV | scm.WWXD, scm.MV | scm.SCXVID, scm.MV | scm.WWXD | scm.SCXVID}
    mv_inters = {scm.MV & scm.WWXD, scm.MV & scm.SCXVID, scm.MV & scm.WWXD & scm.SCXVID}

    # SCXVID and mv share the same prop
    # https://github.com/dubhater/vapoursynth-scxvid/issues/3
    if mode in {scm.WWXD} | wwxd_unions | wwxd_inters:
        clip = clip.wwxd.WWXD()
        props.append("Scenechange")
    if mode in {scm.SCXVID} | scxvid_unions | scxvid_inters:
        clip = clip.scxvid.Scxvid(use_slices=scxvid_use_slices)
        props.append("_SceneChangePrev")
    if mode in {scm.MV} | mv_unions | mv_inters:
        if not mv_vectors:
            mv_vectors = clip.mv.Super().mv.Analyse()
        clip = clip.mv.SCDetection(mv_vectors, mv_thscd1, mv_thscd2)
        props.append("_SceneChangePrev")

    def _cb(n: int, f: vs.VideoFrame) -> None:
        match mode:
            case scm.WWXD | scm.SCXVID | scm.MV:
                if Properties.get_prop(f, props[0], int):
                    frames.append(n)
            case _ if mode in wwxd_unions | scxvid_unions | mv_unions:
                if any(Properties.get_prop(f, p, int) for p in props):
                    frames.append(n)
            case _ if mode in wwxd_inters | scxvid_inters | mv_inters:
                if all(Properties.get_prop(f, p, int) for p in props):
                    frames.append(n)
            case _:
                pass

    clip_async_render(clip, progress="Detecting scene changes...", callback=_cb)

    return sorted(frames)
