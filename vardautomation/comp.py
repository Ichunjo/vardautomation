"""Comparison module"""

__all__ = ['make_comps', 'Writer']

import random
import subprocess
from enum import Enum
from typing import Any, Dict, List, Optional, Sequence

import vapoursynth as vs
from lvsfunc.render import clip_async_render
from requests import Session, session
from requests_toolbelt import MultipartEncoder  # type: ignore
from vardefunc.types import Zimg

from .status import Status
from .tooling import SubProcessAsync, VideoEncoder
from .types import AnyPath
from .vpathlib import VPath


class Writer(Enum):
    FFMPEG = 0
    IMWRI = 1


def make_comps(clips: Dict[str, vs.VideoNode], path: AnyPath = 'comps',
               num: int = 15, frames: Optional[Sequence[int]] = None, *,
               force_bt709: bool = False,
               writer: Writer = Writer.FFMPEG,
               magick_compare: bool = False,
               slowpics: bool = False, collection_name: str = '', public: bool = True) -> None:
    """Extract frames, make diff between two clips and upload to slow.pics

    Args:
        clips (Dict[str, vs.VideoNode]):
            Named clips.

        path (AnyPath, optional):
            Path to your comparison folder. Defaults to 'comps'.

        num (int, optional):
            Number of frames to extract. Defaults to 15.

        frames (Optional[Sequence[int]], optional):
            Additionnal frame numbers that will be added to the total of `num`.
            Defaults to None.

        force_bt709 (bool, optional):
            Force BT709 matrix before conversion to RGB24.
            Defaults to False.

        magick_compare (bool, optional):
            Make diffs between the first and second clip.
            Will raise an exception if more than 2 clips are passed to clips.
            Defaults to False.

        slowpics (bool, optional):
            Upload to slow.pics. Defaults to False.

        collection_name (str, optional):
            Slowpics's collection name. Defaults to ''.

        public (bool, optional):
            Make the comparison public. Defaults to True.
    """
    # Check length of all clips
    lens = set(c.num_frames for c in clips.values())
    if len(lens) != 1:
        Status.fail('generate_comp: "clips" must be equal length!', exception=ValueError)

    # Make samples
    samples = set(random.sample(range(lens.pop()), num))

    # Add additionnal frames if frame exists
    if frames:
        samples.update(frames)
    max_num = max(samples)
    frames = sorted(samples)

    path = VPath(path)
    try:
        path.mkdir(parents=True)
    except FileExistsError as file_err:
        Status.fail('make_comps: "path" already exists!', exception=ValueError, chain_err=file_err)

    # Extracts the requested frames using ffmpeg
    # imwri lib is slower even asynchronously requested
    for name, clip in clips.items():

        path_name = path / name
        try:
            path_name.mkdir(parents=True)
        except FileExistsError as file_err:
            Status.fail(f'make_comps: {path_name.to_str()} already exists!',
                        exception=FileExistsError, chain_err=file_err)

        clip = clip.resize.Bicubic(
            format=vs.RGB24, matrix_in=Zimg.Matrix.BT709 if force_bt709 else None,
            dither_type=Zimg.DitherType.ERROR_DIFFUSION
        )

        if writer == Writer.FFMPEG:
            clip = vs.core.std.Splice([clip[f] for f in frames])

            # -> RGB -> GBR. Needed for ffmpeg
            # Also FPS=1/1. I'm just lazy, okay?
            clip = clip.std.ShufflePlanes([1, 2, 0], vs.RGB).std.AssumeFPS(fpsnum=1, fpsden=1)

            path_images = [
                path_name / (f'{name}_' + f'{f}'.zfill(len("%i" % max_num)) + '.png')
                for f in frames
            ]

            outputs: List[str] = []
            for i, path_image in enumerate(path_images):
                outputs += ['-pred', 'mixed', '-ss', f'{i}', '-t', '1', f'{path_image.to_str()}']

            settings = [
                '-hide_banner', '-loglevel', 'error', '-f', 'rawvideo',
                '-video_size', f'{clip.width}x{clip.height}',
                '-pixel_format', 'gbrp', '-framerate', str(clip.fps),
                '-i', 'pipe:', *outputs
            ]

            VideoEncoder('ffmpeg', settings, progress_update=None).run_enc(clip, None, y4m=False)
            print('\n')

        else:
            reqs = clip.imwri.Write(
                'PNG', (path_name / (f'{name}_%' + f'{len("%i" % max_num)}'.zfill(2) + 'd.png')).to_str()
            )
            clip = vs.core.std.Splice([reqs[f] for f in frames])
            # zzzzzzzzz soooo slow
            clip_async_render(clip)


    # Make diff images
    if magick_compare:
        if len(clips) > 2:
            Status.fail('make_comps: "magick_compare" can only be used with two clips!', exception=ValueError)

        try:
            subprocess.call(['magick', 'compare'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        except FileNotFoundError as file_not_found:
            Status.fail(
                'make_comps: "magick compare" was not found!',
                exception=FileNotFoundError, chain_err=file_not_found
            )

        all_images = [sorted((path / name).glob('*.png')) for name in clips.keys()]
        images_a, images_b = all_images

        path_diff = path / 'diffs'
        try:
            path_diff.mkdir(parents=True)
        except FileExistsError as file_err:
            Status.fail(f'make_comps: {path_diff.to_str()} already exists!', exception=FileExistsError, chain_err=file_err)

        cmds = [
            f'magick compare "{i1.to_str()}" "{i2.to_str()}" "{path_diff.to_str()}/diff_' + f'{f}'.zfill(len("%i" % max_num)) + '.png"'
            for i1, i2, f in zip(images_a, images_b, frames)
        ]

        # Launch asynchronously the Magick commands
        Status.info('Diffing clips...\n')
        SubProcessAsync(cmds)


    # Upload to slow.pics
    if slowpics:
        all_images = [sorted((path / name).glob('*.png')) for name in clips.keys()]
        if magick_compare:
            all_images.append(sorted(path_diff.glob('*.png')))  # type: ignore

        fields: Dict[str, Any] = {
            'collectionName': collection_name,
            'public': str(public).lower(),
            'optimize-images': 'true'
        }

        for i, (name, images) in enumerate(
            zip(list(clips.keys()) + (['diff'] if magick_compare else []),
                all_images)
        ):
            for j, (image, frame) in enumerate(zip(images, frames)):
                fields[f'comparisons[{j}].name'] = str(frame)
                fields[f'comparisons[{j}].images[{i}].name'] = name
                fields[f'comparisons[{j}].images[{i}].file'] = (image.name, image.read_bytes(), 'image/png')

        sess = session()
        sess.get('https://slow.pics/api/comparison')
        # TODO: yeet this
        files = MultipartEncoder(fields)

        Status.info('Uploading images...\n')
        url = sess.post(
            'https://slow.pics/api/comparison', data=files.to_string(),
            headers=_get_slowpics_header(str(files.len), files.content_type, sess)
        )
        sess.close()

        slowpics_url = f'https://slow.pics/c/{url.text}'
        Status.info(f'Slowpics url: {slowpics_url}')

        url_file = path / 'slow.pics.url'
        url_file.write_text(f'[InternetShortcut]\nURL={slowpics_url}', encoding='utf-8')
        Status.info(f'url file copied to {url_file}')


def _get_slowpics_header(content_length: str, content_type: str, sess: Session) -> Dict[str, str]:
    return {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.5",
        "Content-Length": content_length,
        "Content-Type": content_type,
        "Origin": "https://slow.pics/",
        "Referer": "https://slow.pics/comparison",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "X-XSRF-TOKEN": sess.cookies.get_dict()["XSRF-TOKEN"]
    }
