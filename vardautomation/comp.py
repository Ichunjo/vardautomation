"""Comparison module"""

__all__ = ['make_comps', 'Writer']

import os
import random
import subprocess
from enum import Enum, auto
from functools import partial
from typing import (Any, Callable, Collection, Dict, Final, Iterable, List,
                    Optional, Set)

import numpy as np
import vapoursynth as vs
from lvsfunc.util import get_prop
from requests import Session
from requests_toolbelt import MultipartEncoder
from vardefunc.types import Zimg
from vardefunc.util import select_frames

from .binary_path import BinaryPath
from .status import Colours, Status
from .tooling import SubProcessAsync, VideoEncoder
from .types import AnyPath
from .vpathlib import VPath

_MAX_ATTEMPTS_PER_PICTURE_TYPE: Final[int] = 50


class Writer(Enum):
    """Writer to be used to extract frames"""

    FFMPEG = auto()
    """ffmpeg encoder"""

    IMWRI = auto()
    """core.imwri.Write Vapoursynth plugin"""

    OPENCV = auto()
    """opencv library"""

    PILLOW = auto()
    """Pillow library"""

    PYQT = auto()
    """PyQt library"""

    PYTHON = auto()
    """Pure python implementation"""

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__}.{self.name}>'


def make_comps(clips: Dict[str, vs.VideoNode], path: AnyPath = 'comps',  # noqa: C901
               num: int = 15, frames: Optional[Iterable[int]] = None, *,
               picture_types: Optional[Iterable[str]] = None,
               force_bt709: bool = False,
               writer: Writer = Writer.PYTHON, compression: int = -1,
               magick_compare: bool = False,
               slowpics: bool = False, collection_name: str = '', public: bool = True) -> None:
    """
    Extract frames, make diff between two clips and upload to slow.pics

    :param clips:               Named clips.
    :param path:                Path to your comparison folder, defaults to 'comps'
    :param num:                 Number of frames to extract, defaults to 15
    :param frames:              Additionnal frame numbers that will be added to the total of ``num``, defaults to None
    :param picture_types        Select picture types to pick, default to None
    :param force_bt709:         Force BT709 matrix before conversion to RGB24, defaults to False
    :param writer:              Writer method to be used, defaults to Writer.OPENCV
    :param compression:         Compression level. It depends of the writer used, defaults to -1 which means automatic selection
    :param magick_compare:      Make diffs between the first and second clip
                                Will raise an exception if more than 2 clips are passed to clips, defaults to False
    :param slowpics:            Upload to slow.pics, defaults to False
    :param collection_name:     Slowpics's collection name, defaults to ''
    :param public:              Make the comparison public, defaults to True
    """
    # pylint: disable=consider-using-f-string
    # Check length of all clips
    lens = set(c.num_frames for c in clips.values())
    if len(lens) != 1:
        Status.fail('make_comps: "clips" must be equal length!', exception=ValueError)

    # Make samples
    if picture_types:
        Status.info('make_comps: Make samples according to specified picture types...')
        samples = _select_samples_with_picture_types(clips.values(), lens.pop(), num, picture_types)
    else:
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
        Status.fail(f'make_comps: path "{path.to_str()}" already exists!', exception=ValueError, chain_err=file_err)

    # Extracts the requested frames using ffmpeg
    # imwri lib is slower even asynchronously requested
    for name, clip in clips.items():
        path_name = path / name
        try:
            path_name.mkdir(parents=True)
        except FileExistsError as file_err:
            Status.fail(f'make_comps: {path_name.to_str()} already exists!', exception=FileExistsError, chain_err=file_err)

        clip = clip.resize.Bicubic(
            format=vs.RGB24, matrix_in=vs.MATRIX_BT709 if force_bt709 else None,
            dither_type=Zimg.DitherType.ERROR_DIFFUSION
        )

        path_images = [
            path_name / (f'{name}_' + f'{f}'.zfill(len("%i" % max_num)) + '.png')
            for f in frames
        ]

        if writer == Writer.FFMPEG:
            clip = select_frames(clip, frames)

            # -> RGB -> GBR. Needed for ffmpeg
            # Also FPS=1/1. I'm just lazy, okay?
            clip = clip.std.ShufflePlanes([1, 2, 0], vs.RGB).std.AssumeFPS(fpsnum=1, fpsden=1)

            outputs: List[str] = []
            for i, path_image in enumerate(path_images):
                outputs += ['-compression_level', str(compression), '-pred', 'mixed', '-ss', f'{i}', '-t', '1', f'{path_image.to_str()}']

            settings = [
                '-hide_banner', '-loglevel', 'error', '-f', 'rawvideo',
                '-video_size', f'{clip.width}x{clip.height}',
                '-pixel_format', 'gbrp', '-framerate', str(clip.fps),
                '-i', 'pipe:', *outputs
            ]

            VideoEncoder(BinaryPath.ffmpeg, settings, progress_update=_progress_update_func).run_enc(clip, None, y4m=False)

        elif writer == Writer.IMWRI:
            reqs = clip.imwri.Write(
                'PNG', (path_name / (f'{name}_%' + f'{len("%i" % max_num)}'.zfill(2) + 'd.jpg')).to_str(),
                quality=compression if compression >= 0 else None
            )
            clip = select_frames(reqs, frames)
            # zzzzzzzzz soooo slow
            with open(os.devnull, 'wb') as devnull:
                clip.output(devnull, y4m=False, progress_update=_progress_update_func)

        else:
            clip = select_frames(clip, frames)
            clip = clip.std.ModifyFrame(clip, partial(_saver(writer, compression), path_images=path_images))
            with open(os.devnull, 'wb') as devnull:
                clip.output(devnull, y4m=False, progress_update=_progress_update_func)


    # Make diff images
    if magick_compare:
        if len(clips) > 2:
            Status.fail('make_comps: "magick_compare" can only be used with two clips!', exception=ValueError)

        path_diff = path / 'diffs'
        try:
            subprocess.call(['magick', 'compare'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            path_diff.mkdir(parents=True)
        except FileNotFoundError as file_not_found:
            Status.fail('make_comps: "magick compare" was not found!', exception=FileNotFoundError, chain_err=file_not_found)
        except FileExistsError as file_err:
            Status.fail(f'make_comps: {path_diff.to_str()} already exists!', exception=FileExistsError, chain_err=file_err)

        all_images = [sorted((path / name).glob('*.png')) for name in clips.keys()]
        images_a, images_b = all_images

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
            'optimizeImages': 'true',
            'hentai': 'false'
        }

        for i, (name, images) in enumerate(
            zip(list(clips.keys()) + (['diff'] if magick_compare else []),
                all_images)
        ):
            for j, (image, frame) in enumerate(zip(images, frames)):
                fields[f'comparisons[{j}].name'] = str(frame)
                fields[f'comparisons[{j}].images[{i}].name'] = name
                fields[f'comparisons[{j}].images[{i}].file'] = (image.name, image.read_bytes(), 'image/png')

        sess = Session()
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
        Status.info(f'url file copied to "{url_file.resolve().to_str()}"')


def _select_samples_with_picture_types(clips: Collection[vs.VideoNode], num_frames: int, k: int, picture_types: Iterable[str]) -> Set[int]:
    samples: Set[int] = set()
    p_type = [p.upper() for p in picture_types]

    _max_attempts = 0
    _rnum_checked: Set[int] = set()
    while len(samples) < k:
        _attempts = 0

        while True:
            # Check if we don't exceed the length of the clips
            # if yes then that means we checked all the frames
            if len(_rnum_checked) < num_frames:
                rnum = _rand_num_frames(_rnum_checked, partial(random.randrange, start=0, stop=num_frames))
                _rnum_checked.add(rnum)
            else:
                Status.fail(f'make_comps: There are not enough of {p_type} in these clips', exception=ValueError)

            # Check _PictType
            if all(
                get_prop(f, '_PictType', bytes).decode('utf-8') in p_type
                for f in vs.core.std.Splice([select_frames(c, [rnum]) for c in clips], mismatch=True).frames()
            ):
                break
            _attempts += 1
            _max_attempts += 1

            if _attempts > _MAX_ATTEMPTS_PER_PICTURE_TYPE:
                Status.warn(
                    f'make_comps: {_MAX_ATTEMPTS_PER_PICTURE_TYPE} attempts were made for sample {len(samples)} '
                    f'and no match found for {p_type}; stopping iteration...'
                )
                break

        if _max_attempts > (curr_max_att := _MAX_ATTEMPTS_PER_PICTURE_TYPE * k):
            Status.fail(f'make_comps: attempts max of {curr_max_att} has been reached!', exception=RecursionError)

        if _attempts < _MAX_ATTEMPTS_PER_PICTURE_TYPE:
            samples.add(rnum)

    return samples


def _rand_num_frames(checked: Set[int], rand_func: Callable[[], int]) -> int:
    rnum = rand_func()
    while rnum in checked:
        rnum = rand_func()
    return rnum


def _saver(writer: Writer, compression: int) -> Callable[[int, vs.VideoFrame, List[VPath]], vs.VideoFrame]:  # noqa: C901
    # pylint: disable=import-outside-toplevel
    if writer == Writer.OPENCV:
        try:
            import cv2
        except ImportError as imp_err:
            Status.fail('make_comps: you need opencv to use this writer', exception=ValueError, chain_err=imp_err)

        opencv_compression = [cv2.IMWRITE_PNG_COMPRESSION, compression] if compression >= 0 else []

        def _opencv(n: int, f: vs.VideoFrame, path_images: List[VPath]) -> vs.VideoFrame:
            frame_array = np.dstack(tuple(reversed(f)))  # type: ignore
            cv2.imwrite(path_images[n].to_str(), frame_array, opencv_compression)
            return f
        return _opencv

    if writer == Writer.PILLOW:
        try:
            from PIL import Image
        except ImportError as imp_err:
            Status.fail('make_comps: you need Pillow to use this writer', exception=ValueError, chain_err=imp_err)

        def _pillow(n: int, f: vs.VideoFrame, path_images: List[VPath]) -> vs.VideoFrame:
            frame_array = np.dstack(f)  # type: ignore
            img = Image.fromarray(frame_array, 'RGB')  # type: ignore
            img.save(path_images[n], format='PNG', optimize=False, compress_level=abs(compression))
            return f
        return _pillow

    if writer == Writer.PYQT:
        try:
            from PyQt5.QtGui import QImage
        except ImportError as imp_err:
            Status.fail('make_comps: you need pyqt to use this writer', exception=ValueError, chain_err=imp_err)

        def _pyqt(n: int, f: vs.VideoFrame, path_images: List[VPath]) -> vs.VideoFrame:
            frame_array = np.dstack(f)  # type: ignore
            image = QImage(frame_array.tobytes(), f.width, f.height, 3 * f.width, QImage.Format.Format_RGB888)
            image.save(path_images[n].to_str(), 'PNG', -1)
            return f
        return _pyqt

    if writer == Writer.PYTHON:
        import struct
        import zlib

        def _write_png(buf: bytes, width: int, height: int) -> bytes:
            # reverse the vertical line order and add null bytes at the start
            width_byte_3 = width * 3
            raw_data = b''.join(
                b'\x00' + buf[span:span + width_byte_3]
                for span in range((height - 1) * width_byte_3, -1, - width_byte_3)
            )

            def _png_pack(png_tag: bytes, data: bytes) -> bytes:
                chunk_head = png_tag + data
                return (struct.pack("!L", len(data))
                        + chunk_head
                        + struct.pack("!L", 0xFFFFFFFF & zlib.crc32(chunk_head)))

            return b''.join([
                # http://www.w3.org/TR/PNG/#5PNG-file-signature
                struct.pack('8B', 137, 80, 78, 71, 13, 10, 26, 10),
                # https://www.w3.org/TR/PNG/#11IHDR
                _png_pack(b'IHDR', struct.pack("!2I5B", width, height, 8, 2, 0, 0, 0)),
                _png_pack(b'IDAT', zlib.compress(raw_data, compression)),
                _png_pack(b'IEND', b'')])

        def _python_png(n: int, f: vs.VideoFrame, path_images: List[VPath]) -> vs.VideoFrame:
            frame_bytes = _write_png(np.dstack(f).tobytes(), f.width, f.height)  # type: ignore
            path_images[n].write_bytes(frame_bytes)
            return f
        return _python_png

    Status.fail(f'make_comps: unknown writer! "{writer}"', exception=ValueError)


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


def _progress_update_func(value: int, endvalue: int) -> None:
    return print(f"\r{Colours.INFO}Extrating image: {value}/{endvalue} ~ {round(100 * value / endvalue, 2)}%{Colours.RESET}", end="")
