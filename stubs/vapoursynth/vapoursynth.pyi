# Stop pep8 from complaining (hopefully)
# NOQA

# Ignore Flake Warnings
# flake8: noqa

# Ignore coverage
# (No coverage)

# From https://gist.github.com/pylover/7870c235867cf22817ac5b096defb768
# noinspection PyPep8
# noinspection PyPep8Naming
# noinspection PyTypeChecker
# noinspection PyAbstractClass
# noinspection PyArgumentEqualDefault
# noinspection PyArgumentList
# noinspection PyAssignmentToLoopOrWithParameter
# noinspection PyAttributeOutsideInit
# noinspection PyAugmentAssignment
# noinspection PyBroadException
# noinspection PyByteLiteral
# noinspection PyCallByClass
# noinspection PyChainedComparsons
# noinspection PyClassHasNoInit
# noinspection PyClassicStyleClass
# noinspection PyComparisonWithNone
# noinspection PyCompatibility
# noinspection PyDecorator
# noinspection PyDefaultArgument
# noinspection PyDictCreation
# noinspection PyDictDuplicateKeys
# noinspection PyDocstringTypes
# noinspection PyExceptClausesOrder
# noinspection PyExceptionInheritance
# noinspection PyFromFutureImport
# noinspection PyGlobalUndefined
# noinspection PyIncorrectDocstring
# noinspection PyInitNewSignature
# noinspection PyInterpreter
# noinspection PyListCreation
# noinspection PyMandatoryEncoding
# noinspection PyMethodFirstArgAssignment
# noinspection PyMethodMayBeStatic
# noinspection PyMethodOverriding
# noinspection PyMethodParameters
# noinspection PyMissingConstructor
# noinspection PyMissingOrEmptyDocstring
# noinspection PyNestedDecorators
# noinspection PynonAsciiChar
# noinspection PyNoneFunctionAssignment
# noinspection PyOldStyleClasses
# noinspection PyPackageRequirements
# noinspection PyPropertyAccess
# noinspection PyPropertyDefinition
# noinspection PyProtectedMember
# noinspection PyRaisingNewStyleClass
# noinspection PyRedeclaration
# noinspection PyRedundantParentheses
# noinspection PySetFunctionToLiteral
# noinspection PySimplifyBooleanCheck
# noinspection PySingleQuotedDocstring
# noinspection PyStatementEffect
# noinspection PyStringException
# noinspection PyStringFormat
# noinspection PySuperArguments
# noinspection PyTrailingSemicolon
# noinspection PyTupleAssignmentBalance
# noinspection PyTupleItemAssignment
# noinspection PyUnboundLocalVariable
# noinspection PyUnnecessaryBackslash
# noinspection PyUnreachableCode
# noinspection PyUnresolvedReferences
# noinspection PyUnusedLocal
# noinspection ReturnValueFromInit

import ctypes
import enum
import fractions
import inspect
import types
import typing

T = typing.TypeVar("T")
SingleAndSequence = typing.Union[T, typing.Sequence[T]]


###
# ENUMS AND CONSTANTS
class MediaType(enum.IntEnum):
    VIDEO: 'MediaType'
    AUDIO: 'MediaType'


VIDEO: MediaType
AUDIO: MediaType


class ColorFamily(enum.IntEnum):
    GRAY: 'ColorFamily'
    RGB: 'ColorFamily'
    YUV: 'ColorFamily'


GRAY: ColorFamily
RGB: ColorFamily
YUV: ColorFamily


class SampleType(enum.IntEnum):
    INTEGER: 'SampleType'
    FLOAT: 'SampleType'


INTEGER: SampleType
FLOAT: SampleType


class PresetFormat(enum.IntEnum):
    NONE: 'PresetFormat'

    GRAY8: 'PresetFormat'
    GRAY9: 'PresetFormat'
    GRAY10: 'PresetFormat'
    GRAY12: 'PresetFormat'
    GRAY14: 'PresetFormat'
    GRAY16: 'PresetFormat'
    GRAY32: 'PresetFormat'

    GRAYH: 'PresetFormat'
    GRAYS: 'PresetFormat'

    YUV420P8: 'PresetFormat'
    YUV422P8: 'PresetFormat'
    YUV444P8: 'PresetFormat'
    YUV410P8: 'PresetFormat'
    YUV411P8: 'PresetFormat'
    YUV440P8: 'PresetFormat'

    YUV420P9: 'PresetFormat'
    YUV422P9: 'PresetFormat'
    YUV444P9: 'PresetFormat'

    YUV420P10: 'PresetFormat'
    YUV422P10: 'PresetFormat'
    YUV444P10: 'PresetFormat'

    YUV420P12: 'PresetFormat'
    YUV422P12: 'PresetFormat'
    YUV444P12: 'PresetFormat'

    YUV420P14: 'PresetFormat'
    YUV422P14: 'PresetFormat'
    YUV444P14: 'PresetFormat'

    YUV420P16: 'PresetFormat'
    YUV422P16: 'PresetFormat'
    YUV444P16: 'PresetFormat'

    YUV444PH: 'PresetFormat'
    YUV444PS: 'PresetFormat'

    RGB24: 'PresetFormat'
    RGB27: 'PresetFormat'
    RGB30: 'PresetFormat'
    RGB36: 'PresetFormat'
    RGB42: 'PresetFormat'
    RGB48: 'PresetFormat'

    RGBH: 'PresetFormat'
    RGBS: 'PresetFormat'


NONE: PresetFormat

GRAY8: PresetFormat
GRAY9: PresetFormat
GRAY10: PresetFormat
GRAY12: PresetFormat
GRAY14: PresetFormat
GRAY16: PresetFormat
GRAY32: PresetFormat

GRAYH: PresetFormat
GRAYS: PresetFormat

YUV420P8: PresetFormat
YUV422P8: PresetFormat
YUV444P8: PresetFormat
YUV410P8: PresetFormat
YUV411P8: PresetFormat
YUV440P8: PresetFormat

YUV420P9: PresetFormat
YUV422P9: PresetFormat
YUV444P9: PresetFormat

YUV420P10: PresetFormat
YUV422P10: PresetFormat
YUV444P10: PresetFormat

YUV420P12: PresetFormat
YUV422P12: PresetFormat
YUV444P12: PresetFormat

YUV420P14: PresetFormat
YUV422P14: PresetFormat
YUV444P14: PresetFormat

YUV420P16: PresetFormat
YUV422P16: PresetFormat
YUV444P16: PresetFormat

YUV444PH: PresetFormat
YUV444PS: PresetFormat

RGB24: PresetFormat
RGB27: PresetFormat
RGB30: PresetFormat
RGB36: PresetFormat
RGB42: PresetFormat
RGB48: PresetFormat

RGBH: PresetFormat
RGBS: PresetFormat


class AudioChannels(enum.IntEnum):
    FRONT_LEFT: 'AudioChannels'
    FRONT_RIGHT: 'AudioChannels'
    FRONT_CENTER: 'AudioChannels'
    LOW_FREQUENCY: 'AudioChannels'
    BACK_LEFT: 'AudioChannels'
    BACK_RIGHT: 'AudioChannels'
    FRONT_LEFT_OF_CENTER: 'AudioChannels'
    FRONT_RIGHT_OF_CENTER: 'AudioChannels'
    BACK_CENTER: 'AudioChannels'
    SIDE_LEFT: 'AudioChannels'
    SIDE_RIGHT: 'AudioChannels'
    TOP_CENTER: 'AudioChannels'
    TOP_FRONT_LEFT: 'AudioChannels'
    TOP_FRONT_CENTER: 'AudioChannels'
    TOP_FRONT_RIGHT: 'AudioChannels'
    TOP_BACK_LEFT: 'AudioChannels'
    TOP_BACK_CENTER: 'AudioChannels'
    TOP_BACK_RIGHT: 'AudioChannels'
    STEREO_LEFT: 'AudioChannels'
    STEREO_RIGHT: 'AudioChannels'
    WIDE_LEFT: 'AudioChannels'
    WIDE_RIGHT: 'AudioChannels'
    SURROUND_DIRECT_LEFT: 'AudioChannels'
    SURROUND_DIRECT_RIGHT: 'AudioChannels'
    LOW_FREQUENCY2: 'AudioChannels'


FRONT_LEFT: AudioChannels
FRONT_RIGHT: AudioChannels
FRONT_CENTER: AudioChannels
LOW_FREQUENCY: AudioChannels
BACK_LEFT: AudioChannels
BACK_RIGHT: AudioChannels
FRONT_LEFT_OF_CENTER: AudioChannels
FRONT_RIGHT_OF_CENTER: AudioChannels
BACK_CENTER: AudioChannels
SIDE_LEFT: AudioChannels
SIDE_RIGHT: AudioChannels
TOP_CENTER: AudioChannels
TOP_FRONT_LEFT: AudioChannels
TOP_FRONT_CENTER: AudioChannels
TOP_FRONT_RIGHT: AudioChannels
TOP_BACK_LEFT: AudioChannels
TOP_BACK_CENTER: AudioChannels
TOP_BACK_RIGHT: AudioChannels
STEREO_LEFT: AudioChannels
STEREO_RIGHT: AudioChannels
WIDE_LEFT: AudioChannels
WIDE_RIGHT: AudioChannels
SURROUND_DIRECT_LEFT: AudioChannels
SURROUND_DIRECT_RIGHT: AudioChannels
LOW_FREQUENCY2: AudioChannels


class MessageType(enum.IntEnum):
    MESSAGE_TYPE_DEBUG: 'MessageType'
    MESSAGE_TYPE_INFORMATION: 'MessageType'
    MESSAGE_TYPE_WARNING: 'MessageType'
    MESSAGE_TYPE_CRITICAL: 'MessageType'
    MESSAGE_TYPE_FATAL: 'MessageType'


MESSAGE_TYPE_DEBUG: MessageType
MESSAGE_TYPE_INFORMATION: MessageType
MESSAGE_TYPE_WARNING: MessageType
MESSAGE_TYPE_CRITICAL: MessageType
MESSAGE_TYPE_FATAL: MessageType


class VapourSynthVersion(typing.NamedTuple):
    release_major: int
    release_minor: int


__version__: VapourSynthVersion


class VapourSynthAPIVersion(typing.NamedTuple):
    api_major: int
    api_minor: int


__api_version__: VapourSynthAPIVersion


class ColorRange(enum.IntEnum):
    RANGE_FULL: 'ColorRange'
    RANGE_LIMITED: 'ColorRange'


RANGE_FULL: ColorRange
RANGE_LIMITED: ColorRange


class ChromaLocation(enum.IntEnum):
    CHROMA_LEFT: 'ChromaLocation'
    CHROMA_CENTER: 'ChromaLocation'
    CHROMA_TOP_LEFT: 'ChromaLocation'
    CHROMA_TOP: 'ChromaLocation'
    CHROMA_BOTTOM_LEFT: 'ChromaLocation'
    CHROMA_BOTTOM: 'ChromaLocation'


CHROMA_LEFT: ChromaLocation
CHROMA_CENTER: ChromaLocation
CHROMA_TOP_LEFT: ChromaLocation
CHROMA_TOP: ChromaLocation
CHROMA_BOTTOM_LEFT: ChromaLocation
CHROMA_BOTTOM: ChromaLocation


class FieldBased(enum.IntEnum):
    FIELD_PROGRESSIVE: 'FieldBased'
    FIELD_TOP: 'FieldBased'
    FIELD_BOTTOM: 'FieldBased'


FIELD_PROGRESSIVE: FieldBased
FIELD_TOP: FieldBased
FIELD_BOTTOM: FieldBased


class MatrixCoefficients(enum.IntEnum):
    MATRIX_RGB: 'MatrixCoefficients'
    MATRIX_BT709: 'MatrixCoefficients'
    MATRIX_UNSPECIFIED: 'MatrixCoefficients'
    MATRIX_FCC: 'MatrixCoefficients'
    MATRIX_BT470_BG: 'MatrixCoefficients'
    MATRIX_ST170_M: 'MatrixCoefficients'
    MATRIX_YCGCO: 'MatrixCoefficients'
    MATRIX_BT2020_NCL: 'MatrixCoefficients'
    MATRIX_BT2020_CL: 'MatrixCoefficients'
    MATRIX_CHROMATICITY_DERIVED_NCL: 'MatrixCoefficients'
    MATRIX_CHROMATICITY_DERIVED_CL: 'MatrixCoefficients'
    MATRIX_ICTCP: 'MatrixCoefficients'


MATRIX_RGB: MatrixCoefficients
MATRIX_BT709: MatrixCoefficients
MATRIX_UNSPECIFIED: MatrixCoefficients
MATRIX_FCC: MatrixCoefficients
MATRIX_BT470_BG: MatrixCoefficients
MATRIX_ST170_M: MatrixCoefficients
MATRIX_YCGCO: MatrixCoefficients
MATRIX_BT2020_NCL: MatrixCoefficients
MATRIX_BT2020_CL: MatrixCoefficients
MATRIX_CHROMATICITY_DERIVED_NCL: MatrixCoefficients
MATRIX_CHROMATICITY_DERIVED_CL: MatrixCoefficients
MATRIX_ICTCP: MatrixCoefficients


class TransferCharacteristics(enum.IntEnum):
    TRANSFER_BT709: 'TransferCharacteristics'
    TRANSFER_UNSPECIFIED: 'TransferCharacteristics'
    TRANSFER_BT470_M: 'TransferCharacteristics'
    TRANSFER_BT470_BG: 'TransferCharacteristics'
    TRANSFER_BT601: 'TransferCharacteristics'
    TRANSFER_ST240_M: 'TransferCharacteristics'
    TRANSFER_LINEAR: 'TransferCharacteristics'
    TRANSFER_LOG_100: 'TransferCharacteristics'
    TRANSFER_LOG_316: 'TransferCharacteristics'
    TRANSFER_IEC_61966_2_4: 'TransferCharacteristics'
    TRANSFER_IEC_61966_2_1: 'TransferCharacteristics'
    TRANSFER_BT2020_10: 'TransferCharacteristics'
    TRANSFER_BT2020_12: 'TransferCharacteristics'
    TRANSFER_ST2084: 'TransferCharacteristics'
    TRANSFER_ARIB_B67: 'TransferCharacteristics'


TRANSFER_BT709: TransferCharacteristics
TRANSFER_UNSPECIFIED: TransferCharacteristics
TRANSFER_BT470_M: TransferCharacteristics
TRANSFER_BT470_BG: TransferCharacteristics
TRANSFER_BT601: TransferCharacteristics
TRANSFER_ST240_M: TransferCharacteristics
TRANSFER_LINEAR: TransferCharacteristics
TRANSFER_LOG_100: TransferCharacteristics
TRANSFER_LOG_316: TransferCharacteristics
TRANSFER_IEC_61966_2_4: TransferCharacteristics
TRANSFER_IEC_61966_2_1: TransferCharacteristics
TRANSFER_BT2020_10: TransferCharacteristics
TRANSFER_BT2020_12: TransferCharacteristics
TRANSFER_ST2084: TransferCharacteristics
TRANSFER_ARIB_B67: TransferCharacteristics


class ColorPrimaries(enum.IntEnum):
    PRIMARIES_BT709: 'ColorPrimaries'
    PRIMARIES_UNSPECIFIED: 'ColorPrimaries'
    PRIMARIES_BT470_M: 'ColorPrimaries'
    PRIMARIES_BT470_BG: 'ColorPrimaries'
    PRIMARIES_ST170_M: 'ColorPrimaries'
    PRIMARIES_ST240_M: 'ColorPrimaries'
    PRIMARIES_FILM: 'ColorPrimaries'
    PRIMARIES_BT2020: 'ColorPrimaries'
    PRIMARIES_ST428: 'ColorPrimaries'
    PRIMARIES_ST431_2: 'ColorPrimaries'
    PRIMARIES_ST432_1: 'ColorPrimaries'
    PRIMARIES_EBU3213_E: 'ColorPrimaries'


PRIMARIES_BT709: ColorPrimaries
PRIMARIES_UNSPECIFIED: ColorPrimaries
PRIMARIES_BT470_M: ColorPrimaries
PRIMARIES_BT470_BG: ColorPrimaries
PRIMARIES_ST170_M: ColorPrimaries
PRIMARIES_ST240_M: ColorPrimaries
PRIMARIES_FILM: ColorPrimaries
PRIMARIES_BT2020: ColorPrimaries
PRIMARIES_ST428: ColorPrimaries
PRIMARIES_ST431_2: ColorPrimaries
PRIMARIES_ST432_1: ColorPrimaries
PRIMARIES_EBU3213_E: ColorPrimaries


###
# VapourSynth Environment SubSystem
class EnvironmentData:
    """
    Contains the data VapourSynth stores for a specific environment.
    """


class Environment:
    @property
    def alive(self) -> bool: ...
    @property
    def single(self) -> bool: ...
    @property
    def env_id(self) -> int: ...
    @property
    def active(self) -> bool: ...
    @classmethod
    def is_single(cls) -> bool: ...
    def copy(self) -> Environment: ...
    def use(self) -> typing.ContextManager[None]: ...

    def __enter__(self) -> Environment: ...
    def __exit__(self, ty: typing.Optional[typing.Type[BaseException]], tv: typing.Optional[BaseException], tb: typing.Optional[types.TracebackType]) -> None: ...

class EnvironmentPolicyAPI:
    def wrap_environment(self, environment_data: EnvironmentData) -> Environment: ...
    def create_environment(self, flags: int = 0) -> EnvironmentData: ...
    def set_logger(self, env: Environment, logger: typing.Callable[[int, str], None]) -> None: ...
    def destroy_environment(self, env: EnvironmentData) -> None: ...
    def unregister_policy(self) -> None: ...

class EnvironmentPolicy:
    def on_policy_registered(self, special_api: EnvironmentPolicyAPI) -> None: ...
    def on_policy_cleared(self) -> None: ...
    def get_current_environment(self) -> typing.Optional[EnvironmentData]: ...
    def set_environment(self, environment: typing.Optional[EnvironmentData]) -> None: ...
    def is_active(self, environment: EnvironmentData) -> bool: ...


def register_policy(policy: EnvironmentPolicy) -> None: ...
def has_policy() -> bool: ...

# vpy_current_environment is deprecated
def vpy_current_environment() -> Environment: ...
def get_current_environment() -> Environment: ...

def construct_signature(signature: str, return_signature: str, injected: typing.Optional[str] = None) -> inspect.Signature: ...


class VideoOutputTuple(typing.NamedTuple):
    clip: 'VideoNode'
    alpha: typing.Optional['VideoNode']
    alt_output: int


class Error(Exception): ...

def set_message_handler(handler_func: typing.Callable[[int, str], None]) -> None: ...
def clear_output(index: int = 0) -> None: ...
def clear_outputs() -> None: ...
def get_outputs() -> types.MappingProxyType[int, typing.Union[VideoOutputTuple, 'AudioNode']]: ...
def get_output(index: int = 0) -> typing.Union[VideoOutputTuple, 'AudioNode']: ...


class VideoFormat:
    id: int
    name: str
    color_family: ColorFamily
    sample_type: SampleType
    bits_per_sample: int
    bytes_per_sample: int
    subsampling_w: int
    subsampling_h: int
    num_planes: int

    def __int__(self) -> int: ...

    def _as_dict(self) -> typing.Dict[str, typing.Any]: ...
    def replace(self, *,
                color_family: typing.Optional[ColorFamily] = None,
                sample_type: typing.Optional[SampleType] = None,
                bits_per_sample: typing.Optional[int] = None,
                subsampling_w: typing.Optional[int] = None,
                subsampling_h: typing.Optional[int] = None
                ) -> 'VideoFormat': ...


_FramePropsValue = typing.Union[
    SingleAndSequence[int],
    SingleAndSequence[float],
    SingleAndSequence[str],
    SingleAndSequence['VideoNode'],
    SingleAndSequence['VideoFrame'],
    SingleAndSequence['AudioNode'],
    SingleAndSequence['AudioFrame'],
    SingleAndSequence[typing.Callable[..., typing.Any]]
]

class FrameProps(typing.MutableMapping[str, _FramePropsValue]):

    def copy(self) -> typing.Dict[str, _FramePropsValue]: ...

    def __getattr__(self, name: str) -> _FramePropsValue: ...
    def __setattr__(self, name: str, value: _FramePropsValue) -> None: ...

    # mypy lo vult.
    # In all seriousness, why do I need to manually define them in a typestub?
    def __delitem__(self, name: str) -> None: ...
    def __setitem__(self, name: str, value: _FramePropsValue) -> None: ...
    def __getitem__(self, name: str) -> _FramePropsValue: ...
    def __iter__(self) -> typing.Iterator[str]: ...
    def __len__(self) -> int: ...


class _RawFrame:
    @property
    def readonly(self) -> bool: ...

    @property
    def props(self) -> FrameProps: ...

    def get_read_ptr(self, plane: int) -> ctypes.c_void_p: ...
    def get_write_ptr(self, plane: int) -> ctypes.c_void_p: ...
    def get_stride(self, plane: int) -> int: ...

    @property
    def closed(self) -> bool: ...

    def close(self) -> None: ...
    def __enter__(self) -> '_RawFrame': ...
    def __exit__(self, ty: typing.Optional[typing.Type[BaseException]], tv: typing.Optional[BaseException], tb: typing.Optional[types.TracebackType]) -> None: ...


class VideoFrame(_RawFrame):
    height: int
    width: int
    format: VideoFormat

    def copy(self) -> 'VideoFrame': ...
    def _writelines(self, write: typing.Callable[[bytes], int]) -> None: ...

    def __getitem__(self, index: int) -> memoryview: ...
    def __len__(self) -> int: ...
    def __enter__(self) -> 'VideoFrame': ...


class _Future(typing.Generic[T]):
    def set_result(self, value: T) -> None: ...
    def set_exception(self, exception: BaseException) -> None: ...
    def result(self) -> T: ...
    def exception(self) -> typing.Optional[typing.NoReturn]: ...


Func = typing.Callable[..., typing.Any]


class Plugin:
    identifier: str
    namespace: str
    name: str

    def functions(self) -> typing.Iterator[Function]: ...

    # get_functions is deprecated
    def get_functions(self) -> typing.Dict[str, str]: ...
    # list_functions is deprecated
    def list_functions(self) -> str: ...


class Function:
    plugin: Plugin
    name: str
    signature: str
    return_signature: str

    @property
    def __signature__(self) -> inspect.Signature: ...
    def __call__(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Any: ...


# implementation: bas

class _Plugin_bas_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Source(self, source: typing.Union[str, bytes, bytearray], track: typing.Optional[int] = None, adjustdelay: typing.Optional[int] = None, exactsamples: typing.Optional[int] = None, enable_drefs: typing.Optional[int] = None, use_absolute_path: typing.Optional[int] = None, drc_scale: typing.Optional[float] = None) -> "AudioNode": ...

# end implementation


# implementation: ffms2

class _Plugin_ffms2_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def GetLogLevel(self) -> int: ...
    def Index(self, source: typing.Union[str, bytes, bytearray], cachefile: typing.Union[str, bytes, bytearray, None] = None, indextracks: typing.Union[int, typing.Sequence[int], None] = None, errorhandling: typing.Optional[int] = None, overwrite: typing.Optional[int] = None) -> typing.Union[str, bytes, bytearray]: ...
    def SetLogLevel(self, level: int) -> int: ...
    def Source(self, source: typing.Union[str, bytes, bytearray], track: typing.Optional[int] = None, cache: typing.Optional[int] = None, cachefile: typing.Union[str, bytes, bytearray, None] = None, fpsnum: typing.Optional[int] = None, fpsden: typing.Optional[int] = None, threads: typing.Optional[int] = None, timecodes: typing.Union[str, bytes, bytearray, None] = None, seekmode: typing.Optional[int] = None, width: typing.Optional[int] = None, height: typing.Optional[int] = None, resizer: typing.Union[str, bytes, bytearray, None] = None, format: typing.Optional[int] = None, alpha: typing.Optional[int] = None) -> "VideoNode": ...
    def Version(self) -> typing.Union[str, bytes, bytearray]: ...

# end implementation


# implementation: imwri

class _Plugin_imwri_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Read(self, filename: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]]], firstnum: typing.Optional[int] = None, mismatch: typing.Optional[int] = None, alpha: typing.Optional[int] = None, float_output: typing.Optional[int] = None, embed_icc: typing.Optional[int] = None) -> "VideoNode": ...
    def Write(self, clip: "VideoNode", imgformat: typing.Union[str, bytes, bytearray], filename: typing.Union[str, bytes, bytearray], firstnum: typing.Optional[int] = None, quality: typing.Optional[int] = None, dither: typing.Optional[int] = None, compression_type: typing.Union[str, bytes, bytearray, None] = None, overwrite: typing.Optional[int] = None, alpha: typing.Optional["VideoNode"] = None) -> "VideoNode": ...


class _Plugin_imwri_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Write(self, imgformat: typing.Union[str, bytes, bytearray], filename: typing.Union[str, bytes, bytearray], firstnum: typing.Optional[int] = None, quality: typing.Optional[int] = None, dither: typing.Optional[int] = None, compression_type: typing.Union[str, bytes, bytearray, None] = None, overwrite: typing.Optional[int] = None, alpha: typing.Optional["VideoNode"] = None) -> "VideoNode": ...

# end implementation


# implementation: lsmas

class _Plugin_lsmas_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def LWLibavSource(self, source: typing.Union[str, bytes, bytearray], stream_index: typing.Optional[int] = None, cache: typing.Optional[int] = None, cachefile: typing.Union[str, bytes, bytearray, None] = None, threads: typing.Optional[int] = None, seek_mode: typing.Optional[int] = None, seek_threshold: typing.Optional[int] = None, dr: typing.Optional[int] = None, fpsnum: typing.Optional[int] = None, fpsden: typing.Optional[int] = None, variable: typing.Optional[int] = None, format: typing.Union[str, bytes, bytearray, None] = None, decoder: typing.Union[str, bytes, bytearray, None] = None, prefer_hw: typing.Optional[int] = None, repeat: typing.Optional[int] = None, dominance: typing.Optional[int] = None, ff_loglevel: typing.Optional[int] = None) -> "VideoNode": ...
    def LibavSMASHSource(self, source: typing.Union[str, bytes, bytearray], track: typing.Optional[int] = None, threads: typing.Optional[int] = None, seek_mode: typing.Optional[int] = None, seek_threshold: typing.Optional[int] = None, dr: typing.Optional[int] = None, fpsnum: typing.Optional[int] = None, fpsden: typing.Optional[int] = None, variable: typing.Optional[int] = None, format: typing.Union[str, bytes, bytearray, None] = None, decoder: typing.Union[str, bytes, bytearray, None] = None, prefer_hw: typing.Optional[int] = None, ff_loglevel: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: mv

class _Plugin_mv_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Analyse(self, super: "VideoNode", blksize: typing.Optional[int] = None, blksizev: typing.Optional[int] = None, levels: typing.Optional[int] = None, search: typing.Optional[int] = None, searchparam: typing.Optional[int] = None, pelsearch: typing.Optional[int] = None, isb: typing.Optional[int] = None, lambda_: typing.Optional[int] = None, chroma: typing.Optional[int] = None, delta: typing.Optional[int] = None, truemotion: typing.Optional[int] = None, lsad: typing.Optional[int] = None, plevel: typing.Optional[int] = None, global_: typing.Optional[int] = None, pnew: typing.Optional[int] = None, pzero: typing.Optional[int] = None, pglobal: typing.Optional[int] = None, overlap: typing.Optional[int] = None, overlapv: typing.Optional[int] = None, divide: typing.Optional[int] = None, badsad: typing.Optional[int] = None, badrange: typing.Optional[int] = None, opt: typing.Optional[int] = None, meander: typing.Optional[int] = None, trymany: typing.Optional[int] = None, fields: typing.Optional[int] = None, tff: typing.Optional[int] = None, search_coarse: typing.Optional[int] = None, dct: typing.Optional[int] = None) -> "VideoNode": ...
    def BlockFPS(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", num: typing.Optional[int] = None, den: typing.Optional[int] = None, mode: typing.Optional[int] = None, ml: typing.Optional[float] = None, blend: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Compensate(self, clip: "VideoNode", super: "VideoNode", vectors: "VideoNode", scbehavior: typing.Optional[int] = None, thsad: typing.Optional[int] = None, fields: typing.Optional[int] = None, time: typing.Optional[float] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None, tff: typing.Optional[int] = None) -> "VideoNode": ...
    def Degrain1(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", thsad: typing.Optional[int] = None, thsadc: typing.Optional[int] = None, plane: typing.Optional[int] = None, limit: typing.Optional[int] = None, limitc: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Degrain2(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", thsad: typing.Optional[int] = None, thsadc: typing.Optional[int] = None, plane: typing.Optional[int] = None, limit: typing.Optional[int] = None, limitc: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Degrain3(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", thsad: typing.Optional[int] = None, thsadc: typing.Optional[int] = None, plane: typing.Optional[int] = None, limit: typing.Optional[int] = None, limitc: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def DepanAnalyse(self, clip: "VideoNode", vectors: "VideoNode", mask: typing.Optional["VideoNode"] = None, zoom: typing.Optional[int] = None, rot: typing.Optional[int] = None, pixaspect: typing.Optional[float] = None, error: typing.Optional[float] = None, info: typing.Optional[int] = None, wrong: typing.Optional[float] = None, zerow: typing.Optional[float] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, fields: typing.Optional[int] = None, tff: typing.Optional[int] = None) -> "VideoNode": ...
    def DepanCompensate(self, clip: "VideoNode", data: "VideoNode", offset: typing.Optional[float] = None, subpixel: typing.Optional[int] = None, pixaspect: typing.Optional[float] = None, matchfields: typing.Optional[int] = None, mirror: typing.Optional[int] = None, blur: typing.Optional[int] = None, info: typing.Optional[int] = None, fields: typing.Optional[int] = None, tff: typing.Optional[int] = None) -> "VideoNode": ...
    def DepanEstimate(self, clip: "VideoNode", trust: typing.Optional[float] = None, winx: typing.Optional[int] = None, winy: typing.Optional[int] = None, wleft: typing.Optional[int] = None, wtop: typing.Optional[int] = None, dxmax: typing.Optional[int] = None, dymax: typing.Optional[int] = None, zoommax: typing.Optional[float] = None, stab: typing.Optional[float] = None, pixaspect: typing.Optional[float] = None, info: typing.Optional[int] = None, show: typing.Optional[int] = None, fields: typing.Optional[int] = None, tff: typing.Optional[int] = None) -> "VideoNode": ...
    def DepanStabilise(self, clip: "VideoNode", data: "VideoNode", cutoff: typing.Optional[float] = None, damping: typing.Optional[float] = None, initzoom: typing.Optional[float] = None, addzoom: typing.Optional[int] = None, prev: typing.Optional[int] = None, next: typing.Optional[int] = None, mirror: typing.Optional[int] = None, blur: typing.Optional[int] = None, dxmax: typing.Optional[float] = None, dymax: typing.Optional[float] = None, zoommax: typing.Optional[float] = None, rotmax: typing.Optional[float] = None, subpixel: typing.Optional[int] = None, pixaspect: typing.Optional[float] = None, fitlast: typing.Optional[int] = None, tzoom: typing.Optional[float] = None, info: typing.Optional[int] = None, method: typing.Optional[int] = None, fields: typing.Optional[int] = None) -> "VideoNode": ...
    def Finest(self, super: "VideoNode", opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Flow(self, clip: "VideoNode", super: "VideoNode", vectors: "VideoNode", time: typing.Optional[float] = None, mode: typing.Optional[int] = None, fields: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None, tff: typing.Optional[int] = None) -> "VideoNode": ...
    def FlowBlur(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", blur: typing.Optional[float] = None, prec: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def FlowFPS(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", num: typing.Optional[int] = None, den: typing.Optional[int] = None, mask: typing.Optional[int] = None, ml: typing.Optional[float] = None, blend: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def FlowInter(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", time: typing.Optional[float] = None, ml: typing.Optional[float] = None, blend: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Mask(self, clip: "VideoNode", vectors: "VideoNode", ml: typing.Optional[float] = None, gamma: typing.Optional[float] = None, kind: typing.Optional[int] = None, time: typing.Optional[float] = None, ysc: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Recalculate(self, super: "VideoNode", vectors: "VideoNode", thsad: typing.Optional[int] = None, smooth: typing.Optional[int] = None, blksize: typing.Optional[int] = None, blksizev: typing.Optional[int] = None, search: typing.Optional[int] = None, searchparam: typing.Optional[int] = None, lambda_: typing.Optional[int] = None, chroma: typing.Optional[int] = None, truemotion: typing.Optional[int] = None, pnew: typing.Optional[int] = None, overlap: typing.Optional[int] = None, overlapv: typing.Optional[int] = None, divide: typing.Optional[int] = None, opt: typing.Optional[int] = None, meander: typing.Optional[int] = None, fields: typing.Optional[int] = None, tff: typing.Optional[int] = None, dct: typing.Optional[int] = None) -> "VideoNode": ...
    def SCDetection(self, clip: "VideoNode", vectors: "VideoNode", thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None) -> "VideoNode": ...
    def Super(self, clip: "VideoNode", hpad: typing.Optional[int] = None, vpad: typing.Optional[int] = None, pel: typing.Optional[int] = None, levels: typing.Optional[int] = None, chroma: typing.Optional[int] = None, sharp: typing.Optional[int] = None, rfilter: typing.Optional[int] = None, pelclip: typing.Optional["VideoNode"] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_mv_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Analyse(self, blksize: typing.Optional[int] = None, blksizev: typing.Optional[int] = None, levels: typing.Optional[int] = None, search: typing.Optional[int] = None, searchparam: typing.Optional[int] = None, pelsearch: typing.Optional[int] = None, isb: typing.Optional[int] = None, lambda_: typing.Optional[int] = None, chroma: typing.Optional[int] = None, delta: typing.Optional[int] = None, truemotion: typing.Optional[int] = None, lsad: typing.Optional[int] = None, plevel: typing.Optional[int] = None, global_: typing.Optional[int] = None, pnew: typing.Optional[int] = None, pzero: typing.Optional[int] = None, pglobal: typing.Optional[int] = None, overlap: typing.Optional[int] = None, overlapv: typing.Optional[int] = None, divide: typing.Optional[int] = None, badsad: typing.Optional[int] = None, badrange: typing.Optional[int] = None, opt: typing.Optional[int] = None, meander: typing.Optional[int] = None, trymany: typing.Optional[int] = None, fields: typing.Optional[int] = None, tff: typing.Optional[int] = None, search_coarse: typing.Optional[int] = None, dct: typing.Optional[int] = None) -> "VideoNode": ...
    def BlockFPS(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", num: typing.Optional[int] = None, den: typing.Optional[int] = None, mode: typing.Optional[int] = None, ml: typing.Optional[float] = None, blend: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Compensate(self, super: "VideoNode", vectors: "VideoNode", scbehavior: typing.Optional[int] = None, thsad: typing.Optional[int] = None, fields: typing.Optional[int] = None, time: typing.Optional[float] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None, tff: typing.Optional[int] = None) -> "VideoNode": ...
    def Degrain1(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", thsad: typing.Optional[int] = None, thsadc: typing.Optional[int] = None, plane: typing.Optional[int] = None, limit: typing.Optional[int] = None, limitc: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Degrain2(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", thsad: typing.Optional[int] = None, thsadc: typing.Optional[int] = None, plane: typing.Optional[int] = None, limit: typing.Optional[int] = None, limitc: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Degrain3(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", thsad: typing.Optional[int] = None, thsadc: typing.Optional[int] = None, plane: typing.Optional[int] = None, limit: typing.Optional[int] = None, limitc: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def DepanAnalyse(self, vectors: "VideoNode", mask: typing.Optional["VideoNode"] = None, zoom: typing.Optional[int] = None, rot: typing.Optional[int] = None, pixaspect: typing.Optional[float] = None, error: typing.Optional[float] = None, info: typing.Optional[int] = None, wrong: typing.Optional[float] = None, zerow: typing.Optional[float] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, fields: typing.Optional[int] = None, tff: typing.Optional[int] = None) -> "VideoNode": ...
    def DepanCompensate(self, data: "VideoNode", offset: typing.Optional[float] = None, subpixel: typing.Optional[int] = None, pixaspect: typing.Optional[float] = None, matchfields: typing.Optional[int] = None, mirror: typing.Optional[int] = None, blur: typing.Optional[int] = None, info: typing.Optional[int] = None, fields: typing.Optional[int] = None, tff: typing.Optional[int] = None) -> "VideoNode": ...
    def DepanEstimate(self, trust: typing.Optional[float] = None, winx: typing.Optional[int] = None, winy: typing.Optional[int] = None, wleft: typing.Optional[int] = None, wtop: typing.Optional[int] = None, dxmax: typing.Optional[int] = None, dymax: typing.Optional[int] = None, zoommax: typing.Optional[float] = None, stab: typing.Optional[float] = None, pixaspect: typing.Optional[float] = None, info: typing.Optional[int] = None, show: typing.Optional[int] = None, fields: typing.Optional[int] = None, tff: typing.Optional[int] = None) -> "VideoNode": ...
    def DepanStabilise(self, data: "VideoNode", cutoff: typing.Optional[float] = None, damping: typing.Optional[float] = None, initzoom: typing.Optional[float] = None, addzoom: typing.Optional[int] = None, prev: typing.Optional[int] = None, next: typing.Optional[int] = None, mirror: typing.Optional[int] = None, blur: typing.Optional[int] = None, dxmax: typing.Optional[float] = None, dymax: typing.Optional[float] = None, zoommax: typing.Optional[float] = None, rotmax: typing.Optional[float] = None, subpixel: typing.Optional[int] = None, pixaspect: typing.Optional[float] = None, fitlast: typing.Optional[int] = None, tzoom: typing.Optional[float] = None, info: typing.Optional[int] = None, method: typing.Optional[int] = None, fields: typing.Optional[int] = None) -> "VideoNode": ...
    def Finest(self, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Flow(self, super: "VideoNode", vectors: "VideoNode", time: typing.Optional[float] = None, mode: typing.Optional[int] = None, fields: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None, tff: typing.Optional[int] = None) -> "VideoNode": ...
    def FlowBlur(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", blur: typing.Optional[float] = None, prec: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def FlowFPS(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", num: typing.Optional[int] = None, den: typing.Optional[int] = None, mask: typing.Optional[int] = None, ml: typing.Optional[float] = None, blend: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def FlowInter(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", time: typing.Optional[float] = None, ml: typing.Optional[float] = None, blend: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Mask(self, vectors: "VideoNode", ml: typing.Optional[float] = None, gamma: typing.Optional[float] = None, kind: typing.Optional[int] = None, time: typing.Optional[float] = None, ysc: typing.Optional[int] = None, thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...
    def Recalculate(self, vectors: "VideoNode", thsad: typing.Optional[int] = None, smooth: typing.Optional[int] = None, blksize: typing.Optional[int] = None, blksizev: typing.Optional[int] = None, search: typing.Optional[int] = None, searchparam: typing.Optional[int] = None, lambda_: typing.Optional[int] = None, chroma: typing.Optional[int] = None, truemotion: typing.Optional[int] = None, pnew: typing.Optional[int] = None, overlap: typing.Optional[int] = None, overlapv: typing.Optional[int] = None, divide: typing.Optional[int] = None, opt: typing.Optional[int] = None, meander: typing.Optional[int] = None, fields: typing.Optional[int] = None, tff: typing.Optional[int] = None, dct: typing.Optional[int] = None) -> "VideoNode": ...
    def SCDetection(self, vectors: "VideoNode", thscd1: typing.Optional[int] = None, thscd2: typing.Optional[int] = None) -> "VideoNode": ...
    def Super(self, hpad: typing.Optional[int] = None, vpad: typing.Optional[int] = None, pel: typing.Optional[int] = None, levels: typing.Optional[int] = None, chroma: typing.Optional[int] = None, sharp: typing.Optional[int] = None, rfilter: typing.Optional[int] = None, pelclip: typing.Optional["VideoNode"] = None, opt: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: resize

class _Plugin_resize_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Bicubic(self, clip: "VideoNode", width: typing.Optional[int] = None, height: typing.Optional[int] = None, format: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Optional[int] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Optional[int] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Optional[int] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Optional[int] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Optional[int] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Optional[int] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, nominal_luminance: typing.Optional[float] = None) -> "VideoNode": ...
    def Bilinear(self, clip: "VideoNode", width: typing.Optional[int] = None, height: typing.Optional[int] = None, format: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Optional[int] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Optional[int] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Optional[int] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Optional[int] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Optional[int] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Optional[int] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, nominal_luminance: typing.Optional[float] = None) -> "VideoNode": ...
    def Bob(self, clip: "VideoNode", filter: typing.Union[str, bytes, bytearray, None] = None, tff: typing.Optional[int] = None, format: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Optional[int] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Optional[int] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Optional[int] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Optional[int] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Optional[int] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Optional[int] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, nominal_luminance: typing.Optional[float] = None) -> "VideoNode": ...
    def Lanczos(self, clip: "VideoNode", width: typing.Optional[int] = None, height: typing.Optional[int] = None, format: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Optional[int] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Optional[int] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Optional[int] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Optional[int] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Optional[int] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Optional[int] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, nominal_luminance: typing.Optional[float] = None) -> "VideoNode": ...
    def Point(self, clip: "VideoNode", width: typing.Optional[int] = None, height: typing.Optional[int] = None, format: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Optional[int] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Optional[int] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Optional[int] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Optional[int] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Optional[int] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Optional[int] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, nominal_luminance: typing.Optional[float] = None) -> "VideoNode": ...
    def Spline16(self, clip: "VideoNode", width: typing.Optional[int] = None, height: typing.Optional[int] = None, format: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Optional[int] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Optional[int] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Optional[int] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Optional[int] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Optional[int] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Optional[int] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, nominal_luminance: typing.Optional[float] = None) -> "VideoNode": ...
    def Spline36(self, clip: "VideoNode", width: typing.Optional[int] = None, height: typing.Optional[int] = None, format: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Optional[int] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Optional[int] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Optional[int] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Optional[int] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Optional[int] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Optional[int] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, nominal_luminance: typing.Optional[float] = None) -> "VideoNode": ...
    def Spline64(self, clip: "VideoNode", width: typing.Optional[int] = None, height: typing.Optional[int] = None, format: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Optional[int] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Optional[int] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Optional[int] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Optional[int] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Optional[int] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Optional[int] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, nominal_luminance: typing.Optional[float] = None) -> "VideoNode": ...


class _Plugin_resize_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Bicubic(self, width: typing.Optional[int] = None, height: typing.Optional[int] = None, format: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Optional[int] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Optional[int] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Optional[int] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Optional[int] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Optional[int] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Optional[int] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, nominal_luminance: typing.Optional[float] = None) -> "VideoNode": ...
    def Bilinear(self, width: typing.Optional[int] = None, height: typing.Optional[int] = None, format: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Optional[int] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Optional[int] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Optional[int] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Optional[int] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Optional[int] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Optional[int] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, nominal_luminance: typing.Optional[float] = None) -> "VideoNode": ...
    def Bob(self, filter: typing.Union[str, bytes, bytearray, None] = None, tff: typing.Optional[int] = None, format: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Optional[int] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Optional[int] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Optional[int] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Optional[int] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Optional[int] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Optional[int] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, nominal_luminance: typing.Optional[float] = None) -> "VideoNode": ...
    def Lanczos(self, width: typing.Optional[int] = None, height: typing.Optional[int] = None, format: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Optional[int] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Optional[int] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Optional[int] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Optional[int] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Optional[int] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Optional[int] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, nominal_luminance: typing.Optional[float] = None) -> "VideoNode": ...
    def Point(self, width: typing.Optional[int] = None, height: typing.Optional[int] = None, format: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Optional[int] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Optional[int] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Optional[int] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Optional[int] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Optional[int] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Optional[int] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, nominal_luminance: typing.Optional[float] = None) -> "VideoNode": ...
    def Spline16(self, width: typing.Optional[int] = None, height: typing.Optional[int] = None, format: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Optional[int] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Optional[int] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Optional[int] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Optional[int] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Optional[int] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Optional[int] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, nominal_luminance: typing.Optional[float] = None) -> "VideoNode": ...
    def Spline36(self, width: typing.Optional[int] = None, height: typing.Optional[int] = None, format: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Optional[int] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Optional[int] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Optional[int] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Optional[int] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Optional[int] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Optional[int] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, nominal_luminance: typing.Optional[float] = None) -> "VideoNode": ...
    def Spline64(self, width: typing.Optional[int] = None, height: typing.Optional[int] = None, format: typing.Optional[int] = None, matrix: typing.Optional[int] = None, matrix_s: typing.Union[str, bytes, bytearray, None] = None, transfer: typing.Optional[int] = None, transfer_s: typing.Union[str, bytes, bytearray, None] = None, primaries: typing.Optional[int] = None, primaries_s: typing.Union[str, bytes, bytearray, None] = None, range: typing.Optional[int] = None, range_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc: typing.Optional[int] = None, chromaloc_s: typing.Union[str, bytes, bytearray, None] = None, matrix_in: typing.Optional[int] = None, matrix_in_s: typing.Union[str, bytes, bytearray, None] = None, transfer_in: typing.Optional[int] = None, transfer_in_s: typing.Union[str, bytes, bytearray, None] = None, primaries_in: typing.Optional[int] = None, primaries_in_s: typing.Union[str, bytes, bytearray, None] = None, range_in: typing.Optional[int] = None, range_in_s: typing.Union[str, bytes, bytearray, None] = None, chromaloc_in: typing.Optional[int] = None, chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = None, filter_param_a: typing.Optional[float] = None, filter_param_b: typing.Optional[float] = None, resample_filter_uv: typing.Union[str, bytes, bytearray, None] = None, filter_param_a_uv: typing.Optional[float] = None, filter_param_b_uv: typing.Optional[float] = None, dither_type: typing.Union[str, bytes, bytearray, None] = None, cpu_type: typing.Union[str, bytes, bytearray, None] = None, prefer_props: typing.Optional[int] = None, src_left: typing.Optional[float] = None, src_top: typing.Optional[float] = None, src_width: typing.Optional[float] = None, src_height: typing.Optional[float] = None, nominal_luminance: typing.Optional[float] = None) -> "VideoNode": ...

# end implementation


# implementation: scxvid

class _Plugin_scxvid_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Scxvid(self, clip: "VideoNode", log: typing.Union[str, bytes, bytearray, None] = None, use_slices: typing.Optional[int] = None) -> "VideoNode": ...


class _Plugin_scxvid_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Scxvid(self, log: typing.Union[str, bytes, bytearray, None] = None, use_slices: typing.Optional[int] = None) -> "VideoNode": ...

# end implementation


# implementation: std

class _Plugin_std_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def AddBorders(self, clip: "VideoNode", left: typing.Optional[int] = None, right: typing.Optional[int] = None, top: typing.Optional[int] = None, bottom: typing.Optional[int] = None, color: typing.Union[float, typing.Sequence[float], None] = None) -> "VideoNode": ...
    def AssumeFPS(self, clip: "VideoNode", src: typing.Optional["VideoNode"] = None, fpsnum: typing.Optional[int] = None, fpsden: typing.Optional[int] = None) -> "VideoNode": ...
    def AssumeSampleRate(self, clip: "AudioNode", src: typing.Optional["AudioNode"] = None, samplerate: typing.Optional[int] = None) -> "AudioNode": ...
    def AudioGain(self, clip: "AudioNode", gain: typing.Union[float, typing.Sequence[float], None] = None) -> "AudioNode": ...
    def AudioLoop(self, clip: "AudioNode", times: typing.Optional[int] = None) -> "AudioNode": ...
    def AudioMix(self, clips: typing.Union["AudioNode", typing.Sequence["AudioNode"]], matrix: typing.Union[float, typing.Sequence[float]], channels_out: typing.Union[int, typing.Sequence[int]]) -> "AudioNode": ...
    def AudioReverse(self, clip: "AudioNode") -> "AudioNode": ...
    def AudioSplice(self, clips: typing.Union["AudioNode", typing.Sequence["AudioNode"]]) -> "AudioNode": ...
    def AudioTrim(self, clip: "AudioNode", first: typing.Optional[int] = None, last: typing.Optional[int] = None, length: typing.Optional[int] = None) -> "AudioNode": ...
    def AverageFrames(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]], weights: typing.Union[float, typing.Sequence[float]], scale: typing.Optional[float] = None, scenechange: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Binarize(self, clip: "VideoNode", threshold: typing.Union[float, typing.Sequence[float], None] = None, v0: typing.Union[float, typing.Sequence[float], None] = None, v1: typing.Union[float, typing.Sequence[float], None] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def BinarizeMask(self, clip: "VideoNode", threshold: typing.Union[float, typing.Sequence[float], None] = None, v0: typing.Union[float, typing.Sequence[float], None] = None, v1: typing.Union[float, typing.Sequence[float], None] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def BlankAudio(self, clip: typing.Optional["AudioNode"] = None, channels: typing.Union[int, typing.Sequence[int], None] = None, bits: typing.Optional[int] = None, sampletype: typing.Optional[int] = None, samplerate: typing.Optional[int] = None, length: typing.Optional[int] = None, keep: typing.Optional[int] = None) -> "AudioNode": ...
    def BlankClip(self, clip: typing.Optional["VideoNode"] = None, width: typing.Optional[int] = None, height: typing.Optional[int] = None, format: typing.Optional[int] = None, length: typing.Optional[int] = None, fpsnum: typing.Optional[int] = None, fpsden: typing.Optional[int] = None, color: typing.Union[float, typing.Sequence[float], None] = None, keep: typing.Optional[int] = None) -> "VideoNode": ...
    def BoxBlur(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None, hradius: typing.Optional[int] = None, hpasses: typing.Optional[int] = None, vradius: typing.Optional[int] = None, vpasses: typing.Optional[int] = None) -> "VideoNode": ...
    def Cache(self, clip: "VideoNode", size: typing.Optional[int] = None, fixed: typing.Optional[int] = None, make_linear: typing.Optional[int] = None) -> "VideoNode": ...
    def ClipToProp(self, clip: "VideoNode", mclip: "VideoNode", prop: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def Convolution(self, clip: "VideoNode", matrix: typing.Union[float, typing.Sequence[float]], bias: typing.Optional[float] = None, divisor: typing.Optional[float] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, saturate: typing.Optional[int] = None, mode: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def CopyFrameProps(self, clip: "VideoNode", prop_src: "VideoNode") -> "VideoNode": ...
    def Crop(self, clip: "VideoNode", left: typing.Optional[int] = None, right: typing.Optional[int] = None, top: typing.Optional[int] = None, bottom: typing.Optional[int] = None) -> "VideoNode": ...
    def CropAbs(self, clip: "VideoNode", width: int, height: int, left: typing.Optional[int] = None, top: typing.Optional[int] = None, x: typing.Optional[int] = None, y: typing.Optional[int] = None) -> "VideoNode": ...
    def CropRel(self, clip: "VideoNode", left: typing.Optional[int] = None, right: typing.Optional[int] = None, top: typing.Optional[int] = None, bottom: typing.Optional[int] = None) -> "VideoNode": ...
    def Deflate(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None, threshold: typing.Optional[float] = None) -> "VideoNode": ...
    def DeleteFrames(self, clip: "VideoNode", frames: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def DoubleWeave(self, clip: "VideoNode", tff: typing.Optional[int] = None) -> "VideoNode": ...
    def DuplicateFrames(self, clip: "VideoNode", frames: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def Expr(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]], expr: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]]], format: typing.Optional[int] = None) -> "VideoNode": ...
    def FlipHorizontal(self, clip: "VideoNode") -> "VideoNode": ...
    def FlipVertical(self, clip: "VideoNode") -> "VideoNode": ...
    def FrameEval(self, clip: "VideoNode", eval: typing.Callable[..., typing.Any], prop_src: typing.Union["VideoNode", typing.Sequence["VideoNode"], None] = None, clip_src: typing.Union["VideoNode", typing.Sequence["VideoNode"], None] = None) -> "VideoNode": ...
    def FreezeFrames(self, clip: "VideoNode", first: typing.Union[int, typing.Sequence[int], None] = None, last: typing.Union[int, typing.Sequence[int], None] = None, replacement: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Inflate(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None, threshold: typing.Optional[float] = None) -> "VideoNode": ...
    def Interleave(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]], extend: typing.Optional[int] = None, mismatch: typing.Optional[int] = None, modify_duration: typing.Optional[int] = None) -> "VideoNode": ...
    def Invert(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def InvertMask(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Levels(self, clip: "VideoNode", min_in: typing.Union[float, typing.Sequence[float], None] = None, max_in: typing.Union[float, typing.Sequence[float], None] = None, gamma: typing.Union[float, typing.Sequence[float], None] = None, min_out: typing.Union[float, typing.Sequence[float], None] = None, max_out: typing.Union[float, typing.Sequence[float], None] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Limiter(self, clip: "VideoNode", min: typing.Union[float, typing.Sequence[float], None] = None, max: typing.Union[float, typing.Sequence[float], None] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def LoadAllPlugins(self, path: typing.Union[str, bytes, bytearray]) -> None: ...
    def LoadPlugin(self, path: typing.Union[str, bytes, bytearray], altsearchpath: typing.Optional[int] = None, forcens: typing.Union[str, bytes, bytearray, None] = None, forceid: typing.Union[str, bytes, bytearray, None] = None) -> None: ...
    def Loop(self, clip: "VideoNode", times: typing.Optional[int] = None) -> "VideoNode": ...
    def Lut(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None, lut: typing.Union[int, typing.Sequence[int], None] = None, lutf: typing.Union[float, typing.Sequence[float], None] = None, function: typing.Optional[typing.Callable[..., typing.Any]] = None, bits: typing.Optional[int] = None, floatout: typing.Optional[int] = None) -> "VideoNode": ...
    def Lut2(self, clipa: "VideoNode", clipb: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None, lut: typing.Union[int, typing.Sequence[int], None] = None, lutf: typing.Union[float, typing.Sequence[float], None] = None, function: typing.Optional[typing.Callable[..., typing.Any]] = None, bits: typing.Optional[int] = None, floatout: typing.Optional[int] = None) -> "VideoNode": ...
    def MakeDiff(self, clipa: "VideoNode", clipb: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def MakeFullDiff(self, clipa: "VideoNode", clipb: "VideoNode") -> "VideoNode": ...
    def MaskedMerge(self, clipa: "VideoNode", clipb: "VideoNode", mask: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None, first_plane: typing.Optional[int] = None, premultiplied: typing.Optional[int] = None) -> "VideoNode": ...
    def Maximum(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None, threshold: typing.Optional[float] = None, coordinates: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Median(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Merge(self, clipa: "VideoNode", clipb: "VideoNode", weight: typing.Union[float, typing.Sequence[float], None] = None) -> "VideoNode": ...
    def MergeDiff(self, clipa: "VideoNode", clipb: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def MergeFullDiff(self, clipa: "VideoNode", clipb: "VideoNode") -> "VideoNode": ...
    def Minimum(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None, threshold: typing.Optional[float] = None, coordinates: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def ModifyFrame(self, clip: "VideoNode", clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]], selector: typing.Callable[..., typing.Any]) -> "VideoNode": ...
    def PEMVerifier(self, clip: "VideoNode", upper: typing.Union[float, typing.Sequence[float], None] = None, lower: typing.Union[float, typing.Sequence[float], None] = None) -> "VideoNode": ...
    def PlaneStats(self, clipa: "VideoNode", clipb: typing.Optional["VideoNode"] = None, plane: typing.Optional[int] = None, prop: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def PreMultiply(self, clip: "VideoNode", alpha: "VideoNode") -> "VideoNode": ...
    def Prewitt(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None, scale: typing.Optional[float] = None) -> "VideoNode": ...
    def PropToClip(self, clip: "VideoNode", prop: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def RemoveFrameProps(self, clip: "VideoNode", props: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None) -> "VideoNode": ...
    def Reverse(self, clip: "VideoNode") -> "VideoNode": ...
    def SelectEvery(self, clip: "VideoNode", cycle: int, offsets: typing.Union[int, typing.Sequence[int]], modify_duration: typing.Optional[int] = None) -> "VideoNode": ...
    def SeparateFields(self, clip: "VideoNode", tff: typing.Optional[int] = None, modify_duration: typing.Optional[int] = None) -> "VideoNode": ...
    def SetAudioCache(self, clip: "AudioNode", mode: typing.Optional[int] = None, fixedsize: typing.Optional[int] = None, maxsize: typing.Optional[int] = None, maxhistory: typing.Optional[int] = None) -> None: ...
    def SetFieldBased(self, clip: "VideoNode", value: int) -> "VideoNode": ...
    def SetFrameProp(self, clip: "VideoNode", prop: typing.Union[str, bytes, bytearray], intval: typing.Union[int, typing.Sequence[int], None] = None, floatval: typing.Union[float, typing.Sequence[float], None] = None, data: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None) -> "VideoNode": ...
    def SetFrameProps(self, clip: "VideoNode", **kwargs: typing.Any) -> "VideoNode": ...
    def SetMaxCPU(self, cpu: typing.Union[str, bytes, bytearray]) -> typing.Union[str, bytes, bytearray]: ...
    def SetVideoCache(self, clip: "VideoNode", mode: typing.Optional[int] = None, fixedsize: typing.Optional[int] = None, maxsize: typing.Optional[int] = None, maxhistory: typing.Optional[int] = None) -> None: ...
    def ShuffleChannels(self, clips: typing.Union["AudioNode", typing.Sequence["AudioNode"]], channels_in: typing.Union[int, typing.Sequence[int]], channels_out: typing.Union[int, typing.Sequence[int]]) -> "AudioNode": ...
    def ShufflePlanes(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]], planes: typing.Union[int, typing.Sequence[int]], colorfamily: int) -> "VideoNode": ...
    def Sobel(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None, scale: typing.Optional[float] = None) -> "VideoNode": ...
    def Splice(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]], mismatch: typing.Optional[int] = None) -> "VideoNode": ...
    def SplitChannels(self, clip: "AudioNode") -> typing.Union["AudioNode", typing.Sequence["AudioNode"]]: ...
    def SplitPlanes(self, clip: "VideoNode") -> typing.Union["VideoNode", typing.Sequence["VideoNode"]]: ...
    def StackHorizontal(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]]) -> "VideoNode": ...
    def StackVertical(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]]) -> "VideoNode": ...
    def TestAudio(self, channels: typing.Union[int, typing.Sequence[int], None] = None, bits: typing.Optional[int] = None, isfloat: typing.Optional[int] = None, samplerate: typing.Optional[int] = None, length: typing.Optional[int] = None) -> "AudioNode": ...
    def Transpose(self, clip: "VideoNode") -> "VideoNode": ...
    def Trim(self, clip: "VideoNode", first: typing.Optional[int] = None, last: typing.Optional[int] = None, length: typing.Optional[int] = None) -> "VideoNode": ...
    def Turn180(self, clip: "VideoNode") -> "VideoNode": ...


class _Plugin_std_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def AddBorders(self, left: typing.Optional[int] = None, right: typing.Optional[int] = None, top: typing.Optional[int] = None, bottom: typing.Optional[int] = None, color: typing.Union[float, typing.Sequence[float], None] = None) -> "VideoNode": ...
    def AssumeFPS(self, src: typing.Optional["VideoNode"] = None, fpsnum: typing.Optional[int] = None, fpsden: typing.Optional[int] = None) -> "VideoNode": ...
    def AverageFrames(self, weights: typing.Union[float, typing.Sequence[float]], scale: typing.Optional[float] = None, scenechange: typing.Optional[int] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Binarize(self, threshold: typing.Union[float, typing.Sequence[float], None] = None, v0: typing.Union[float, typing.Sequence[float], None] = None, v1: typing.Union[float, typing.Sequence[float], None] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def BinarizeMask(self, threshold: typing.Union[float, typing.Sequence[float], None] = None, v0: typing.Union[float, typing.Sequence[float], None] = None, v1: typing.Union[float, typing.Sequence[float], None] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def BlankClip(self, width: typing.Optional[int] = None, height: typing.Optional[int] = None, format: typing.Optional[int] = None, length: typing.Optional[int] = None, fpsnum: typing.Optional[int] = None, fpsden: typing.Optional[int] = None, color: typing.Union[float, typing.Sequence[float], None] = None, keep: typing.Optional[int] = None) -> "VideoNode": ...
    def BoxBlur(self, planes: typing.Union[int, typing.Sequence[int], None] = None, hradius: typing.Optional[int] = None, hpasses: typing.Optional[int] = None, vradius: typing.Optional[int] = None, vpasses: typing.Optional[int] = None) -> "VideoNode": ...
    def Cache(self, size: typing.Optional[int] = None, fixed: typing.Optional[int] = None, make_linear: typing.Optional[int] = None) -> "VideoNode": ...
    def ClipToProp(self, mclip: "VideoNode", prop: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def Convolution(self, matrix: typing.Union[float, typing.Sequence[float]], bias: typing.Optional[float] = None, divisor: typing.Optional[float] = None, planes: typing.Union[int, typing.Sequence[int], None] = None, saturate: typing.Optional[int] = None, mode: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def CopyFrameProps(self, prop_src: "VideoNode") -> "VideoNode": ...
    def Crop(self, left: typing.Optional[int] = None, right: typing.Optional[int] = None, top: typing.Optional[int] = None, bottom: typing.Optional[int] = None) -> "VideoNode": ...
    def CropAbs(self, width: int, height: int, left: typing.Optional[int] = None, top: typing.Optional[int] = None, x: typing.Optional[int] = None, y: typing.Optional[int] = None) -> "VideoNode": ...
    def CropRel(self, left: typing.Optional[int] = None, right: typing.Optional[int] = None, top: typing.Optional[int] = None, bottom: typing.Optional[int] = None) -> "VideoNode": ...
    def Deflate(self, planes: typing.Union[int, typing.Sequence[int], None] = None, threshold: typing.Optional[float] = None) -> "VideoNode": ...
    def DeleteFrames(self, frames: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def DoubleWeave(self, tff: typing.Optional[int] = None) -> "VideoNode": ...
    def DuplicateFrames(self, frames: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def Expr(self, expr: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]]], format: typing.Optional[int] = None) -> "VideoNode": ...
    def FlipHorizontal(self) -> "VideoNode": ...
    def FlipVertical(self) -> "VideoNode": ...
    def FrameEval(self, eval: typing.Callable[..., typing.Any], prop_src: typing.Union["VideoNode", typing.Sequence["VideoNode"], None] = None, clip_src: typing.Union["VideoNode", typing.Sequence["VideoNode"], None] = None) -> "VideoNode": ...
    def FreezeFrames(self, first: typing.Union[int, typing.Sequence[int], None] = None, last: typing.Union[int, typing.Sequence[int], None] = None, replacement: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Inflate(self, planes: typing.Union[int, typing.Sequence[int], None] = None, threshold: typing.Optional[float] = None) -> "VideoNode": ...
    def Interleave(self, extend: typing.Optional[int] = None, mismatch: typing.Optional[int] = None, modify_duration: typing.Optional[int] = None) -> "VideoNode": ...
    def Invert(self, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def InvertMask(self, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Levels(self, min_in: typing.Union[float, typing.Sequence[float], None] = None, max_in: typing.Union[float, typing.Sequence[float], None] = None, gamma: typing.Union[float, typing.Sequence[float], None] = None, min_out: typing.Union[float, typing.Sequence[float], None] = None, max_out: typing.Union[float, typing.Sequence[float], None] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Limiter(self, min: typing.Union[float, typing.Sequence[float], None] = None, max: typing.Union[float, typing.Sequence[float], None] = None, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Loop(self, times: typing.Optional[int] = None) -> "VideoNode": ...
    def Lut(self, planes: typing.Union[int, typing.Sequence[int], None] = None, lut: typing.Union[int, typing.Sequence[int], None] = None, lutf: typing.Union[float, typing.Sequence[float], None] = None, function: typing.Optional[typing.Callable[..., typing.Any]] = None, bits: typing.Optional[int] = None, floatout: typing.Optional[int] = None) -> "VideoNode": ...
    def Lut2(self, clipb: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None, lut: typing.Union[int, typing.Sequence[int], None] = None, lutf: typing.Union[float, typing.Sequence[float], None] = None, function: typing.Optional[typing.Callable[..., typing.Any]] = None, bits: typing.Optional[int] = None, floatout: typing.Optional[int] = None) -> "VideoNode": ...
    def MakeDiff(self, clipb: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def MakeFullDiff(self, clipb: "VideoNode") -> "VideoNode": ...
    def MaskedMerge(self, clipb: "VideoNode", mask: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None, first_plane: typing.Optional[int] = None, premultiplied: typing.Optional[int] = None) -> "VideoNode": ...
    def Maximum(self, planes: typing.Union[int, typing.Sequence[int], None] = None, threshold: typing.Optional[float] = None, coordinates: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Median(self, planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def Merge(self, clipb: "VideoNode", weight: typing.Union[float, typing.Sequence[float], None] = None) -> "VideoNode": ...
    def MergeDiff(self, clipb: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def MergeFullDiff(self, clipb: "VideoNode") -> "VideoNode": ...
    def Minimum(self, planes: typing.Union[int, typing.Sequence[int], None] = None, threshold: typing.Optional[float] = None, coordinates: typing.Union[int, typing.Sequence[int], None] = None) -> "VideoNode": ...
    def ModifyFrame(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]], selector: typing.Callable[..., typing.Any]) -> "VideoNode": ...
    def PEMVerifier(self, upper: typing.Union[float, typing.Sequence[float], None] = None, lower: typing.Union[float, typing.Sequence[float], None] = None) -> "VideoNode": ...
    def PlaneStats(self, clipb: typing.Optional["VideoNode"] = None, plane: typing.Optional[int] = None, prop: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def PreMultiply(self, alpha: "VideoNode") -> "VideoNode": ...
    def Prewitt(self, planes: typing.Union[int, typing.Sequence[int], None] = None, scale: typing.Optional[float] = None) -> "VideoNode": ...
    def PropToClip(self, prop: typing.Union[str, bytes, bytearray, None] = None) -> "VideoNode": ...
    def RemoveFrameProps(self, props: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None) -> "VideoNode": ...
    def Reverse(self) -> "VideoNode": ...
    def SelectEvery(self, cycle: int, offsets: typing.Union[int, typing.Sequence[int]], modify_duration: typing.Optional[int] = None) -> "VideoNode": ...
    def SeparateFields(self, tff: typing.Optional[int] = None, modify_duration: typing.Optional[int] = None) -> "VideoNode": ...
    def SetFieldBased(self, value: int) -> "VideoNode": ...
    def SetFrameProp(self, prop: typing.Union[str, bytes, bytearray], intval: typing.Union[int, typing.Sequence[int], None] = None, floatval: typing.Union[float, typing.Sequence[float], None] = None, data: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = None) -> "VideoNode": ...
    def SetFrameProps(self, **kwargs: typing.Any) -> "VideoNode": ...
    def SetVideoCache(self, mode: typing.Optional[int] = None, fixedsize: typing.Optional[int] = None, maxsize: typing.Optional[int] = None, maxhistory: typing.Optional[int] = None) -> None: ...
    def ShufflePlanes(self, planes: typing.Union[int, typing.Sequence[int]], colorfamily: int) -> "VideoNode": ...
    def Sobel(self, planes: typing.Union[int, typing.Sequence[int], None] = None, scale: typing.Optional[float] = None) -> "VideoNode": ...
    def Splice(self, mismatch: typing.Optional[int] = None) -> "VideoNode": ...
    def SplitPlanes(self) -> typing.Union["VideoNode", typing.Sequence["VideoNode"]]: ...
    def StackHorizontal(self) -> "VideoNode": ...
    def StackVertical(self) -> "VideoNode": ...
    def Transpose(self) -> "VideoNode": ...
    def Trim(self, first: typing.Optional[int] = None, last: typing.Optional[int] = None, length: typing.Optional[int] = None) -> "VideoNode": ...
    def Turn180(self) -> "VideoNode": ...


class _Plugin_std_AudioNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def AssumeSampleRate(self, src: typing.Optional["AudioNode"] = None, samplerate: typing.Optional[int] = None) -> "AudioNode": ...
    def AudioGain(self, gain: typing.Union[float, typing.Sequence[float], None] = None) -> "AudioNode": ...
    def AudioLoop(self, times: typing.Optional[int] = None) -> "AudioNode": ...
    def AudioMix(self, matrix: typing.Union[float, typing.Sequence[float]], channels_out: typing.Union[int, typing.Sequence[int]]) -> "AudioNode": ...
    def AudioReverse(self) -> "AudioNode": ...
    def AudioSplice(self) -> "AudioNode": ...
    def AudioTrim(self, first: typing.Optional[int] = None, last: typing.Optional[int] = None, length: typing.Optional[int] = None) -> "AudioNode": ...
    def BlankAudio(self, channels: typing.Union[int, typing.Sequence[int], None] = None, bits: typing.Optional[int] = None, sampletype: typing.Optional[int] = None, samplerate: typing.Optional[int] = None, length: typing.Optional[int] = None, keep: typing.Optional[int] = None) -> "AudioNode": ...
    def SetAudioCache(self, mode: typing.Optional[int] = None, fixedsize: typing.Optional[int] = None, maxsize: typing.Optional[int] = None, maxhistory: typing.Optional[int] = None) -> None: ...
    def ShuffleChannels(self, channels_in: typing.Union[int, typing.Sequence[int]], channels_out: typing.Union[int, typing.Sequence[int]]) -> "AudioNode": ...
    def SplitChannels(self) -> typing.Union["AudioNode", typing.Sequence["AudioNode"]]: ...

# end implementation


# implementation: wwxd

class _Plugin_wwxd_Core_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def WWXD(self, clip: "VideoNode") -> "VideoNode": ...


class _Plugin_wwxd_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def WWXD(self) -> "VideoNode": ...

# end implementation


class VideoNode:
# instance_bound_VideoNode: imwri
    @property
    def imwri(self) -> _Plugin_imwri_VideoNode_Bound:
        """
        VapourSynth ImageMagick 7 HDRI Writer/Reader
        """
# end instance
# instance_bound_VideoNode: mv
    @property
    def mv(self) -> _Plugin_mv_VideoNode_Bound:
        """
        MVTools v23
        """
# end instance
# instance_bound_VideoNode: resize
    @property
    def resize(self) -> _Plugin_resize_VideoNode_Bound:
        """
        VapourSynth Resize
        """
# end instance
# instance_bound_VideoNode: scxvid
    @property
    def scxvid(self) -> _Plugin_scxvid_VideoNode_Bound:
        """
        VapourSynth Scxvid Plugin
        """
# end instance
# instance_bound_VideoNode: std
    @property
    def std(self) -> _Plugin_std_VideoNode_Bound:
        """
        VapourSynth Core Functions
        """
# end instance
# instance_bound_VideoNode: wwxd
    @property
    def wwxd(self) -> _Plugin_wwxd_VideoNode_Bound:
        """
        Scene change detection approximately like Xvid's
        """
# end instance

    format: typing.Optional[VideoFormat]

    fps: fractions.Fraction
    fps_den: int
    fps_num: int

    height: int
    width: int

    num_frames: int

    # RawNode methods
    @typing.overload
    def get_frame_async_raw(self, n: int, cb: typing.Callable[['VideoNode', int, VideoFrame], None]) -> None: ...
    @typing.overload
    def get_frame_async_raw(self, n: int, cb: _Future[VideoFrame], future_wrapper: typing.Optional[typing.Callable[..., None]] = None) -> _Future[VideoFrame]: ...
    def get_frame_async(self, n: int) -> _Future[VideoFrame]: ...
    def frames(self, prefetch: typing.Optional[int] = None, backlog: typing.Optional[int] = None, close: bool = False) -> typing.Iterator[VideoFrame]: ...

    def get_frame(self, n: int) -> VideoFrame: ...
    def set_output(self, index: int = 0, alpha: typing.Optional['VideoNode'] = None, alt_output: int = 0) -> None: ...
    def output(self, fileobj: typing.BinaryIO, y4m: bool = False, progress_update: typing.Optional[typing.Callable[[int, int], None]] = None, prefetch: int = 0, backlog: int = -1) -> None: ...

    def __add__(self, other: 'VideoNode') -> 'VideoNode': ...
    def __radd__(self, other: 'VideoNode') -> 'VideoNode': ...
    def __mul__(self, other: int) -> 'VideoNode': ...
    def __rmul__(self, other: int) -> 'VideoNode': ...
    def __getitem__(self, other: typing.Union[int, slice]) -> 'VideoNode': ...
    def __len__(self) -> int: ...


class AudioFrame(_RawFrame):
    sample_type: SampleType
    bits_per_sample: int
    bytes_per_sample: int
    channel_layout: int
    num_channels: int

    def copy(self) -> 'AudioFrame': ...

    def __enter__(self) -> 'AudioFrame': ...

    def __getitem__(self, index: int) -> memoryview: ...
    def __len__(self) -> int: ...


class AudioNode:
# instance_bound_AudioNode: std
    @property
    def std(self) -> _Plugin_std_AudioNode_Bound:
        """
        VapourSynth Core Functions
        """
# end instance

    sample_type: SampleType
    bits_per_sample: int
    bytes_per_sample: int
    channel_layout: int
    num_channels: int
    sample_rate: int
    num_samples: int

    num_frames: int

    # RawNode methods
    @typing.overload
    def get_frame_async_raw(self, n: int, cb: typing.Callable[['AudioNode', int, AudioFrame], None]) -> None: ...
    @typing.overload
    def get_frame_async_raw(self, n: int, cb: _Future[AudioFrame], future_wrapper: typing.Optional[typing.Callable[..., None]] = None) -> _Future[AudioFrame]: ...
    def get_frame_async(self, n: int) -> _Future[AudioFrame]: ...
    def frames(self, prefetch: typing.Optional[int] = None, backlog: typing.Optional[int] = None, close: bool = False) -> typing.Iterator[AudioFrame]: ...

    def get_frame(self, n: int) -> AudioFrame: ...
    def set_output(self, index: int = 0) -> None: ...

    def __add__(self, other: 'AudioNode') -> 'AudioNode': ...
    def __radd__(self, other: 'AudioNode') -> 'AudioNode': ...
    def __mul__(self, other: int) -> 'AudioNode': ...
    def __rmul__(self, other: int) -> 'AudioNode': ...
    def __getitem__(self, other: typing.Union[int, slice]) -> 'AudioNode': ...
    def __len__(self) -> int: ...


class _PluginMeta(typing.TypedDict):
    namespace: str
    identifier: str
    name: str
    functions: typing.Dict[str, str]


class LogHandle:
    handler_func: typing.Callable[[MessageType, str], None]


class Core:
# instance_bound_Core: bas
    @property
    def bas(self) -> _Plugin_bas_Core_Bound:
        """
        Best Audio Source
        """
# end instance
# instance_bound_Core: ffms2
    @property
    def ffms2(self) -> _Plugin_ffms2_Core_Bound:
        """
        FFmpegSource 2 for VapourSynth
        """
# end instance
# instance_bound_Core: imwri
    @property
    def imwri(self) -> _Plugin_imwri_Core_Bound:
        """
        VapourSynth ImageMagick 7 HDRI Writer/Reader
        """
# end instance
# instance_bound_Core: lsmas
    @property
    def lsmas(self) -> _Plugin_lsmas_Core_Bound:
        """
        LSMASHSource for VapourSynth
        """
# end instance
# instance_bound_Core: mv
    @property
    def mv(self) -> _Plugin_mv_Core_Bound:
        """
        MVTools v23
        """
# end instance
# instance_bound_Core: resize
    @property
    def resize(self) -> _Plugin_resize_Core_Bound:
        """
        VapourSynth Resize
        """
# end instance
# instance_bound_Core: scxvid
    @property
    def scxvid(self) -> _Plugin_scxvid_Core_Bound:
        """
        VapourSynth Scxvid Plugin
        """
# end instance
# instance_bound_Core: std
    @property
    def std(self) -> _Plugin_std_Core_Bound:
        """
        VapourSynth Core Functions
        """
# end instance
# instance_bound_Core: wwxd
    @property
    def wwxd(self) -> _Plugin_wwxd_Core_Bound:
        """
        Scene change detection approximately like Xvid's
        """
# end instance

    @property
    def num_threads(self) -> int: ...
    @num_threads.setter
    def num_threads(self) -> None: ...
    @property
    def max_cache_size(self) -> int: ...
    @max_cache_size.setter
    def max_cache_size(self) -> None: ...

    def plugins(self) -> typing.Iterator[Plugin]: ...
    # get_plugins is deprecated
    def get_plugins(self) -> typing.Dict[str, _PluginMeta]: ...
    # list_functions is deprecated
    def list_functions(self) -> str: ...

    def query_video_format(self, color_family: ColorFamily, sample_type: SampleType, bits_per_sample: int, subsampling_w: int = 0, subsampling_h: int = 0) -> VideoFormat: ...
    # register_format is deprecated
    def register_format(self, color_family: ColorFamily, sample_type: SampleType, bits_per_sample: int, subsampling_w: int, subsampling_h: int) -> VideoFormat: ...
    def get_video_format(self, id: typing.Union[VideoFormat, int, PresetFormat]) -> VideoFormat: ...
    # get_format is deprecated
    def get_format(self, id: typing.Union[VideoFormat, int, PresetFormat]) -> VideoFormat: ...
    def log_message(self, message_type: MessageType, message: str) -> None: ...
    def add_log_handler(self, handler_func: typing.Optional[typing.Callable[[MessageType, str], None]]) -> LogHandle: ...
    def remove_log_handler(self, handle: LogHandle) -> None: ...

    def version(self) -> str: ...
    def version_number(self) -> int: ...


class _CoreProxy(Core):
    @property
    def core(self) -> Core: ...


core: _CoreProxy
