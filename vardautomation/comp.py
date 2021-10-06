"""Comparison module"""

__all__ = [
    # Enums
    'Writer', 'PictureType',

    # Dicts
    'SlowPicsConf', 'default_conf',

    # Class and function
    'Comparison', 'make_comps'
]

import inspect
import os
import random
import subprocess
from enum import Enum, auto
from functools import partial
from typing import (Any, Callable, Dict, Final, Iterable, Iterator, List,
                    Literal, Optional, Sequence, Set, TypedDict, final)

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

# pylint: disable=consider-using-f-string


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


@final
class PictureTypes(Iterable[bytes]):
    def __init__(self, iterable: Sequence[bytes]) -> None:
        self.__ptseq = iterable

    def __iter__(self) -> Iterator[bytes]:
        return iter(self.__ptseq)


class PictureType(Enum):
    """A simple enum to cover all the choices of the selected picture types."""
    I = PictureTypes([b'I'])  # noqa E741
    """I frames only"""

    IP = PictureTypes([b'I', b'P'])
    """I and P frames"""

    IPB = PictureTypes([b'I', b'P', b'B'])
    """I, P and B frames"""

    P = PictureTypes([b'P'])
    """P frames only"""

    PB = PictureTypes([b'P', b'B'])
    """P and B frames"""

    B = PictureTypes([b'B'])
    """B frames only"""


class SlowPicsConf(TypedDict, total=False):
    """TypedDict configuration for Slowpics"""

    collectionName: str
    """Slowpics's collection name"""

    public: Literal['true', 'false']
    """Make the comparison public"""

    optimizeImages: Literal['true', 'false']
    """If 'true", images will be losslessly optimised"""

    hentai: Literal['true', 'false']
    """If images not suitable for minors (nudity, gore, etc.)"""

    removeAfter: str
    """Remove after N days"""


default_conf: SlowPicsConf = SlowPicsConf(
    collectionName=VPath(inspect.stack()[-1].filename).stem,
    public='true', optimizeImages='true', hentai='false'
)
"""Default Slowpics's configuration """


class Comparison:
    """Can extract frames, make diff between two clips and upload to slow.pics"""

    def __init__(self, clips: Dict[str, vs.VideoNode], path: AnyPath = 'comps',
                 num: int = 15, frames: Optional[Iterable[int]] = None,
                 picture_type: Optional[PictureType] = None) -> None:
        """
        :param clips:               Named clips.
        :param path:                Path to your comparison folder, defaults to 'comps'
        :param num:                 Number of frames to extract, defaults to 15
        :param frames:              Additionnal frame numbers that will be added to the total of ``num``, defaults to None
        :param picture_type         Select picture types to pick, default to None
        """
        self.clips = clips
        self.path = VPath(path)
        self.path_diff: Optional[VPath] = None

        # Check length of all clips
        lens = set(c.num_frames for c in clips.values())
        if len(lens) != 1:
            Status.fail('make_comps: "clips" must be equal length!', exception=ValueError)

        try:
            self.path.mkdir(parents=True)
        except FileExistsError as file_err:
            Status.fail(f'make_comps: path "{self.path.to_str()}" already exists!', exception=ValueError, chain_err=file_err)

        # Make samples
        if picture_type:
            Status.info('make_comps: Make samples according to specified picture types...')
            samples = self._select_samples_ptypes(lens.pop(), num, picture_type.value)
        else:
            samples = set(random.sample(range(lens.pop()), num))

        # Add additionnal frames if frame exists
        if frames:
            samples.update(frames)
        self.max_num = max(samples)
        self.frames = sorted(samples)

    def extract(self, writer: Writer = Writer.PYTHON, compression: int = -1, force_bt709: bool = False) -> None:
        """
        Extract images from the specified clips in the constructor

        :param writer:              Writer method to be used, defaults to Writer.PYTHON
        :param compression:         Compression level. It depends of the writer used, defaults to -1 which means automatic selection
        :param force_bt709:         Force BT709 matrix before conversion to RGB24, defaults to False
        """
        for name, clip in self.clips.items():
            path_name = self.path / name
            try:
                path_name.mkdir(parents=True)
            except FileExistsError as file_err:
                Status.fail(f'make_comps: {path_name.to_str()} already exists!', exception=FileExistsError, chain_err=file_err)

            clip = clip.resize.Bicubic(
                format=vs.RGB24, matrix_in=vs.MATRIX_BT709 if force_bt709 else None,
                dither_type=Zimg.DitherType.ERROR_DIFFUSION
            )

            path_images = [
                path_name / (f'{name}_' + f'{f}'.zfill(len("%i" % self.max_num)) + '.png')
                for f in self.frames
            ]
            # Extracts the requested frames using ffmpeg
            if writer == Writer.FFMPEG:
                clip = select_frames(clip, self.frames)

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
            # imwri lib is slower even asynchronously requested
            elif writer == Writer.IMWRI:
                reqs = clip.imwri.Write(
                    'PNG', (path_name / (f'{name}_%' + f'{len("%i" % self.max_num)}'.zfill(2) + 'd.jpg')).to_str(),
                    quality=compression if compression >= 0 else None
                )
                clip = select_frames(reqs, self.frames)
                # zzzzzzzzz soooo slow
                with open(os.devnull, 'wb') as devnull:
                    clip.output(devnull, y4m=False, progress_update=_progress_update_func)
                print()
            else:
                clip = select_frames(clip, self.frames)
                clip = clip.std.ModifyFrame(clip, partial(_saver(writer, compression), path_images=path_images))
                with open(os.devnull, 'wb') as devnull:
                    clip.output(devnull, y4m=False, progress_update=_progress_update_func)
                print()

    def magick_compare(self) -> None:
        """
        Make an image of differences between the first and second clip using ImageMagick.
        Will raise an exception if more than 2 clips are passed to the constructor.
        """
        # Make diff images
        if len(self.clips) > 2:
            Status.fail('make_comps: "magick_compare" can only be used with two clips!', exception=ValueError)

        self.path_diff = self.path / 'diffs'
        try:
            subprocess.call(['magick', 'compare'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            self.path_diff.mkdir(parents=True)
        except FileNotFoundError as file_not_found:
            Status.fail('make_comps: "magick compare" was not found!', exception=FileNotFoundError, chain_err=file_not_found)
        except FileExistsError as file_err:
            Status.fail(f'make_comps: {self.path_diff.to_str()} already exists!', exception=FileExistsError, chain_err=file_err)

        all_images = [sorted((self.path / name).glob('*.png')) for name in self.clips.keys()]
        images_a, images_b = all_images

        cmds = [
            f'magick compare "{i1.to_str()}" "{i2.to_str()}" "{self.path_diff.to_str()}/diff_' + f'{f}'.zfill(len("%i" % self.max_num)) + '.png"'
            for i1, i2, f in zip(images_a, images_b, self.frames)
        ]

        # Launch asynchronously the Magick commands
        Status.info('Diffing clips...')
        print()
        SubProcessAsync(cmds)

    def upload_to_slowpics(self, config: SlowPicsConf = default_conf) -> None:
        """
        Upload to slow.pics with given configuration

        :param config:              TypeDict which contains the uploading configuration, defaults to :py:data`.default_conf`
        """
        # Upload to slow.pics
        all_images = [sorted((self.path / name).glob('*.png')) for name in self.clips.keys()]
        if self.path_diff:
            all_images.append(sorted(self.path_diff.glob('*.png')))  # type: ignore

        fields: Dict[str, Any] = {}

        for i, (name, images) in enumerate(
            zip(list(self.clips.keys()) + (['diff'] if self.path_diff else []),
                all_images)
        ):
            for j, (image, frame) in enumerate(zip(images, self.frames)):
                fields[f'comparisons[{j}].name'] = str(frame)
                fields[f'comparisons[{j}].images[{i}].name'] = name
                fields[f'comparisons[{j}].images[{i}].file'] = (image.name, image.read_bytes(), 'image/png')

        with Session() as sess:
            sess.get('https://slow.pics/api/comparison')
            # TODO: yeet this
            files = MultipartEncoder(config | fields)

            Status.info('Uploading images...')
            print()
            url = sess.post(
                'https://slow.pics/api/comparison', data=files.to_string(),
                headers=_get_slowpics_header(str(files.len), files.content_type, sess)
            )

        slowpics_url = f'https://slow.pics/c/{url.text}'
        Status.info(f'Slowpics url: {slowpics_url}')

        url_file = self.path / 'slow.pics.url'
        url_file.write_text(f'[InternetShortcut]\nURL={slowpics_url}', encoding='utf-8')
        Status.info(f'url file copied to "{url_file.resolve().to_str()}"')

    def _select_samples_ptypes(self, num_frames: int, k: int, picture_types: PictureTypes) -> Set[int]:
        samples: Set[int] = set()
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
                    Status.fail(f'make_comps: There are not enough of {picture_types} in these clips', exception=ValueError)

                # Check _PictType
                if all(
                    get_prop(f, '_PictType', bytes) in picture_types
                    for f in vs.core.std.Splice([select_frames(c, [rnum]) for c in self.clips.values()], mismatch=True).frames()
                ):
                    break
                _attempts += 1
                _max_attempts += 1

                if _attempts > _MAX_ATTEMPTS_PER_PICTURE_TYPE:
                    Status.warn(
                        f'make_comps: {_MAX_ATTEMPTS_PER_PICTURE_TYPE} attempts were made for sample {len(samples)} '
                        f'and no match found for {picture_types}; stopping iteration...'
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
            Status.fail('comp: you need opencv to use this writer', exception=ValueError, chain_err=imp_err)

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
            Status.fail('comp: you need Pillow to use this writer', exception=ValueError, chain_err=imp_err)

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
            Status.fail('comp: you need pyqt to use this writer', exception=ValueError, chain_err=imp_err)

        def _pyqt(n: int, f: vs.VideoFrame, path_images: List[VPath]) -> vs.VideoFrame:
            frame_array = np.dstack(f)  # type: ignore
            image = QImage(frame_array.tobytes(), f.width, f.height, 3 * f.width, QImage.Format.Format_RGB888)  # type: ignore
            image.save(path_images[n].to_str(), 'PNG', compression)
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

    Status.fail(f'comp: unknown writer! "{writer}"', exception=ValueError)


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
    return print(
        "\r%sExtracting image: %i/%i ~ %.2f %%%s" % (
            Colours.INFO,
            value, endvalue, 100 * value / endvalue,
            Colours.RESET
        ),
        end=""
    )
