"""Properties and helpers functions"""
import subprocess
from functools import wraps
from typing import Any, Callable, Dict, List, Tuple, Type, TypeVar, Union

import vapoursynth as vs

from ._logging import logger
from .status import VSColourRangeError, VSSubsamplingError
from .types import AnyPath, T

core = vs.core


@logger.catch
class Properties:
    """Collection of methods to get some properties from the parameters and/or the clip"""

    @classmethod
    def get_colour_range(cls, params: List[str], clip: vs.VideoNode) -> Tuple[int, int]:
        """
        Get the luma colour range specified in the params.
        Fallback to the clip properties.

        :param params:              Settings of the encoder.
        :param clip:                Source
        :return:                    A tuple of min_luma and max_luma value
        """
        bits = cls.get_depth(clip)

        def _get_props(clip: vs.VideoNode) -> vs.FrameProps:
            with clip.get_frame(0) as frame:
                props = frame.props
            return props

        if '--range' in params:
            rng_param = params[params.index('--range') + 1]
            if rng_param == 'limited':
                min_luma = 16 << (bits - 8)
                max_luma = 235 << (bits - 8)
            elif rng_param == 'full':
                min_luma = 0
                max_luma = (1 << bits) - 1
            else:
                raise VSColourRangeError(f'{cls.__name__}: Wrong range in parameters!')
        elif '_ColorRange' in (props := _get_props(clip)):
            color_rng = props['_ColorRange']
            if color_rng == 1:
                min_luma = 16 << (bits - 8)
                max_luma = 235 << (bits - 8)
            elif color_rng == 0:
                min_luma = 0
                max_luma = (1 << bits) - 1
            else:
                raise VSColourRangeError(f'{cls.__name__}: Wrong "_ColorRange" prop in the clip!')
        else:
            raise VSColourRangeError(f'{cls.__name__}: Cannot guess the color range!')

        return min_luma, max_luma

    @staticmethod
    def get_depth(clip: vs.VideoNode, /) -> int:
        """
        Returns the bit depth of a VideoNode as an integer.

        :param clip:            Source clip
        :return:                Bitdepth
        """
        assert clip.format
        return clip.format.bits_per_sample

    @staticmethod
    def get_csp(clip: vs.VideoNode) -> str:
        """
        Get the colourspace a the given clip based on its format

        :param clip:            Source clip
        :return:                Colourspace suitable for x264
        """
        def _get_csp_subsampled(format_clip: vs.VideoFormat) -> str:
            sub_w, sub_h = format_clip.subsampling_w, format_clip.subsampling_h
            csp_yuv_subs: Dict[Tuple[int, int], str] = {(0, 0): 'i444', (1, 0): 'i422', (1, 1): 'i420'}
            try:
                return csp_yuv_subs[(sub_w, sub_h)]
            except KeyError as k_err:
                raise VSSubsamplingError(f'{Properties.__name__}: wrong subsampling "{(sub_w, sub_h)}"') from k_err

        assert clip.format

        csp_avc = {
            vs.GRAY: 'i400',
            vs.YUV: _get_csp_subsampled(clip.format),
            vs.RGB: 'rgb'
        }
        return csp_avc[clip.format.color_family]

    @staticmethod
    def get_encoder_name(path: AnyPath) -> str:
        """
        Get the encoder name from the file's tags

        :param path:            File path
        :return:                Encoder name
        """
        ffprobe_args = ['ffprobe', '-loglevel', 'quiet', '-show_entries', 'format_tags=encoder',
                        '-print_format', 'default=nokey=1:noprint_wrappers=1', str(path)]
        return subprocess.check_output(ffprobe_args, shell=True, encoding='utf-8')

    @staticmethod
    def get_prop(frame: vs.VideoFrame, key: str, t: Type[T]) -> T:
        """
        Gets FrameProp ``prop`` from frame ``frame`` with expected type ``t``
        to satisfy the type checker.
        Function borrowed from lvsfunc.

        :param frame:           Frame containing props
        :param key:             Prop to get
        :param t:               Type of prop

        :return:                frame.prop[key]
        """
        try:
            prop = frame.props[key]
        except KeyError as key_err:
            raise KeyError(f"get_prop: 'Key {key} not present in props'") from key_err

        if not isinstance(prop, t):
            raise ValueError(f"get_prop: 'Key {key} did not contain expected type: Expected {t} got {type(prop)}'")

        return prop



def recursive_dict(obj: object) -> Union[Dict[str, Any], str]:
    # pylint: disable=no-else-return
    if hasattr(obj, '__dict__') and obj.__dict__:
        return {k: recursive_dict(v) for k, v in obj.__dict__.items()}
    else:
        if isinstance(obj, vs.VideoNode):
            return repr(obj)
        else:
            return str(obj)


F = TypeVar('F', bound=Callable[..., Any])


def copy_docstring_from(original: Callable[..., Any], mode: str = 'o') -> Callable[[F], F]:
    """
    :param original:        Original function
    :param mode:            Copy mode. Can be 'o+t', 't+o', 'o', defaults to 'o'
    """
    @wraps(original)
    def wrapper(target: F) -> F:
        if target.__doc__ is None:
            target.__doc__ = ''
        if original.__doc__ is None:
            original.__doc__ = ''

        if mode == 'o':
            target.__doc__ = original.__doc__
        elif mode == 'o+t':
            target.__doc__ = original.__doc__ + target.__doc__
        elif mode == 't+o':
            target.__doc__ += original.__doc__
        else:
            with logger.catch_ctx():
                raise ValueError('copy_docstring_from: Wrong mode!')
        return target

    return wrapper
