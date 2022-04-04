"""Comparison module"""

__all__ = [
    # Enums
    'Writer', 'PictureType',

    # Dicts
    'SlowPicsConf',

    # Class and function
    'Comparison', 'make_comps'
]

import inspect
import os
import random
import subprocess
from enum import Enum, auto
from functools import partial
from typing import Any, Callable, Dict, Final, Iterable, List, NamedTuple, Optional, Set

import numpy as np
import vapoursynth as vs
from numpy.typing import NDArray
from requests import Session
from requests_toolbelt import MultipartEncoder
from vardefunc.types import Zimg
from vardefunc.util import select_frames

from ._logging import logger
from .binary_path import BinaryPath
from .tooling import SubProcessAsync, VideoEncoder
from .types import AnyPath
from .utils import Properties
from .vpathlib import VPath

_MAX_ATTEMPTS_PER_PICTURE_TYPE: Final[int] = 50

# pylint: disable=consider-using-f-string


class Writer(Enum):
    """Writer to be used to extract frames"""

    FFMPEG = auto()
    """FFmpeg encoder"""

    IMWRI = auto()
    """vapoursynth.core.imwri Vapoursynth plugin"""

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


class PictureType(bytes, Enum):
    """A simple enum for picture types."""
    I = b'I'  # noqa E741
    """I frames"""

    P = b'P'
    """P frames"""

    B = b'B'
    """B frames"""


class SlowPicsConf(NamedTuple):
    """Slow.pics configuration"""
    collection_name: str = VPath(inspect.stack()[-1].filename).stem
    """
    Slowpics's collection name.\n
    Default is the name of the current script
    """

    public: bool = True
    """Make the comparison public"""

    optimise: bool = True
    """If 'true", images will be losslessly optimised"""

    nsfw: bool = False
    """If images not suitable for minors (nudity, gore, etc.)"""

    remove_after: Optional[int] = None
    """Remove after N days"""


class Comparison:
    """Extract frames, make diff between two clips and upload to slow.pics"""

    @logger.catch
    def __init__(self, clips: Dict[str, vs.VideoNode], path: AnyPath = 'comps',
                 num: int = 15, frames: Optional[Iterable[int]] = None,
                 picture_type: Optional[PictureType | List[PictureType]] = None) -> None:
        """
        :param clips:               Named clips.
        :param path:                Path to your comparison folder, defaults to 'comps'
        :param num:                 Number of frames to extract, defaults to 15
        :param frames:              Additionnal frame numbers that will be added to the total of ``num``, defaults to None
        :param picture_type:        Select picture types to pick, default to None
        """
        self.clips = clips
        self.path = VPath(path)
        self.path_diff: Optional[VPath] = None

        # Check length of all clips
        lens = set(c.num_frames for c in clips.values())
        if len(lens) != 1:
            logger.warning(f'{self.__class__.__name__}: "clips" doesn\'t have the same length!')
        lens_n = min(lens)

        try:
            self.path.mkdir(parents=True)
        except FileExistsError as file_err:
            raise ValueError(f'{self.__class__.__name__}: path "{self.path.to_str()}" already exists!') from file_err

        # Make samples
        if picture_type:
            logger.info(f'{self.__class__.__name__}: Make samples according to specified picture types...')
            samples = self._select_samples_ptypes(lens_n, num, picture_type)
        else:
            samples = set(random.sample(range(lens_n), num))

        # Add additionnal frames if frame exists
        if frames:
            samples.update(frames)
        self.max_num = max(samples)
        self.frames = sorted(samples)

    @logger.catch
    def extract(self, writer: Writer = Writer.PYTHON, compression: int = -1, force_bt709: bool = False) -> None:
        """
        Extract images from the specified clips in the constructor

        :param writer:              Writer method to be used, defaults to Writer.PYTHON
        :param compression:         Compression level. It depends of the writer used, defaults to -1 which means automatic selection
        :param force_bt709:         Force BT709 matrix before conversion to RGB24, defaults to False
        """
        # pylint: disable=cell-var-from-loop
        for name, clip in self.clips.items():
            path_name = self.path / name
            try:
                path_name.mkdir(parents=True)
            except FileExistsError as file_err:
                logger.critical(f'{self.__class__.__name__}: {path_name.to_str()} already exists!', file_err)

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
                    outputs.extend([
                        '-compression_level', str(compression), '-pred', 'mixed',
                        '-ss', f'{i}', '-t', '1', f'{path_image.to_str()}'
                    ])

                settings = [
                    '-hide_banner', '-loglevel', 'error', '-f', 'rawvideo',
                    '-video_size', f'{clip.width}x{clip.height}',
                    '-pixel_format', 'gbrp', '-framerate', str(clip.fps),
                    '-i', 'pipe:'
                ]
                settings.extend(outputs)

                encoder = VideoEncoder(BinaryPath.ffmpeg, settings)
                encoder.progress_update = _progress_update_func
                encoder.y4m = False
                encoder.run_enc(clip, None)
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
                logger.logger.opt(raw=True).info('\n')
            else:
                clip = select_frames(clip, self.frames)
                clip = clip.std.ModifyFrame(clip, lambda n, f: _saver(writer, compression)(n, f, path_images))
                with open(os.devnull, 'wb') as devnull:
                    clip.output(devnull, y4m=False, progress_update=_progress_update_func)
                logger.logger.opt(raw=True).info('\n')

    @logger.catch
    def magick_compare(self) -> None:
        """
        Make an image of differences between the first and second clip using ImageMagick.
        Will raise an exception if more than 2 clips are passed to the constructor.
        """
        # Make diff images
        if len(self.clips) > 2:
            raise ValueError(f'{self.__class__.__name__}: "magick_compare" can only be used with two clips!')

        self.path_diff = self.path / 'diffs'
        try:
            subprocess.call(['magick', 'compare'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            self.path_diff.mkdir(parents=True)
        except FileNotFoundError as f_err:
            logger.critical(f'{self.__class__.__name__}: "magick compare" was not found!', f_err)
        except FileExistsError as f_err:
            logger.critical(f'{self.__class__.__name__}: {self.path_diff.to_str()} already exists!', f_err)

        all_images = [sorted((self.path / name).glob('*.png')) for name in self.clips.keys()]
        images_a, images_b = all_images

        cmds = [
            f'magick compare "{i1.to_str()}" "{i2.to_str()}" '
            + f'"{self.path_diff.to_str()}/diff_' + f'{f}'.zfill(len("%i" % self.max_num)) + '.png"'
            for i1, i2, f in zip(images_a, images_b, self.frames)
        ]

        # Launch asynchronously the Magick commands
        logger.info('Diffing clips...')
        SubProcessAsync(cmds)
        logger.logger.opt(raw=True).info('\n')

    @logger.catch
    def upload_to_slowpics(self, config: SlowPicsConf) -> None:
        """
        Upload to slow.pics with given configuration

        :param config:              NamedTuple which contains the uploading configuration
        """
        # Upload to slow.pics
        all_images = [sorted((self.path / name).glob('*.png')) for name in self.clips.keys()]
        if self.path_diff:
            all_images.append(sorted(self.path_diff.glob('*.png')))

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
            files = MultipartEncoder(_make_api_compatible(config) | fields)

            logger.info('Uploading images...\n')
            logger.logger.opt(raw=True).info('\n')
            url = sess.post(
                'https://slow.pics/api/comparison', data=files.to_string(),
                headers=_get_slowpics_header(str(files.len), files.content_type, sess)
            )

        slowpics_url = f'https://slow.pics/c/{url.text}'
        logger.info(f'Slowpics url: {slowpics_url}')

        url_file = self.path / 'slow.pics.url'
        url_file.write_text(f'[InternetShortcut]\nURL={slowpics_url}', encoding='utf-8')
        logger.info(f'url file copied to "{url_file.resolve().to_str()}"')

    @logger.catch
    def _select_samples_ptypes(self, num_frames: int, k: int, picture_types: PictureType | List[PictureType]) -> Set[int]:
        samples: Set[int] = set()
        _max_attempts = 0
        _rnum_checked: Set[int] = set()
        picture_types = picture_types if isinstance(picture_types, list) else [picture_types]
        while len(samples) < k:
            _attempts = 0

            while True:
                # Check if we don't exceed the length of the clips
                # if yes then that means we checked all the frames
                if len(_rnum_checked) >= num_frames:
                    raise ValueError(f'{self.__class__.__name__}: There are not enough of {picture_types} in these clips')
                rnum = _rand_num_frames(_rnum_checked, partial(random.randrange, start=0, stop=num_frames))
                _rnum_checked.add(rnum)

                # Check _PictType
                if all(
                    Properties.get_prop(f, '_PictType', bytes) in picture_types
                    for f in vs.core.std.Splice([select_frames(c, [rnum]) for c in self.clips.values()], mismatch=True).frames()
                ):
                    break
                _attempts += 1
                _max_attempts += 1

                if _attempts > _MAX_ATTEMPTS_PER_PICTURE_TYPE:
                    logger.warning(
                        f'{self.__class__.__name__}: {_MAX_ATTEMPTS_PER_PICTURE_TYPE} attempts were made for sample {len(samples)} '
                        f'and no match found for {picture_types}; stopping iteration...'
                    )
                    break

            if _max_attempts > (curr_max_att := _MAX_ATTEMPTS_PER_PICTURE_TYPE * k):
                raise RecursionError(f'{self.__class__.__name__}: attempts max of {curr_max_att} has been reached!')

            if _attempts < _MAX_ATTEMPTS_PER_PICTURE_TYPE:
                samples.add(rnum)
                logger.info(
                    "\rSelecting image: %i/%i ~ %.2f %%" % (
                        len(samples), k, 100 * len(samples) / k
                    )
                )

        logger.logger.opt(raw=True).info('\n')
        return samples


def make_comps(
    clips: Dict[str, vs.VideoNode], path: AnyPath = 'comps',
    num: int = 15, frames: Optional[Iterable[int]] = None, *,
    picture_types: Optional[PictureType | List[PictureType]] = None,
    force_bt709: bool = False,
    writer: Writer = Writer.PYTHON, compression: int = -1,
    magick_compare: bool = False,
    slowpics_conf: Optional[SlowPicsConf] = None
) -> None:
    """
    Convenience function for :py:class:`Comparison`.

    :param clips:               Named clips.
    :param path:                Path to your comparison folder, defaults to 'comps'
    :param num:                 Number of frames to extract, defaults to 15
    :param frames:              Additionnal frame numbers that will be added to the total of num, defaults to None
    :param picture_types:       Select picture types to pick, default to None
    :param force_bt709:         Force BT709 matrix before conversion to RGB24, defaults to False
    :param writer:              Writer method to be used, defaults to Writer.PYTHON
    :param compression:         Compression level. It depends of the writer used, defaults to -1 which means automatic selection
    :param magick_compare:      Make diffs between the first and second clip.
                                Will raise an exception if more than 2 clips are passed to clips, defaults to False
    :param slowpics_conf:       slow.pics configuration. If specified, images will be uploaded following this configuration
    """
    comp = Comparison(clips, path, num, frames, picture_types)
    comp.extract(writer, compression, force_bt709)
    if magick_compare:
        comp.magick_compare()
    if slowpics_conf is not None:
        comp.upload_to_slowpics(slowpics_conf)


def _rand_num_frames(checked: Set[int], rand_func: Callable[[], int]) -> int:
    rnum = rand_func()
    while rnum in checked:
        rnum = rand_func()
    return rnum


@logger.catch
def _saver(writer: Writer, compression: int) -> Callable[[int, vs.VideoFrame, List[VPath]], vs.VideoFrame]:  # noqa: C901
    if writer == Writer.OPENCV:
        try:
            import cv2
        except ImportError as imp_err:
            raise ValueError('comp: you need opencv to use this writer') from imp_err

        opencv_compression = [cv2.IMWRITE_PNG_COMPRESSION, compression] if compression >= 0 else []

        def _opencv(n: int, f: vs.VideoFrame, path_images: List[VPath]) -> vs.VideoFrame:
            frame_array = np.dstack(tuple(reversed(f)))  # type: ignore[var-annotated]
            cv2.imwrite(path_images[n].to_str(), frame_array, opencv_compression)
            return f
        return _opencv

    if writer == Writer.PILLOW:
        try:
            from PIL import Image
        except ImportError as imp_err:
            raise ValueError('comp: you need Pillow to use this writer') from imp_err

        def _pillow(n: int, f: vs.VideoFrame, path_images: List[VPath]) -> vs.VideoFrame:
            frame_array: NDArray[Any] = np.dstack(f)  # type: ignore[call-overload]
            img = Image.fromarray(frame_array, 'RGB')  # type: ignore[pylance-strict]
            img.save(path_images[n], format='PNG', optimize=False, compress_level=abs(compression))
            return f
        return _pillow

    if writer == Writer.PYQT:
        try:
            from PyQt5.QtGui import QImage
        except ImportError as imp_err:
            raise ValueError('comp: you need pyqt to use this writer') from imp_err

        def _pyqt(n: int, f: vs.VideoFrame, path_images: List[VPath]) -> vs.VideoFrame:
            frame_array: NDArray[Any] = np.dstack(f)  # type: ignore[call-overload]
            # pylint: disable=no-member
            image = QImage(frame_array.tobytes(), f.width, f.height, 3 * f.width, QImage.Format_RGB888)
            image.save(path_images[n].to_str(), 'PNG', compression)
            return f
        return _pyqt

    if writer == Writer.PYTHON:
        import struct
        import zlib

        def _write_png(buf: bytes, width: int, height: int) -> bytes:
            # add null bytes at the start
            width_byte_3 = width * 3
            raw_data = b''.join(
                b'\x00' + buf[span:span + width_byte_3]
                for span in range(0, (height + 1) * width_byte_3, width_byte_3)
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
            # pylint: disable=no-member
            frame_bytes = _write_png(np.dstack(f).tobytes(), f.width, f.height)  # type: ignore[call-overload]
            path_images[n].write_bytes(frame_bytes)
            return f
        return _python_png

    raise ValueError(f'comp: unknown writer! "{writer}"')


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


def _make_api_compatible(config: SlowPicsConf) -> Dict[str, str]:
    conf = {
        'collectionName': config.collection_name,
        'public': str(config.public).lower(),
        'optimizeImages': str(config.optimise).lower(),
        'hentai': str(config.nsfw).lower(),
    }
    if config.remove_after is not None:
        conf.update({'removeAfter': str(config.remove_after)})
    return conf


def _progress_update_func(value: int, endvalue: int) -> None:
    if value == 0:
        return
    logger.logger.opt(raw=True, colors=True).info(
        logger.info.colour
        + "\rExtracting image: %i/%i ~ %.2f %%" % (value, endvalue, 100 * value / endvalue)
        + logger.info.colour_close
    )
