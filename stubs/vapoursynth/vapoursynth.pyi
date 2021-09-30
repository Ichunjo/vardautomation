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
    def copy(self) -> Environment: ...
    def use(self) -> typing.ContextManager[None]: ...

    def __enter__(self) -> Environment: ...
    def __exit__(self, ty: typing.Type[BaseException], tv: BaseException, tb: types.TracebackType) -> None: ...

class EnvironmentPolicyAPI:
    def wrap_environment(self, environment_data: EnvironmentData) -> Environment: ...
    def create_environment(self) -> EnvironmentData: ...
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

def construct_signature(signature: str, return_signature: str, injected: typing.Optional[str] = ...) -> inspect.Signature: ...


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
                color_family: typing.Optional[ColorFamily] = ...,
                sample_type: typing.Optional[SampleType] = ...,
                bits_per_sample: typing.Optional[int] = ...,
                subsampling_w: typing.Optional[int] = ...,
                subsampling_h: typing.Optional[int] = ...
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


class VideoFrame:
    props: FrameProps
    height: int
    width: int
    format: VideoFormat
    readonly: bool

    def copy(self) -> 'VideoFrame': ...
    def get_read_ptr(self, plane: int) -> ctypes.c_void_p: ...
    def get_write_ptr(self, plane: int) -> ctypes.c_void_p: ...
    def get_stride(self, plane: int) -> int: ...
    def __getitem__(self, index: int) -> memoryview: ...
    def __len__(self) -> int: ...

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


class _Plugin_acrop_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def AutoCrop(self, clip: "VideoNode", range: typing.Optional[int] = ..., top: typing.Optional[int] = ..., bottom: typing.Optional[int] = ..., left: typing.Optional[int] = ..., right: typing.Optional[int] = ..., color: typing.Union[int, typing.Sequence[int], None] = ..., color_second: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def CropProp(self, clip: "VideoNode") -> "VideoNode": ...
    def CropValues(self, clip: "VideoNode", range: typing.Optional[int] = ..., top: typing.Optional[int] = ..., bottom: typing.Optional[int] = ..., left: typing.Optional[int] = ..., right: typing.Optional[int] = ..., color: typing.Union[int, typing.Sequence[int], None] = ..., color_second: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...


class _Plugin_ocr_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Recognize(self, clip: "VideoNode", datapath: typing.Union[str, bytes, bytearray, None] = ..., language: typing.Union[str, bytes, bytearray, None] = ..., options: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = ...) -> "VideoNode": ...


class _Plugin_remap_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def RemapFrames(self, baseclip: "VideoNode", filename: typing.Union[str, bytes, bytearray, None] = ..., mappings: typing.Union[str, bytes, bytearray, None] = ..., sourceclip: typing.Optional["VideoNode"] = ..., mismatch: typing.Optional[int] = ...) -> "VideoNode": ...
    def RemapFramesSimple(self, clip: "VideoNode", filename: typing.Union[str, bytes, bytearray, None] = ..., mappings: typing.Union[str, bytes, bytearray, None] = ...) -> "VideoNode": ...
    def Remf(self, baseclip: "VideoNode", filename: typing.Union[str, bytes, bytearray, None] = ..., mappings: typing.Union[str, bytes, bytearray, None] = ..., sourceclip: typing.Optional["VideoNode"] = ..., mismatch: typing.Optional[int] = ...) -> "VideoNode": ...
    def Remfs(self, clip: "VideoNode", filename: typing.Union[str, bytes, bytearray, None] = ..., mappings: typing.Union[str, bytes, bytearray, None] = ...) -> "VideoNode": ...
    def ReplaceFramesSimple(self, baseclip: "VideoNode", sourceclip: "VideoNode", filename: typing.Union[str, bytes, bytearray, None] = ..., mappings: typing.Union[str, bytes, bytearray, None] = ..., mismatch: typing.Optional[int] = ...) -> "VideoNode": ...
    def Rfs(self, baseclip: "VideoNode", sourceclip: "VideoNode", filename: typing.Union[str, bytes, bytearray, None] = ..., mappings: typing.Union[str, bytes, bytearray, None] = ..., mismatch: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_comb_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def CMaskedMerge(self, base: "VideoNode", alt: "VideoNode", mask: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def CombMask(self, clip: "VideoNode", cthresh: typing.Optional[int] = ..., mthresh: typing.Optional[int] = ..., mi: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...


class _Plugin_focus2_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TemporalSoften2(self, clip: "VideoNode", radius: typing.Optional[int] = ..., luma_threshold: typing.Optional[int] = ..., chroma_threshold: typing.Optional[int] = ..., scenechange: typing.Optional[int] = ..., mode: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_knlm_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def KNLMeansCL(self, clip: "VideoNode", d: typing.Optional[int] = ..., a: typing.Optional[int] = ..., s: typing.Optional[int] = ..., h: typing.Optional[float] = ..., channels: typing.Union[str, bytes, bytearray, None] = ..., wmode: typing.Optional[int] = ..., wref: typing.Optional[float] = ..., rclip: typing.Optional["VideoNode"] = ..., device_type: typing.Union[str, bytes, bytearray, None] = ..., device_id: typing.Optional[int] = ..., ocl_x: typing.Optional[int] = ..., ocl_y: typing.Optional[int] = ..., ocl_r: typing.Optional[int] = ..., info: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_ftf_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def FixFades(self, clip: "VideoNode", mode: typing.Optional[int] = ..., threshold: typing.Optional[float] = ..., color: typing.Union[float, typing.Sequence[float], None] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_nnedi3_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def nnedi3(self, clip: "VideoNode", field: int, dh: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., nsize: typing.Optional[int] = ..., nns: typing.Optional[int] = ..., qual: typing.Optional[int] = ..., etype: typing.Optional[int] = ..., pscrn: typing.Optional[int] = ..., opt: typing.Optional[int] = ..., int16_prescreener: typing.Optional[int] = ..., int16_predictor: typing.Optional[int] = ..., exp: typing.Optional[int] = ..., show_mask: typing.Optional[int] = ..., combed_only: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_libp2p_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Pack(self, clip: "VideoNode") -> "VideoNode": ...
    def Unpack(self, clip: "VideoNode") -> "VideoNode": ...


class _Plugin_ccd_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def CCD(self, clip: "VideoNode", threshold: typing.Optional[float] = ...) -> "VideoNode": ...


class _Plugin_grain_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Add(self, clip: "VideoNode", var: typing.Optional[float] = ..., uvar: typing.Optional[float] = ..., hcorr: typing.Optional[float] = ..., vcorr: typing.Optional[float] = ..., seed: typing.Optional[int] = ..., constant: typing.Optional[int] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_cas_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def CAS(self, clip: "VideoNode", sharpness: typing.Optional[float] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_ctmf_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def CTMF(self, clip: "VideoNode", radius: typing.Optional[int] = ..., memsize: typing.Optional[int] = ..., opt: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...


class _Plugin_dctf_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def DCTFilter(self, clip: "VideoNode", factors: typing.Union[float, typing.Sequence[float]], planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...


class _Plugin_deblock_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Deblock(self, clip: "VideoNode", quant: typing.Optional[int] = ..., aoffset: typing.Optional[int] = ..., boffset: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...


class _Plugin_dfttest_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def DFTTest(self, clip: "VideoNode", ftype: typing.Optional[int] = ..., sigma: typing.Optional[float] = ..., sigma2: typing.Optional[float] = ..., pmin: typing.Optional[float] = ..., pmax: typing.Optional[float] = ..., sbsize: typing.Optional[int] = ..., smode: typing.Optional[int] = ..., sosize: typing.Optional[int] = ..., tbsize: typing.Optional[int] = ..., tmode: typing.Optional[int] = ..., tosize: typing.Optional[int] = ..., swin: typing.Optional[int] = ..., twin: typing.Optional[int] = ..., sbeta: typing.Optional[float] = ..., tbeta: typing.Optional[float] = ..., zmean: typing.Optional[int] = ..., f0beta: typing.Optional[float] = ..., nlocation: typing.Union[int, typing.Sequence[int], None] = ..., alpha: typing.Optional[float] = ..., slocation: typing.Union[float, typing.Sequence[float], None] = ..., ssx: typing.Union[float, typing.Sequence[float], None] = ..., ssy: typing.Union[float, typing.Sequence[float], None] = ..., sst: typing.Union[float, typing.Sequence[float], None] = ..., ssystem: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_eedi2_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def EEDI2(self, clip: "VideoNode", field: int, mthresh: typing.Optional[int] = ..., lthresh: typing.Optional[int] = ..., vthresh: typing.Optional[int] = ..., estr: typing.Optional[int] = ..., dstr: typing.Optional[int] = ..., maxd: typing.Optional[int] = ..., map: typing.Optional[int] = ..., nt: typing.Optional[int] = ..., pp: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_eedi3m_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def EEDI3(self, clip: "VideoNode", field: int, dh: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., alpha: typing.Optional[float] = ..., beta: typing.Optional[float] = ..., gamma: typing.Optional[float] = ..., nrad: typing.Optional[int] = ..., mdis: typing.Optional[int] = ..., hp: typing.Optional[int] = ..., ucubic: typing.Optional[int] = ..., cost3: typing.Optional[int] = ..., vcheck: typing.Optional[int] = ..., vthresh0: typing.Optional[float] = ..., vthresh1: typing.Optional[float] = ..., vthresh2: typing.Optional[float] = ..., sclip: typing.Optional["VideoNode"] = ..., mclip: typing.Optional["VideoNode"] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...
    def EEDI3CL(self, clip: "VideoNode", field: int, dh: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., alpha: typing.Optional[float] = ..., beta: typing.Optional[float] = ..., gamma: typing.Optional[float] = ..., nrad: typing.Optional[int] = ..., mdis: typing.Optional[int] = ..., hp: typing.Optional[int] = ..., ucubic: typing.Optional[int] = ..., cost3: typing.Optional[int] = ..., vcheck: typing.Optional[int] = ..., vthresh0: typing.Optional[float] = ..., vthresh1: typing.Optional[float] = ..., vthresh2: typing.Optional[float] = ..., sclip: typing.Optional["VideoNode"] = ..., opt: typing.Optional[int] = ..., device: typing.Optional[int] = ..., list_device: typing.Optional[int] = ..., info: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_lghost_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def LGhost(self, clip: "VideoNode", mode: typing.Union[int, typing.Sequence[int]], shift: typing.Union[int, typing.Sequence[int]], intensity: typing.Union[int, typing.Sequence[int]], planes: typing.Union[int, typing.Sequence[int], None] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_nnedi3cl_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def NNEDI3CL(self, clip: "VideoNode", field: int, dh: typing.Optional[int] = ..., dw: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., nsize: typing.Optional[int] = ..., nns: typing.Optional[int] = ..., qual: typing.Optional[int] = ..., etype: typing.Optional[int] = ..., pscrn: typing.Optional[int] = ..., device: typing.Optional[int] = ..., list_device: typing.Optional[int] = ..., info: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_mpls_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Read(self, bd_path: typing.Union[str, bytes, bytearray], playlist: int, angle: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_tcanny_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TCanny(self, clip: "VideoNode", sigma: typing.Union[float, typing.Sequence[float], None] = ..., sigma_v: typing.Union[float, typing.Sequence[float], None] = ..., t_h: typing.Optional[float] = ..., t_l: typing.Optional[float] = ..., mode: typing.Optional[int] = ..., op: typing.Optional[int] = ..., gmmax: typing.Optional[float] = ..., opt: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def TCannyCL(self, clip: "VideoNode", sigma: typing.Union[float, typing.Sequence[float], None] = ..., sigma_v: typing.Union[float, typing.Sequence[float], None] = ..., t_h: typing.Optional[float] = ..., t_l: typing.Optional[float] = ..., mode: typing.Optional[int] = ..., op: typing.Optional[int] = ..., gmmax: typing.Optional[float] = ..., device: typing.Optional[int] = ..., list_device: typing.Optional[int] = ..., info: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...


class _Plugin_tdm_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def IsCombed(self, clip: "VideoNode", cthresh: typing.Optional[int] = ..., blockx: typing.Optional[int] = ..., blocky: typing.Optional[int] = ..., chroma: typing.Optional[int] = ..., mi: typing.Optional[int] = ..., metric: typing.Optional[int] = ...) -> "VideoNode": ...
    def TDeintMod(self, clip: "VideoNode", order: int, field: typing.Optional[int] = ..., mode: typing.Optional[int] = ..., length: typing.Optional[int] = ..., mtype: typing.Optional[int] = ..., ttype: typing.Optional[int] = ..., mtql: typing.Optional[int] = ..., mthl: typing.Optional[int] = ..., mtqc: typing.Optional[int] = ..., mthc: typing.Optional[int] = ..., nt: typing.Optional[int] = ..., minthresh: typing.Optional[int] = ..., maxthresh: typing.Optional[int] = ..., cstr: typing.Optional[int] = ..., athresh: typing.Optional[int] = ..., metric: typing.Optional[int] = ..., expand: typing.Optional[int] = ..., link: typing.Optional[int] = ..., show: typing.Optional[int] = ..., edeint: typing.Optional["VideoNode"] = ..., opt: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...


class _Plugin_ttmpsm_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TTempSmooth(self, clip: "VideoNode", maxr: typing.Optional[int] = ..., thresh: typing.Union[int, typing.Sequence[int], None] = ..., mdiff: typing.Union[int, typing.Sequence[int], None] = ..., strength: typing.Optional[int] = ..., scthresh: typing.Optional[float] = ..., fp: typing.Optional[int] = ..., pfclip: typing.Optional["VideoNode"] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...


class _Plugin_vsf_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TextSub(self, clip: "VideoNode", file: typing.Union[str, bytes, bytearray], charset: typing.Optional[int] = ..., fps: typing.Optional[float] = ..., vfr: typing.Union[str, bytes, bytearray, None] = ...) -> "VideoNode": ...
    def VobSub(self, clip: "VideoNode", file: typing.Union[str, bytes, bytearray]) -> "VideoNode": ...


class _Plugin_vsfm_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TextSubMod(self, clip: "VideoNode", file: typing.Union[str, bytes, bytearray], charset: typing.Optional[int] = ..., fps: typing.Optional[float] = ..., vfr: typing.Union[str, bytes, bytearray, None] = ..., accurate: typing.Optional[int] = ...) -> "VideoNode": ...
    def VobSub(self, clip: "VideoNode", file: typing.Union[str, bytes, bytearray], accurate: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_w2xc_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Waifu2x(self, clip: "VideoNode", noise: typing.Optional[int] = ..., scale: typing.Optional[int] = ..., block: typing.Optional[int] = ..., photo: typing.Optional[int] = ..., gpu: typing.Optional[int] = ..., processor: typing.Optional[int] = ..., list_proc: typing.Optional[int] = ..., log: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_yadifmod_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Yadifmod(self, clip: "VideoNode", edeint: "VideoNode", order: int, field: typing.Optional[int] = ..., mode: typing.Optional[int] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_tonemap_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Hable(self, clip: "VideoNode", exposure: typing.Optional[float] = ..., a: typing.Optional[float] = ..., b: typing.Optional[float] = ..., c: typing.Optional[float] = ..., d: typing.Optional[float] = ..., e: typing.Optional[float] = ..., f: typing.Optional[float] = ..., w: typing.Optional[float] = ...) -> "VideoNode": ...
    def Mobius(self, clip: "VideoNode", exposure: typing.Optional[float] = ..., transition: typing.Optional[float] = ..., peak: typing.Optional[float] = ...) -> "VideoNode": ...
    def Reinhard(self, clip: "VideoNode", exposure: typing.Optional[float] = ..., contrast: typing.Optional[float] = ..., peak: typing.Optional[float] = ...) -> "VideoNode": ...


class _Plugin_sangnom_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def SangNom(self, clip: "VideoNode", order: typing.Optional[int] = ..., dh: typing.Optional[int] = ..., aa: typing.Union[int, typing.Sequence[int], None] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...


class _Plugin_edgefixer_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ContinuityFixer(self, clip: "VideoNode", left: typing.Union[int, typing.Sequence[int]], top: typing.Union[int, typing.Sequence[int]], right: typing.Union[int, typing.Sequence[int]], bottom: typing.Union[int, typing.Sequence[int]], radius: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...


class _Plugin_warp_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ABlur(self, clip: "VideoNode", blur: typing.Optional[int] = ..., type: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...
    def ASobel(self, clip: "VideoNode", thresh: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...
    def AWarp(self, clip: "VideoNode", mask: "VideoNode", depth: typing.Union[int, typing.Sequence[int], None] = ..., chroma: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., opt: typing.Optional[int] = ..., cplace: typing.Union[str, bytes, bytearray, None] = ...) -> "VideoNode": ...
    def AWarpSharp2(self, clip: "VideoNode", thresh: typing.Optional[int] = ..., blur: typing.Optional[int] = ..., type: typing.Optional[int] = ..., depth: typing.Union[int, typing.Sequence[int], None] = ..., chroma: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., opt: typing.Optional[int] = ..., cplace: typing.Union[str, bytes, bytearray, None] = ...) -> "VideoNode": ...


class _Plugin_fb_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def FillBorders(self, clip: "VideoNode", left: typing.Optional[int] = ..., right: typing.Optional[int] = ..., top: typing.Optional[int] = ..., bottom: typing.Optional[int] = ..., mode: typing.Union[str, bytes, bytearray, None] = ...) -> "VideoNode": ...


class _Plugin_flux_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def SmoothST(self, clip: "VideoNode", temporal_threshold: typing.Optional[int] = ..., spatial_threshold: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def SmoothT(self, clip: "VideoNode", temporal_threshold: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...


class _Plugin_hist_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Classic(self, clip: "VideoNode") -> "VideoNode": ...
    def Color(self, clip: "VideoNode") -> "VideoNode": ...
    def Color2(self, clip: "VideoNode") -> "VideoNode": ...
    def Levels(self, clip: "VideoNode", factor: typing.Optional[float] = ...) -> "VideoNode": ...
    def Luma(self, clip: "VideoNode") -> "VideoNode": ...


class _Plugin_median_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Median(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]], sync: typing.Optional[int] = ..., samples: typing.Optional[int] = ..., debug: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def MedianBlend(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]], low: typing.Optional[int] = ..., high: typing.Optional[int] = ..., closest: typing.Optional[int] = ..., sync: typing.Optional[int] = ..., samples: typing.Optional[int] = ..., debug: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def TemporalMedian(self, clip: "VideoNode", radius: typing.Optional[int] = ..., debug: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...


class _Plugin_msmoosh_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def MSharpen(self, clip: "VideoNode", threshold: typing.Optional[float] = ..., strength: typing.Optional[float] = ..., mask: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def MSmooth(self, clip: "VideoNode", threshold: typing.Optional[float] = ..., strength: typing.Optional[int] = ..., mask: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...


class _Plugin_mvsf_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Analyse(self, super: "VideoNode", blksize: typing.Optional[int] = ..., blksizev: typing.Optional[int] = ..., levels: typing.Optional[int] = ..., search: typing.Optional[int] = ..., searchparam: typing.Optional[int] = ..., pelsearch: typing.Optional[int] = ..., isb: typing.Optional[int] = ..., lambda_: typing.Optional[float] = ..., chroma: typing.Optional[int] = ..., delta: typing.Optional[int] = ..., truemotion: typing.Optional[int] = ..., lsad: typing.Optional[float] = ..., plevel: typing.Optional[int] = ..., global_: typing.Optional[int] = ..., pnew: typing.Optional[int] = ..., pzero: typing.Optional[int] = ..., pglobal: typing.Optional[int] = ..., overlap: typing.Optional[int] = ..., overlapv: typing.Optional[int] = ..., divide: typing.Optional[int] = ..., badsad: typing.Optional[float] = ..., badrange: typing.Optional[int] = ..., meander: typing.Optional[int] = ..., trymany: typing.Optional[int] = ..., fields: typing.Optional[int] = ..., tff: typing.Optional[int] = ..., search_coarse: typing.Optional[int] = ..., dct: typing.Optional[int] = ...) -> "VideoNode": ...
    def Analyze(self, super: "VideoNode", blksize: typing.Optional[int] = ..., blksizev: typing.Optional[int] = ..., levels: typing.Optional[int] = ..., search: typing.Optional[int] = ..., searchparam: typing.Optional[int] = ..., pelsearch: typing.Optional[int] = ..., isb: typing.Optional[int] = ..., lambda_: typing.Optional[float] = ..., chroma: typing.Optional[int] = ..., delta: typing.Optional[int] = ..., truemotion: typing.Optional[int] = ..., lsad: typing.Optional[float] = ..., plevel: typing.Optional[int] = ..., global_: typing.Optional[int] = ..., pnew: typing.Optional[int] = ..., pzero: typing.Optional[int] = ..., pglobal: typing.Optional[int] = ..., overlap: typing.Optional[int] = ..., overlapv: typing.Optional[int] = ..., divide: typing.Optional[int] = ..., badsad: typing.Optional[float] = ..., badrange: typing.Optional[int] = ..., meander: typing.Optional[int] = ..., trymany: typing.Optional[int] = ..., fields: typing.Optional[int] = ..., tff: typing.Optional[int] = ..., search_coarse: typing.Optional[int] = ..., dct: typing.Optional[int] = ...) -> "VideoNode": ...
    def BlockFPS(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", num: typing.Optional[int] = ..., den: typing.Optional[int] = ..., mode: typing.Optional[int] = ..., ml: typing.Optional[float] = ..., blend: typing.Optional[int] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Compensate(self, clip: "VideoNode", super: "VideoNode", vectors: "VideoNode", scbehavior: typing.Optional[int] = ..., thsad: typing.Optional[float] = ..., fields: typing.Optional[int] = ..., time: typing.Optional[float] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ..., tff: typing.Optional[int] = ...) -> "VideoNode": ...
    def Degrain1(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain10(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain11(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain12(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain13(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain14(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain15(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain16(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain17(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", mvbw17: "VideoNode", mvfw17: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain18(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", mvbw17: "VideoNode", mvfw17: "VideoNode", mvbw18: "VideoNode", mvfw18: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain19(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", mvbw17: "VideoNode", mvfw17: "VideoNode", mvbw18: "VideoNode", mvfw18: "VideoNode", mvbw19: "VideoNode", mvfw19: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain2(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain20(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", mvbw17: "VideoNode", mvfw17: "VideoNode", mvbw18: "VideoNode", mvfw18: "VideoNode", mvbw19: "VideoNode", mvfw19: "VideoNode", mvbw20: "VideoNode", mvfw20: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain21(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", mvbw17: "VideoNode", mvfw17: "VideoNode", mvbw18: "VideoNode", mvfw18: "VideoNode", mvbw19: "VideoNode", mvfw19: "VideoNode", mvbw20: "VideoNode", mvfw20: "VideoNode", mvbw21: "VideoNode", mvfw21: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain22(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", mvbw17: "VideoNode", mvfw17: "VideoNode", mvbw18: "VideoNode", mvfw18: "VideoNode", mvbw19: "VideoNode", mvfw19: "VideoNode", mvbw20: "VideoNode", mvfw20: "VideoNode", mvbw21: "VideoNode", mvfw21: "VideoNode", mvbw22: "VideoNode", mvfw22: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain23(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", mvbw17: "VideoNode", mvfw17: "VideoNode", mvbw18: "VideoNode", mvfw18: "VideoNode", mvbw19: "VideoNode", mvfw19: "VideoNode", mvbw20: "VideoNode", mvfw20: "VideoNode", mvbw21: "VideoNode", mvfw21: "VideoNode", mvbw22: "VideoNode", mvfw22: "VideoNode", mvbw23: "VideoNode", mvfw23: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain24(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", mvbw17: "VideoNode", mvfw17: "VideoNode", mvbw18: "VideoNode", mvfw18: "VideoNode", mvbw19: "VideoNode", mvfw19: "VideoNode", mvbw20: "VideoNode", mvfw20: "VideoNode", mvbw21: "VideoNode", mvfw21: "VideoNode", mvbw22: "VideoNode", mvfw22: "VideoNode", mvbw23: "VideoNode", mvfw23: "VideoNode", mvbw24: "VideoNode", mvfw24: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain3(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain4(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain5(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain6(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain7(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain8(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain9(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Finest(self, super: "VideoNode") -> "VideoNode": ...
    def Flow(self, clip: "VideoNode", super: "VideoNode", vectors: "VideoNode", time: typing.Optional[float] = ..., mode: typing.Optional[int] = ..., fields: typing.Optional[int] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ..., tff: typing.Optional[int] = ...) -> "VideoNode": ...
    def FlowBlur(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", blur: typing.Optional[float] = ..., prec: typing.Optional[int] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def FlowFPS(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", num: typing.Optional[int] = ..., den: typing.Optional[int] = ..., mask: typing.Optional[int] = ..., ml: typing.Optional[float] = ..., blend: typing.Optional[int] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def FlowInter(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", time: typing.Optional[float] = ..., ml: typing.Optional[float] = ..., blend: typing.Optional[int] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Mask(self, clip: "VideoNode", vectors: "VideoNode", ml: typing.Optional[float] = ..., gamma: typing.Optional[float] = ..., kind: typing.Optional[int] = ..., time: typing.Optional[float] = ..., ysc: typing.Optional[float] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Recalculate(self, super: "VideoNode", vectors: "VideoNode", thsad: typing.Optional[float] = ..., smooth: typing.Optional[int] = ..., blksize: typing.Optional[int] = ..., blksizev: typing.Optional[int] = ..., search: typing.Optional[int] = ..., searchparam: typing.Optional[int] = ..., lambda_: typing.Optional[float] = ..., chroma: typing.Optional[int] = ..., truemotion: typing.Optional[int] = ..., pnew: typing.Optional[int] = ..., overlap: typing.Optional[int] = ..., overlapv: typing.Optional[int] = ..., divide: typing.Optional[int] = ..., meander: typing.Optional[int] = ..., fields: typing.Optional[int] = ..., tff: typing.Optional[int] = ..., dct: typing.Optional[int] = ...) -> "VideoNode": ...
    def SCDetection(self, clip: "VideoNode", vectors: "VideoNode", thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Super(self, clip: "VideoNode", hpad: typing.Optional[int] = ..., vpad: typing.Optional[int] = ..., pel: typing.Optional[int] = ..., levels: typing.Optional[int] = ..., chroma: typing.Optional[int] = ..., sharp: typing.Optional[int] = ..., rfilter: typing.Optional[int] = ..., pelclip: typing.Optional["VideoNode"] = ...) -> "VideoNode": ...


class _Plugin_mv_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Analyse(self, super: "VideoNode", blksize: typing.Optional[int] = ..., blksizev: typing.Optional[int] = ..., levels: typing.Optional[int] = ..., search: typing.Optional[int] = ..., searchparam: typing.Optional[int] = ..., pelsearch: typing.Optional[int] = ..., isb: typing.Optional[int] = ..., lambda_: typing.Optional[int] = ..., chroma: typing.Optional[int] = ..., delta: typing.Optional[int] = ..., truemotion: typing.Optional[int] = ..., lsad: typing.Optional[int] = ..., plevel: typing.Optional[int] = ..., global_: typing.Optional[int] = ..., pnew: typing.Optional[int] = ..., pzero: typing.Optional[int] = ..., pglobal: typing.Optional[int] = ..., overlap: typing.Optional[int] = ..., overlapv: typing.Optional[int] = ..., divide: typing.Optional[int] = ..., badsad: typing.Optional[int] = ..., badrange: typing.Optional[int] = ..., opt: typing.Optional[int] = ..., meander: typing.Optional[int] = ..., trymany: typing.Optional[int] = ..., fields: typing.Optional[int] = ..., tff: typing.Optional[int] = ..., search_coarse: typing.Optional[int] = ..., dct: typing.Optional[int] = ...) -> "VideoNode": ...
    def BlockFPS(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", num: typing.Optional[int] = ..., den: typing.Optional[int] = ..., mode: typing.Optional[int] = ..., ml: typing.Optional[float] = ..., blend: typing.Optional[int] = ..., thscd1: typing.Optional[int] = ..., thscd2: typing.Optional[int] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...
    def Compensate(self, clip: "VideoNode", super: "VideoNode", vectors: "VideoNode", scbehavior: typing.Optional[int] = ..., thsad: typing.Optional[int] = ..., fields: typing.Optional[int] = ..., time: typing.Optional[float] = ..., thscd1: typing.Optional[int] = ..., thscd2: typing.Optional[int] = ..., opt: typing.Optional[int] = ..., tff: typing.Optional[int] = ...) -> "VideoNode": ...
    def Degrain1(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", thsad: typing.Optional[int] = ..., thsadc: typing.Optional[int] = ..., plane: typing.Optional[int] = ..., limit: typing.Optional[int] = ..., limitc: typing.Optional[int] = ..., thscd1: typing.Optional[int] = ..., thscd2: typing.Optional[int] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...
    def Degrain2(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", thsad: typing.Optional[int] = ..., thsadc: typing.Optional[int] = ..., plane: typing.Optional[int] = ..., limit: typing.Optional[int] = ..., limitc: typing.Optional[int] = ..., thscd1: typing.Optional[int] = ..., thscd2: typing.Optional[int] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...
    def Degrain3(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", thsad: typing.Optional[int] = ..., thsadc: typing.Optional[int] = ..., plane: typing.Optional[int] = ..., limit: typing.Optional[int] = ..., limitc: typing.Optional[int] = ..., thscd1: typing.Optional[int] = ..., thscd2: typing.Optional[int] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...
    def DepanAnalyse(self, clip: "VideoNode", vectors: "VideoNode", mask: typing.Optional["VideoNode"] = ..., zoom: typing.Optional[int] = ..., rot: typing.Optional[int] = ..., pixaspect: typing.Optional[float] = ..., error: typing.Optional[float] = ..., info: typing.Optional[int] = ..., wrong: typing.Optional[float] = ..., zerow: typing.Optional[float] = ..., thscd1: typing.Optional[int] = ..., thscd2: typing.Optional[int] = ..., fields: typing.Optional[int] = ..., tff: typing.Optional[int] = ...) -> "VideoNode": ...
    def DepanCompensate(self, clip: "VideoNode", data: "VideoNode", offset: typing.Optional[float] = ..., subpixel: typing.Optional[int] = ..., pixaspect: typing.Optional[float] = ..., matchfields: typing.Optional[int] = ..., mirror: typing.Optional[int] = ..., blur: typing.Optional[int] = ..., info: typing.Optional[int] = ..., fields: typing.Optional[int] = ..., tff: typing.Optional[int] = ...) -> "VideoNode": ...
    def DepanEstimate(self, clip: "VideoNode", trust: typing.Optional[float] = ..., winx: typing.Optional[int] = ..., winy: typing.Optional[int] = ..., wleft: typing.Optional[int] = ..., wtop: typing.Optional[int] = ..., dxmax: typing.Optional[int] = ..., dymax: typing.Optional[int] = ..., zoommax: typing.Optional[float] = ..., stab: typing.Optional[float] = ..., pixaspect: typing.Optional[float] = ..., info: typing.Optional[int] = ..., show: typing.Optional[int] = ..., fields: typing.Optional[int] = ..., tff: typing.Optional[int] = ...) -> "VideoNode": ...
    def DepanStabilise(self, clip: "VideoNode", data: "VideoNode", cutoff: typing.Optional[float] = ..., damping: typing.Optional[float] = ..., initzoom: typing.Optional[float] = ..., addzoom: typing.Optional[int] = ..., prev: typing.Optional[int] = ..., next: typing.Optional[int] = ..., mirror: typing.Optional[int] = ..., blur: typing.Optional[int] = ..., dxmax: typing.Optional[float] = ..., dymax: typing.Optional[float] = ..., zoommax: typing.Optional[float] = ..., rotmax: typing.Optional[float] = ..., subpixel: typing.Optional[int] = ..., pixaspect: typing.Optional[float] = ..., fitlast: typing.Optional[int] = ..., tzoom: typing.Optional[float] = ..., info: typing.Optional[int] = ..., method: typing.Optional[int] = ..., fields: typing.Optional[int] = ...) -> "VideoNode": ...
    def Finest(self, super: "VideoNode", opt: typing.Optional[int] = ...) -> "VideoNode": ...
    def Flow(self, clip: "VideoNode", super: "VideoNode", vectors: "VideoNode", time: typing.Optional[float] = ..., mode: typing.Optional[int] = ..., fields: typing.Optional[int] = ..., thscd1: typing.Optional[int] = ..., thscd2: typing.Optional[int] = ..., opt: typing.Optional[int] = ..., tff: typing.Optional[int] = ...) -> "VideoNode": ...
    def FlowBlur(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", blur: typing.Optional[float] = ..., prec: typing.Optional[int] = ..., thscd1: typing.Optional[int] = ..., thscd2: typing.Optional[int] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...
    def FlowFPS(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", num: typing.Optional[int] = ..., den: typing.Optional[int] = ..., mask: typing.Optional[int] = ..., ml: typing.Optional[float] = ..., blend: typing.Optional[int] = ..., thscd1: typing.Optional[int] = ..., thscd2: typing.Optional[int] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...
    def FlowInter(self, clip: "VideoNode", super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", time: typing.Optional[float] = ..., ml: typing.Optional[float] = ..., blend: typing.Optional[int] = ..., thscd1: typing.Optional[int] = ..., thscd2: typing.Optional[int] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...
    def Mask(self, clip: "VideoNode", vectors: "VideoNode", ml: typing.Optional[float] = ..., gamma: typing.Optional[float] = ..., kind: typing.Optional[int] = ..., time: typing.Optional[float] = ..., ysc: typing.Optional[int] = ..., thscd1: typing.Optional[int] = ..., thscd2: typing.Optional[int] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...
    def Recalculate(self, super: "VideoNode", vectors: "VideoNode", thsad: typing.Optional[int] = ..., smooth: typing.Optional[int] = ..., blksize: typing.Optional[int] = ..., blksizev: typing.Optional[int] = ..., search: typing.Optional[int] = ..., searchparam: typing.Optional[int] = ..., lambda_: typing.Optional[int] = ..., chroma: typing.Optional[int] = ..., truemotion: typing.Optional[int] = ..., pnew: typing.Optional[int] = ..., overlap: typing.Optional[int] = ..., overlapv: typing.Optional[int] = ..., divide: typing.Optional[int] = ..., opt: typing.Optional[int] = ..., meander: typing.Optional[int] = ..., fields: typing.Optional[int] = ..., tff: typing.Optional[int] = ..., dct: typing.Optional[int] = ...) -> "VideoNode": ...
    def SCDetection(self, clip: "VideoNode", vectors: "VideoNode", thscd1: typing.Optional[int] = ..., thscd2: typing.Optional[int] = ...) -> "VideoNode": ...
    def Super(self, clip: "VideoNode", hpad: typing.Optional[int] = ..., vpad: typing.Optional[int] = ..., pel: typing.Optional[int] = ..., levels: typing.Optional[int] = ..., chroma: typing.Optional[int] = ..., sharp: typing.Optional[int] = ..., rfilter: typing.Optional[int] = ..., pelclip: typing.Optional["VideoNode"] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_scxvid_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Scxvid(self, clip: "VideoNode", log: typing.Union[str, bytes, bytearray, None] = ..., use_slices: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_tedgemask_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TEdgeMask(self, clip: "VideoNode", threshold: typing.Union[float, typing.Sequence[float], None] = ..., type: typing.Optional[int] = ..., link: typing.Optional[int] = ..., scale: typing.Optional[float] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_tmedian_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TemporalMedian(self, clip: "VideoNode", radius: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...


class _Plugin_tivtc_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TDecimate(self, clip: "VideoNode", mode: typing.Optional[int] = ..., cycleR: typing.Optional[int] = ..., cycle: typing.Optional[int] = ..., rate: typing.Optional[float] = ..., dupThresh: typing.Optional[float] = ..., vidThresh: typing.Optional[float] = ..., sceneThresh: typing.Optional[float] = ..., hybrid: typing.Optional[int] = ..., vidDetect: typing.Optional[int] = ..., conCycle: typing.Optional[int] = ..., conCycleTP: typing.Optional[int] = ..., ovr: typing.Union[str, bytes, bytearray, None] = ..., output: typing.Union[str, bytes, bytearray, None] = ..., input: typing.Union[str, bytes, bytearray, None] = ..., tfmIn: typing.Union[str, bytes, bytearray, None] = ..., mkvOut: typing.Union[str, bytes, bytearray, None] = ..., nt: typing.Optional[int] = ..., blockx: typing.Optional[int] = ..., blocky: typing.Optional[int] = ..., debug: typing.Optional[int] = ..., display: typing.Optional[int] = ..., vfrDec: typing.Optional[int] = ..., batch: typing.Optional[int] = ..., tcfv1: typing.Optional[int] = ..., se: typing.Optional[int] = ..., chroma: typing.Optional[int] = ..., exPP: typing.Optional[int] = ..., maxndl: typing.Optional[int] = ..., m2PA: typing.Optional[int] = ..., denoise: typing.Optional[int] = ..., noblend: typing.Optional[int] = ..., ssd: typing.Optional[int] = ..., hint: typing.Optional[int] = ..., clip2: typing.Optional["VideoNode"] = ..., sdlim: typing.Optional[int] = ..., opt: typing.Optional[int] = ..., orgOut: typing.Union[str, bytes, bytearray, None] = ...) -> "VideoNode": ...
    def TFM(self, clip: "VideoNode", order: typing.Optional[int] = ..., field: typing.Optional[int] = ..., mode: typing.Optional[int] = ..., PP: typing.Optional[int] = ..., ovr: typing.Union[str, bytes, bytearray, None] = ..., input: typing.Union[str, bytes, bytearray, None] = ..., output: typing.Union[str, bytes, bytearray, None] = ..., outputC: typing.Union[str, bytes, bytearray, None] = ..., debug: typing.Optional[int] = ..., display: typing.Optional[int] = ..., slow: typing.Optional[int] = ..., mChroma: typing.Optional[int] = ..., cNum: typing.Optional[int] = ..., cthresh: typing.Optional[int] = ..., MI: typing.Optional[int] = ..., chroma: typing.Optional[int] = ..., blockx: typing.Optional[int] = ..., blocky: typing.Optional[int] = ..., y0: typing.Optional[int] = ..., y1: typing.Optional[int] = ..., mthresh: typing.Optional[int] = ..., clip2: typing.Optional["VideoNode"] = ..., d2v: typing.Union[str, bytes, bytearray, None] = ..., ovrDefault: typing.Optional[int] = ..., flags: typing.Optional[int] = ..., scthresh: typing.Optional[float] = ..., micout: typing.Optional[int] = ..., micmatching: typing.Optional[int] = ..., trimIn: typing.Union[str, bytes, bytearray, None] = ..., hint: typing.Optional[int] = ..., metric: typing.Optional[int] = ..., batch: typing.Optional[int] = ..., ubsco: typing.Optional[int] = ..., mmsco: typing.Optional[int] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_wwxd_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def WWXD(self, clip: "VideoNode") -> "VideoNode": ...


class _Plugin_d2v_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ApplyRFF(self, clip: "VideoNode", d2v: typing.Union[str, bytes, bytearray]) -> "VideoNode": ...
    def Source(self, input: typing.Union[str, bytes, bytearray], threads: typing.Optional[int] = ..., nocrop: typing.Optional[int] = ..., rff: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_svp1_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Analyse(self, clip: "VideoNode", sdata: int, src: "VideoNode", opt: typing.Union[str, bytes, bytearray]) -> "VideoNode": ...
    def Super(self, clip: "VideoNode", opt: typing.Union[str, bytes, bytearray]) -> "VideoNode": ...


class _Plugin_svp2_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def SmoothFps(self, clip: "VideoNode", super: "VideoNode", sdata: int, vectors: "VideoNode", vdata: int, opt: typing.Union[str, bytes, bytearray], src: typing.Optional["VideoNode"] = ..., fps: typing.Optional[float] = ...) -> "VideoNode": ...
    def SmoothFps_NVOF(self, clip: "VideoNode", opt: typing.Union[str, bytes, bytearray], nvof_src: typing.Optional["VideoNode"] = ..., src: typing.Optional["VideoNode"] = ..., fps: typing.Optional[float] = ...) -> "VideoNode": ...


class _Plugin_area_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def AreaResize(self, clip: "VideoNode", width: int, height: int, gamma: typing.Optional[float] = ...) -> "VideoNode": ...


class _Plugin_avs_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def LoadPlugin(self, path: typing.Union[str, bytes, bytearray]) -> "VideoNode": ...


class _Plugin_bm3d_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Basic(self, input: "VideoNode", ref: typing.Optional["VideoNode"] = ..., profile: typing.Union[str, bytes, bytearray, None] = ..., sigma: typing.Union[float, typing.Sequence[float], None] = ..., block_size: typing.Optional[int] = ..., block_step: typing.Optional[int] = ..., group_size: typing.Optional[int] = ..., bm_range: typing.Optional[int] = ..., bm_step: typing.Optional[int] = ..., th_mse: typing.Optional[float] = ..., hard_thr: typing.Optional[float] = ..., matrix: typing.Optional[int] = ...) -> "VideoNode": ...
    def Final(self, input: "VideoNode", ref: "VideoNode", profile: typing.Union[str, bytes, bytearray, None] = ..., sigma: typing.Union[float, typing.Sequence[float], None] = ..., block_size: typing.Optional[int] = ..., block_step: typing.Optional[int] = ..., group_size: typing.Optional[int] = ..., bm_range: typing.Optional[int] = ..., bm_step: typing.Optional[int] = ..., th_mse: typing.Optional[float] = ..., matrix: typing.Optional[int] = ...) -> "VideoNode": ...
    def OPP2RGB(self, input: "VideoNode", sample: typing.Optional[int] = ...) -> "VideoNode": ...
    def RGB2OPP(self, input: "VideoNode", sample: typing.Optional[int] = ...) -> "VideoNode": ...
    def VAggregate(self, input: "VideoNode", radius: typing.Optional[int] = ..., sample: typing.Optional[int] = ...) -> "VideoNode": ...
    def VBasic(self, input: "VideoNode", ref: typing.Optional["VideoNode"] = ..., profile: typing.Union[str, bytes, bytearray, None] = ..., sigma: typing.Union[float, typing.Sequence[float], None] = ..., radius: typing.Optional[int] = ..., block_size: typing.Optional[int] = ..., block_step: typing.Optional[int] = ..., group_size: typing.Optional[int] = ..., bm_range: typing.Optional[int] = ..., bm_step: typing.Optional[int] = ..., ps_num: typing.Optional[int] = ..., ps_range: typing.Optional[int] = ..., ps_step: typing.Optional[int] = ..., th_mse: typing.Optional[float] = ..., hard_thr: typing.Optional[float] = ..., matrix: typing.Optional[int] = ...) -> "VideoNode": ...
    def VFinal(self, input: "VideoNode", ref: "VideoNode", profile: typing.Union[str, bytes, bytearray, None] = ..., sigma: typing.Union[float, typing.Sequence[float], None] = ..., radius: typing.Optional[int] = ..., block_size: typing.Optional[int] = ..., block_step: typing.Optional[int] = ..., group_size: typing.Optional[int] = ..., bm_range: typing.Optional[int] = ..., bm_step: typing.Optional[int] = ..., ps_num: typing.Optional[int] = ..., ps_range: typing.Optional[int] = ..., ps_step: typing.Optional[int] = ..., th_mse: typing.Optional[float] = ..., matrix: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_dgdecodenv_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def DGSource(self, source: typing.Union[str, bytes, bytearray], i420: typing.Optional[int] = ..., deinterlace: typing.Optional[int] = ..., use_top_field: typing.Optional[int] = ..., use_pf: typing.Optional[int] = ..., ct: typing.Optional[int] = ..., cb: typing.Optional[int] = ..., cl: typing.Optional[int] = ..., cr: typing.Optional[int] = ..., rw: typing.Optional[int] = ..., rh: typing.Optional[int] = ..., fieldop: typing.Optional[int] = ..., show: typing.Optional[int] = ..., show2: typing.Union[str, bytes, bytearray, None] = ...) -> "VideoNode": ...


class _Plugin_ffms2_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def GetLogLevel(self) -> "VideoNode": ...
    def Index(self, source: typing.Union[str, bytes, bytearray], cachefile: typing.Union[str, bytes, bytearray, None] = ..., indextracks: typing.Union[int, typing.Sequence[int], None] = ..., errorhandling: typing.Optional[int] = ..., overwrite: typing.Optional[int] = ..., enable_drefs: typing.Optional[int] = ..., use_absolute_path: typing.Optional[int] = ...) -> "VideoNode": ...
    def SetLogLevel(self, level: int) -> "VideoNode": ...
    def Source(self, source: typing.Union[str, bytes, bytearray], track: typing.Optional[int] = ..., cache: typing.Optional[int] = ..., cachefile: typing.Union[str, bytes, bytearray, None] = ..., fpsnum: typing.Optional[int] = ..., fpsden: typing.Optional[int] = ..., threads: typing.Optional[int] = ..., timecodes: typing.Union[str, bytes, bytearray, None] = ..., seekmode: typing.Optional[int] = ..., width: typing.Optional[int] = ..., height: typing.Optional[int] = ..., resizer: typing.Union[str, bytes, bytearray, None] = ..., format: typing.Optional[int] = ..., alpha: typing.Optional[int] = ...) -> "VideoNode": ...
    def Version(self) -> "VideoNode": ...


class _Plugin_hqdn3d_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Hqdn3d(self, clip: "VideoNode", lum_spac: typing.Optional[float] = ..., chrom_spac: typing.Optional[float] = ..., lum_tmp: typing.Optional[float] = ..., chrom_tmp: typing.Optional[float] = ..., restart_lap: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_imwri_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Read(self, filename: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]]], firstnum: typing.Optional[int] = ..., mismatch: typing.Optional[int] = ..., alpha: typing.Optional[int] = ..., float_output: typing.Optional[int] = ..., embed_icc: typing.Optional[int] = ...) -> "VideoNode": ...
    def Write(self, clip: "VideoNode", imgformat: typing.Union[str, bytes, bytearray], filename: typing.Union[str, bytes, bytearray], firstnum: typing.Optional[int] = ..., quality: typing.Optional[int] = ..., dither: typing.Optional[int] = ..., compression_type: typing.Union[str, bytes, bytearray, None] = ..., overwrite: typing.Optional[int] = ..., alpha: typing.Optional["VideoNode"] = ...) -> "VideoNode": ...


class _Plugin_jinc_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def JincResize(self, clip: "VideoNode", width: int, height: int, tap: typing.Optional[int] = ..., src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ..., src_width: typing.Optional[float] = ..., src_height: typing.Optional[float] = ..., quant_x: typing.Optional[int] = ..., quant_y: typing.Optional[int] = ..., blur: typing.Optional[float] = ...) -> "VideoNode": ...


class _Plugin_rsnv_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def RealSR(self, clip: "VideoNode", scale: typing.Optional[int] = ..., tilesize_x: typing.Optional[int] = ..., tilesize_y: typing.Optional[int] = ..., gpu_id: typing.Optional[int] = ..., gpu_thread: typing.Optional[int] = ..., tta: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_rgsf_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def BackwardClense(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def Clense(self, clip: "VideoNode", previous: typing.Optional["VideoNode"] = ..., next: typing.Optional["VideoNode"] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def ForwardClense(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def RemoveGrain(self, clip: "VideoNode", mode: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def Repair(self, clip: "VideoNode", repairclip: "VideoNode", mode: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def VerticalCleaner(self, clip: "VideoNode", mode: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...


class _Plugin_rgvs_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def BackwardClense(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def Clense(self, clip: "VideoNode", previous: typing.Optional["VideoNode"] = ..., next: typing.Optional["VideoNode"] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def ForwardClense(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def RemoveGrain(self, clip: "VideoNode", mode: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def Repair(self, clip: "VideoNode", repairclip: "VideoNode", mode: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def VerticalCleaner(self, clip: "VideoNode", mode: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...


class _Plugin_resize_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Bicubic(self, clip: "VideoNode", width: typing.Optional[int] = ..., height: typing.Optional[int] = ..., format: typing.Optional[int] = ..., matrix: typing.Optional[int] = ..., matrix_s: typing.Union[str, bytes, bytearray, None] = ..., transfer: typing.Optional[int] = ..., transfer_s: typing.Union[str, bytes, bytearray, None] = ..., primaries: typing.Optional[int] = ..., primaries_s: typing.Union[str, bytes, bytearray, None] = ..., range: typing.Optional[int] = ..., range_s: typing.Union[str, bytes, bytearray, None] = ..., chromaloc: typing.Optional[int] = ..., chromaloc_s: typing.Union[str, bytes, bytearray, None] = ..., matrix_in: typing.Optional[int] = ..., matrix_in_s: typing.Union[str, bytes, bytearray, None] = ..., transfer_in: typing.Optional[int] = ..., transfer_in_s: typing.Union[str, bytes, bytearray, None] = ..., primaries_in: typing.Optional[int] = ..., primaries_in_s: typing.Union[str, bytes, bytearray, None] = ..., range_in: typing.Optional[int] = ..., range_in_s: typing.Union[str, bytes, bytearray, None] = ..., chromaloc_in: typing.Optional[int] = ..., chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = ..., filter_param_a: typing.Optional[float] = ..., filter_param_b: typing.Optional[float] = ..., resample_filter_uv: typing.Union[str, bytes, bytearray, None] = ..., filter_param_a_uv: typing.Optional[float] = ..., filter_param_b_uv: typing.Optional[float] = ..., dither_type: typing.Union[str, bytes, bytearray, None] = ..., cpu_type: typing.Union[str, bytes, bytearray, None] = ..., prefer_props: typing.Optional[int] = ..., src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ..., src_width: typing.Optional[float] = ..., src_height: typing.Optional[float] = ..., nominal_luminance: typing.Optional[float] = ...) -> "VideoNode": ...
    def Bilinear(self, clip: "VideoNode", width: typing.Optional[int] = ..., height: typing.Optional[int] = ..., format: typing.Optional[int] = ..., matrix: typing.Optional[int] = ..., matrix_s: typing.Union[str, bytes, bytearray, None] = ..., transfer: typing.Optional[int] = ..., transfer_s: typing.Union[str, bytes, bytearray, None] = ..., primaries: typing.Optional[int] = ..., primaries_s: typing.Union[str, bytes, bytearray, None] = ..., range: typing.Optional[int] = ..., range_s: typing.Union[str, bytes, bytearray, None] = ..., chromaloc: typing.Optional[int] = ..., chromaloc_s: typing.Union[str, bytes, bytearray, None] = ..., matrix_in: typing.Optional[int] = ..., matrix_in_s: typing.Union[str, bytes, bytearray, None] = ..., transfer_in: typing.Optional[int] = ..., transfer_in_s: typing.Union[str, bytes, bytearray, None] = ..., primaries_in: typing.Optional[int] = ..., primaries_in_s: typing.Union[str, bytes, bytearray, None] = ..., range_in: typing.Optional[int] = ..., range_in_s: typing.Union[str, bytes, bytearray, None] = ..., chromaloc_in: typing.Optional[int] = ..., chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = ..., filter_param_a: typing.Optional[float] = ..., filter_param_b: typing.Optional[float] = ..., resample_filter_uv: typing.Union[str, bytes, bytearray, None] = ..., filter_param_a_uv: typing.Optional[float] = ..., filter_param_b_uv: typing.Optional[float] = ..., dither_type: typing.Union[str, bytes, bytearray, None] = ..., cpu_type: typing.Union[str, bytes, bytearray, None] = ..., prefer_props: typing.Optional[int] = ..., src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ..., src_width: typing.Optional[float] = ..., src_height: typing.Optional[float] = ..., nominal_luminance: typing.Optional[float] = ...) -> "VideoNode": ...
    def Lanczos(self, clip: "VideoNode", width: typing.Optional[int] = ..., height: typing.Optional[int] = ..., format: typing.Optional[int] = ..., matrix: typing.Optional[int] = ..., matrix_s: typing.Union[str, bytes, bytearray, None] = ..., transfer: typing.Optional[int] = ..., transfer_s: typing.Union[str, bytes, bytearray, None] = ..., primaries: typing.Optional[int] = ..., primaries_s: typing.Union[str, bytes, bytearray, None] = ..., range: typing.Optional[int] = ..., range_s: typing.Union[str, bytes, bytearray, None] = ..., chromaloc: typing.Optional[int] = ..., chromaloc_s: typing.Union[str, bytes, bytearray, None] = ..., matrix_in: typing.Optional[int] = ..., matrix_in_s: typing.Union[str, bytes, bytearray, None] = ..., transfer_in: typing.Optional[int] = ..., transfer_in_s: typing.Union[str, bytes, bytearray, None] = ..., primaries_in: typing.Optional[int] = ..., primaries_in_s: typing.Union[str, bytes, bytearray, None] = ..., range_in: typing.Optional[int] = ..., range_in_s: typing.Union[str, bytes, bytearray, None] = ..., chromaloc_in: typing.Optional[int] = ..., chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = ..., filter_param_a: typing.Optional[float] = ..., filter_param_b: typing.Optional[float] = ..., resample_filter_uv: typing.Union[str, bytes, bytearray, None] = ..., filter_param_a_uv: typing.Optional[float] = ..., filter_param_b_uv: typing.Optional[float] = ..., dither_type: typing.Union[str, bytes, bytearray, None] = ..., cpu_type: typing.Union[str, bytes, bytearray, None] = ..., prefer_props: typing.Optional[int] = ..., src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ..., src_width: typing.Optional[float] = ..., src_height: typing.Optional[float] = ..., nominal_luminance: typing.Optional[float] = ...) -> "VideoNode": ...
    def Point(self, clip: "VideoNode", width: typing.Optional[int] = ..., height: typing.Optional[int] = ..., format: typing.Optional[int] = ..., matrix: typing.Optional[int] = ..., matrix_s: typing.Union[str, bytes, bytearray, None] = ..., transfer: typing.Optional[int] = ..., transfer_s: typing.Union[str, bytes, bytearray, None] = ..., primaries: typing.Optional[int] = ..., primaries_s: typing.Union[str, bytes, bytearray, None] = ..., range: typing.Optional[int] = ..., range_s: typing.Union[str, bytes, bytearray, None] = ..., chromaloc: typing.Optional[int] = ..., chromaloc_s: typing.Union[str, bytes, bytearray, None] = ..., matrix_in: typing.Optional[int] = ..., matrix_in_s: typing.Union[str, bytes, bytearray, None] = ..., transfer_in: typing.Optional[int] = ..., transfer_in_s: typing.Union[str, bytes, bytearray, None] = ..., primaries_in: typing.Optional[int] = ..., primaries_in_s: typing.Union[str, bytes, bytearray, None] = ..., range_in: typing.Optional[int] = ..., range_in_s: typing.Union[str, bytes, bytearray, None] = ..., chromaloc_in: typing.Optional[int] = ..., chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = ..., filter_param_a: typing.Optional[float] = ..., filter_param_b: typing.Optional[float] = ..., resample_filter_uv: typing.Union[str, bytes, bytearray, None] = ..., filter_param_a_uv: typing.Optional[float] = ..., filter_param_b_uv: typing.Optional[float] = ..., dither_type: typing.Union[str, bytes, bytearray, None] = ..., cpu_type: typing.Union[str, bytes, bytearray, None] = ..., prefer_props: typing.Optional[int] = ..., src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ..., src_width: typing.Optional[float] = ..., src_height: typing.Optional[float] = ..., nominal_luminance: typing.Optional[float] = ...) -> "VideoNode": ...
    def Spline16(self, clip: "VideoNode", width: typing.Optional[int] = ..., height: typing.Optional[int] = ..., format: typing.Optional[int] = ..., matrix: typing.Optional[int] = ..., matrix_s: typing.Union[str, bytes, bytearray, None] = ..., transfer: typing.Optional[int] = ..., transfer_s: typing.Union[str, bytes, bytearray, None] = ..., primaries: typing.Optional[int] = ..., primaries_s: typing.Union[str, bytes, bytearray, None] = ..., range: typing.Optional[int] = ..., range_s: typing.Union[str, bytes, bytearray, None] = ..., chromaloc: typing.Optional[int] = ..., chromaloc_s: typing.Union[str, bytes, bytearray, None] = ..., matrix_in: typing.Optional[int] = ..., matrix_in_s: typing.Union[str, bytes, bytearray, None] = ..., transfer_in: typing.Optional[int] = ..., transfer_in_s: typing.Union[str, bytes, bytearray, None] = ..., primaries_in: typing.Optional[int] = ..., primaries_in_s: typing.Union[str, bytes, bytearray, None] = ..., range_in: typing.Optional[int] = ..., range_in_s: typing.Union[str, bytes, bytearray, None] = ..., chromaloc_in: typing.Optional[int] = ..., chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = ..., filter_param_a: typing.Optional[float] = ..., filter_param_b: typing.Optional[float] = ..., resample_filter_uv: typing.Union[str, bytes, bytearray, None] = ..., filter_param_a_uv: typing.Optional[float] = ..., filter_param_b_uv: typing.Optional[float] = ..., dither_type: typing.Union[str, bytes, bytearray, None] = ..., cpu_type: typing.Union[str, bytes, bytearray, None] = ..., prefer_props: typing.Optional[int] = ..., src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ..., src_width: typing.Optional[float] = ..., src_height: typing.Optional[float] = ..., nominal_luminance: typing.Optional[float] = ...) -> "VideoNode": ...
    def Spline36(self, clip: "VideoNode", width: typing.Optional[int] = ..., height: typing.Optional[int] = ..., format: typing.Optional[int] = ..., matrix: typing.Optional[int] = ..., matrix_s: typing.Union[str, bytes, bytearray, None] = ..., transfer: typing.Optional[int] = ..., transfer_s: typing.Union[str, bytes, bytearray, None] = ..., primaries: typing.Optional[int] = ..., primaries_s: typing.Union[str, bytes, bytearray, None] = ..., range: typing.Optional[int] = ..., range_s: typing.Union[str, bytes, bytearray, None] = ..., chromaloc: typing.Optional[int] = ..., chromaloc_s: typing.Union[str, bytes, bytearray, None] = ..., matrix_in: typing.Optional[int] = ..., matrix_in_s: typing.Union[str, bytes, bytearray, None] = ..., transfer_in: typing.Optional[int] = ..., transfer_in_s: typing.Union[str, bytes, bytearray, None] = ..., primaries_in: typing.Optional[int] = ..., primaries_in_s: typing.Union[str, bytes, bytearray, None] = ..., range_in: typing.Optional[int] = ..., range_in_s: typing.Union[str, bytes, bytearray, None] = ..., chromaloc_in: typing.Optional[int] = ..., chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = ..., filter_param_a: typing.Optional[float] = ..., filter_param_b: typing.Optional[float] = ..., resample_filter_uv: typing.Union[str, bytes, bytearray, None] = ..., filter_param_a_uv: typing.Optional[float] = ..., filter_param_b_uv: typing.Optional[float] = ..., dither_type: typing.Union[str, bytes, bytearray, None] = ..., cpu_type: typing.Union[str, bytes, bytearray, None] = ..., prefer_props: typing.Optional[int] = ..., src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ..., src_width: typing.Optional[float] = ..., src_height: typing.Optional[float] = ..., nominal_luminance: typing.Optional[float] = ...) -> "VideoNode": ...
    def Spline64(self, clip: "VideoNode", width: typing.Optional[int] = ..., height: typing.Optional[int] = ..., format: typing.Optional[int] = ..., matrix: typing.Optional[int] = ..., matrix_s: typing.Union[str, bytes, bytearray, None] = ..., transfer: typing.Optional[int] = ..., transfer_s: typing.Union[str, bytes, bytearray, None] = ..., primaries: typing.Optional[int] = ..., primaries_s: typing.Union[str, bytes, bytearray, None] = ..., range: typing.Optional[int] = ..., range_s: typing.Union[str, bytes, bytearray, None] = ..., chromaloc: typing.Optional[int] = ..., chromaloc_s: typing.Union[str, bytes, bytearray, None] = ..., matrix_in: typing.Optional[int] = ..., matrix_in_s: typing.Union[str, bytes, bytearray, None] = ..., transfer_in: typing.Optional[int] = ..., transfer_in_s: typing.Union[str, bytes, bytearray, None] = ..., primaries_in: typing.Optional[int] = ..., primaries_in_s: typing.Union[str, bytes, bytearray, None] = ..., range_in: typing.Optional[int] = ..., range_in_s: typing.Union[str, bytes, bytearray, None] = ..., chromaloc_in: typing.Optional[int] = ..., chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = ..., filter_param_a: typing.Optional[float] = ..., filter_param_b: typing.Optional[float] = ..., resample_filter_uv: typing.Union[str, bytes, bytearray, None] = ..., filter_param_a_uv: typing.Optional[float] = ..., filter_param_b_uv: typing.Optional[float] = ..., dither_type: typing.Union[str, bytes, bytearray, None] = ..., cpu_type: typing.Union[str, bytes, bytearray, None] = ..., prefer_props: typing.Optional[int] = ..., src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ..., src_width: typing.Optional[float] = ..., src_height: typing.Optional[float] = ..., nominal_luminance: typing.Optional[float] = ...) -> "VideoNode": ...


class _Plugin_retinex_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def MSRCP(self, input: "VideoNode", sigma: typing.Union[float, typing.Sequence[float], None] = ..., lower_thr: typing.Optional[float] = ..., upper_thr: typing.Optional[float] = ..., fulls: typing.Optional[int] = ..., fulld: typing.Optional[int] = ..., chroma_protect: typing.Optional[float] = ...) -> "VideoNode": ...
    def MSRCR(self, input: "VideoNode", sigma: typing.Union[float, typing.Sequence[float], None] = ..., lower_thr: typing.Optional[float] = ..., upper_thr: typing.Optional[float] = ..., fulls: typing.Optional[int] = ..., fulld: typing.Optional[int] = ..., restore: typing.Optional[float] = ...) -> "VideoNode": ...


class _Plugin_srmdnv_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def SRMD(self, clip: "VideoNode", scale: typing.Optional[int] = ..., noise: typing.Optional[int] = ..., tilesize_x: typing.Optional[int] = ..., tilesize_y: typing.Optional[int] = ..., gpu_id: typing.Optional[int] = ..., gpu_thread: typing.Optional[int] = ..., tta: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_std_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def AddBorders(self, clip: "VideoNode", left: typing.Optional[int] = ..., right: typing.Optional[int] = ..., top: typing.Optional[int] = ..., bottom: typing.Optional[int] = ..., color: typing.Union[float, typing.Sequence[float], None] = ...) -> "VideoNode": ...
    def AssumeFPS(self, clip: "VideoNode", src: typing.Optional["VideoNode"] = ..., fpsnum: typing.Optional[int] = ..., fpsden: typing.Optional[int] = ...) -> "VideoNode": ...
    def AssumeSampleRate(self, clip: "AudioNode", src: typing.Optional["AudioNode"] = ..., samplerate: typing.Optional[int] = ...) -> "VideoNode": ...
    def AudioGain(self, clip: "AudioNode", gain: typing.Union[float, typing.Sequence[float], None] = ...) -> "VideoNode": ...
    def AudioLoop(self, clip: "AudioNode", times: typing.Optional[int] = ...) -> "VideoNode": ...
    def AudioMix(self, clips: typing.Union["AudioNode", typing.Sequence["AudioNode"]], matrix: typing.Union[float, typing.Sequence[float]], channels_out: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def AudioReverse(self, clip: "AudioNode") -> "VideoNode": ...
    def AudioSplice(self, clips: typing.Union["AudioNode", typing.Sequence["AudioNode"]]) -> "VideoNode": ...
    def AudioTrim(self, clip: "AudioNode", first: typing.Optional[int] = ..., last: typing.Optional[int] = ..., length: typing.Optional[int] = ...) -> "VideoNode": ...
    def AverageFrames(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]], weights: typing.Union[float, typing.Sequence[float]], scale: typing.Optional[float] = ..., scenechange: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def Binarize(self, clip: "VideoNode", threshold: typing.Union[float, typing.Sequence[float], None] = ..., v0: typing.Union[float, typing.Sequence[float], None] = ..., v1: typing.Union[float, typing.Sequence[float], None] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def BinarizeMask(self, clip: "VideoNode", threshold: typing.Union[float, typing.Sequence[float], None] = ..., v0: typing.Union[float, typing.Sequence[float], None] = ..., v1: typing.Union[float, typing.Sequence[float], None] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def BlankAudio(self, clip: typing.Optional["AudioNode"] = ..., channels: typing.Optional[int] = ..., bits: typing.Optional[int] = ..., sampletype: typing.Optional[int] = ..., samplerate: typing.Optional[int] = ..., length: typing.Optional[int] = ..., keep: typing.Optional[int] = ...) -> "VideoNode": ...
    def BlankClip(self, clip: typing.Optional["VideoNode"] = ..., width: typing.Optional[int] = ..., height: typing.Optional[int] = ..., format: typing.Optional[int] = ..., length: typing.Optional[int] = ..., fpsnum: typing.Optional[int] = ..., fpsden: typing.Optional[int] = ..., color: typing.Union[float, typing.Sequence[float], None] = ..., keep: typing.Optional[int] = ...) -> "VideoNode": ...
    def BoxBlur(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = ..., hradius: typing.Optional[int] = ..., hpasses: typing.Optional[int] = ..., vradius: typing.Optional[int] = ..., vpasses: typing.Optional[int] = ...) -> "VideoNode": ...
    def Cache(self, clip: "VideoNode", size: typing.Optional[int] = ..., fixed: typing.Optional[int] = ..., make_linear: typing.Optional[int] = ...) -> "VideoNode": ...
    def ClipToProp(self, clip: "VideoNode", mclip: "VideoNode", prop: typing.Union[str, bytes, bytearray, None] = ...) -> "VideoNode": ...
    def Convolution(self, clip: "VideoNode", matrix: typing.Union[float, typing.Sequence[float]], bias: typing.Optional[float] = ..., divisor: typing.Optional[float] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., saturate: typing.Optional[int] = ..., mode: typing.Union[str, bytes, bytearray, None] = ...) -> "VideoNode": ...
    def CopyFrameProps(self, clip: "VideoNode", prop_src: "VideoNode") -> "VideoNode": ...
    def Crop(self, clip: "VideoNode", left: typing.Optional[int] = ..., right: typing.Optional[int] = ..., top: typing.Optional[int] = ..., bottom: typing.Optional[int] = ...) -> "VideoNode": ...
    def CropAbs(self, clip: "VideoNode", width: int, height: int, left: typing.Optional[int] = ..., top: typing.Optional[int] = ..., x: typing.Optional[int] = ..., y: typing.Optional[int] = ...) -> "VideoNode": ...
    def CropRel(self, clip: "VideoNode", left: typing.Optional[int] = ..., right: typing.Optional[int] = ..., top: typing.Optional[int] = ..., bottom: typing.Optional[int] = ...) -> "VideoNode": ...
    def Deflate(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = ..., threshold: typing.Optional[float] = ...) -> "VideoNode": ...
    def DeleteFrames(self, clip: "VideoNode", frames: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def DoubleWeave(self, clip: "VideoNode", tff: typing.Optional[int] = ...) -> "VideoNode": ...
    def DuplicateFrames(self, clip: "VideoNode", frames: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def Expr(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]], expr: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]]], format: typing.Optional[int] = ...) -> "VideoNode": ...
    def FlipHorizontal(self, clip: "VideoNode") -> "VideoNode": ...
    def FlipVertical(self, clip: "VideoNode") -> "VideoNode": ...
    def FrameEval(self, clip: "VideoNode", eval: typing.Callable[..., typing.Any], prop_src: typing.Union["VideoNode", typing.Sequence["VideoNode"], None] = ..., clip_src: typing.Union["VideoNode", typing.Sequence["VideoNode"], None] = ...) -> "VideoNode": ...
    def FreezeFrames(self, clip: "VideoNode", first: typing.Union[int, typing.Sequence[int]], last: typing.Union[int, typing.Sequence[int]], replacement: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def Inflate(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = ..., threshold: typing.Optional[float] = ...) -> "VideoNode": ...
    def Interleave(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]], extend: typing.Optional[int] = ..., mismatch: typing.Optional[int] = ..., modify_duration: typing.Optional[int] = ...) -> "VideoNode": ...
    def Invert(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def InvertMask(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def Levels(self, clip: "VideoNode", min_in: typing.Union[float, typing.Sequence[float], None] = ..., max_in: typing.Union[float, typing.Sequence[float], None] = ..., gamma: typing.Union[float, typing.Sequence[float], None] = ..., min_out: typing.Union[float, typing.Sequence[float], None] = ..., max_out: typing.Union[float, typing.Sequence[float], None] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def Limiter(self, clip: "VideoNode", min: typing.Union[float, typing.Sequence[float], None] = ..., max: typing.Union[float, typing.Sequence[float], None] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def LoadAllPlugins(self, path: typing.Union[str, bytes, bytearray]) -> "VideoNode": ...
    def LoadPlugin(self, path: typing.Union[str, bytes, bytearray], altsearchpath: typing.Optional[int] = ..., forcens: typing.Union[str, bytes, bytearray, None] = ..., forceid: typing.Union[str, bytes, bytearray, None] = ...) -> "VideoNode": ...
    def Loop(self, clip: "VideoNode", times: typing.Optional[int] = ...) -> "VideoNode": ...
    def Lut(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = ..., lut: typing.Union[int, typing.Sequence[int], None] = ..., lutf: typing.Union[float, typing.Sequence[float], None] = ..., function: typing.Optional[typing.Callable[..., typing.Any]] = ..., bits: typing.Optional[int] = ..., floatout: typing.Optional[int] = ...) -> "VideoNode": ...
    def Lut2(self, clipa: "VideoNode", clipb: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = ..., lut: typing.Union[int, typing.Sequence[int], None] = ..., lutf: typing.Union[float, typing.Sequence[float], None] = ..., function: typing.Optional[typing.Callable[..., typing.Any]] = ..., bits: typing.Optional[int] = ..., floatout: typing.Optional[int] = ...) -> "VideoNode": ...
    def MakeDiff(self, clipa: "VideoNode", clipb: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def MaskedMerge(self, clipa: "VideoNode", clipb: "VideoNode", mask: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = ..., first_plane: typing.Optional[int] = ..., premultiplied: typing.Optional[int] = ...) -> "VideoNode": ...
    def Maximum(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = ..., threshold: typing.Optional[float] = ..., coordinates: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def Median(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def Merge(self, clipa: "VideoNode", clipb: "VideoNode", weight: typing.Union[float, typing.Sequence[float], None] = ...) -> "VideoNode": ...
    def MergeDiff(self, clipa: "VideoNode", clipb: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def Minimum(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = ..., threshold: typing.Optional[float] = ..., coordinates: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def ModifyFrame(self, clip: "VideoNode", clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]], selector: typing.Callable[..., typing.Any]) -> "VideoNode": ...
    def PEMVerifier(self, clip: "VideoNode", upper: typing.Union[float, typing.Sequence[float], None] = ..., lower: typing.Union[float, typing.Sequence[float], None] = ...) -> "VideoNode": ...
    def PlaneStats(self, clipa: "VideoNode", clipb: typing.Optional["VideoNode"] = ..., plane: typing.Optional[int] = ..., prop: typing.Union[str, bytes, bytearray, None] = ...) -> "VideoNode": ...
    def PreMultiply(self, clip: "VideoNode", alpha: "VideoNode") -> "VideoNode": ...
    def Prewitt(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = ..., scale: typing.Optional[float] = ...) -> "VideoNode": ...
    def PropToClip(self, clip: "VideoNode", prop: typing.Union[str, bytes, bytearray, None] = ...) -> "VideoNode": ...
    def RemoveFrameProps(self, clip: "VideoNode", props: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = ...) -> "VideoNode": ...
    def Reverse(self, clip: "VideoNode") -> "VideoNode": ...
    def SelectEvery(self, clip: "VideoNode", cycle: int, offsets: typing.Union[int, typing.Sequence[int]], modify_duration: typing.Optional[int] = ...) -> "VideoNode": ...
    def SeparateFields(self, clip: "VideoNode", tff: typing.Optional[int] = ..., modify_duration: typing.Optional[int] = ...) -> "VideoNode": ...
    def SetAudioCache(self, clip: "AudioNode", mode: typing.Optional[int] = ..., fixedsize: typing.Optional[int] = ..., maxsize: typing.Optional[int] = ..., maxhistory: typing.Optional[int] = ...) -> "VideoNode": ...
    def SetFieldBased(self, clip: "VideoNode", value: int) -> "VideoNode": ...
    def SetFrameProp(self, clip: "VideoNode", prop: typing.Union[str, bytes, bytearray], intval: typing.Union[int, typing.Sequence[int], None] = ..., floatval: typing.Union[float, typing.Sequence[float], None] = ..., data: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = ...) -> "VideoNode": ...
    def SetFrameProps(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Optional["VideoNode"]: ...
    def SetMaxCPU(self, cpu: typing.Union[str, bytes, bytearray]) -> "VideoNode": ...
    def SetVideoCache(self, clip: "VideoNode", mode: typing.Optional[int] = ..., fixedsize: typing.Optional[int] = ..., maxsize: typing.Optional[int] = ..., maxhistory: typing.Optional[int] = ...) -> "VideoNode": ...
    def ShuffleChannels(self, clips: typing.Union["AudioNode", typing.Sequence["AudioNode"]], channels_in: typing.Union[int, typing.Sequence[int]], channels_out: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def ShufflePlanes(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]], planes: typing.Union[int, typing.Sequence[int]], colorfamily: int) -> "VideoNode": ...
    def Sobel(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = ..., scale: typing.Optional[float] = ...) -> "VideoNode": ...
    def Splice(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]], mismatch: typing.Optional[int] = ...) -> "VideoNode": ...
    def SplitChannels(self, clip: "AudioNode") -> "VideoNode": ...
    def SplitPlanes(self, clip: "VideoNode") -> "VideoNode": ...
    def StackHorizontal(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]]) -> "VideoNode": ...
    def StackVertical(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]]) -> "VideoNode": ...
    def TestAudio(self, channels: typing.Optional[int] = ..., bits: typing.Optional[int] = ..., isfloat: typing.Optional[int] = ..., samplerate: typing.Optional[int] = ..., length: typing.Optional[int] = ...) -> "VideoNode": ...
    def Transpose(self, clip: "VideoNode") -> "VideoNode": ...
    def Trim(self, clip: "VideoNode", first: typing.Optional[int] = ..., last: typing.Optional[int] = ..., length: typing.Optional[int] = ...) -> "VideoNode": ...
    def Turn180(self, clip: "VideoNode") -> "VideoNode": ...


class _Plugin_text_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ClipInfo(self, clip: "VideoNode", alignment: typing.Optional[int] = ..., scale: typing.Optional[int] = ...) -> "VideoNode": ...
    def CoreInfo(self, clip: typing.Optional["VideoNode"] = ..., alignment: typing.Optional[int] = ..., scale: typing.Optional[int] = ...) -> "VideoNode": ...
    def FrameNum(self, clip: "VideoNode", alignment: typing.Optional[int] = ..., scale: typing.Optional[int] = ...) -> "VideoNode": ...
    def FrameProps(self, clip: "VideoNode", props: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = ..., alignment: typing.Optional[int] = ..., scale: typing.Optional[int] = ...) -> "VideoNode": ...
    def Text(self, clip: "VideoNode", text: typing.Union[str, bytes, bytearray], alignment: typing.Optional[int] = ..., scale: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_placebo_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Deband(self, clip: "VideoNode", planes: typing.Optional[int] = ..., iterations: typing.Optional[int] = ..., threshold: typing.Optional[float] = ..., radius: typing.Optional[float] = ..., grain: typing.Optional[float] = ..., dither: typing.Optional[int] = ..., dither_algo: typing.Optional[int] = ..., renderer_api: typing.Optional[int] = ...) -> "VideoNode": ...
    def Resample(self, clip: "VideoNode", width: int, height: int, filter: typing.Union[str, bytes, bytearray, None] = ..., clamp: typing.Optional[float] = ..., blur: typing.Optional[float] = ..., taper: typing.Optional[float] = ..., radius: typing.Optional[float] = ..., param1: typing.Optional[float] = ..., param2: typing.Optional[float] = ..., sx: typing.Optional[float] = ..., sy: typing.Optional[float] = ..., antiring: typing.Optional[float] = ..., lut_entries: typing.Optional[int] = ..., cutoff: typing.Optional[float] = ..., sigmoidize: typing.Optional[int] = ..., sigmoid_center: typing.Optional[float] = ..., sigmoid_slope: typing.Optional[float] = ..., linearize: typing.Optional[int] = ..., trc: typing.Optional[int] = ...) -> "VideoNode": ...
    def Shader(self, clip: "VideoNode", shader: typing.Union[str, bytes, bytearray], width: typing.Optional[int] = ..., height: typing.Optional[int] = ..., chroma_loc: typing.Optional[int] = ..., matrix: typing.Optional[int] = ..., trc: typing.Optional[int] = ..., linearize: typing.Optional[int] = ..., sigmoidize: typing.Optional[int] = ..., sigmoid_center: typing.Optional[float] = ..., sigmoid_slope: typing.Optional[float] = ..., lut_entries: typing.Optional[int] = ..., antiring: typing.Optional[float] = ..., filter: typing.Union[str, bytes, bytearray, None] = ..., clamp: typing.Optional[float] = ..., blur: typing.Optional[float] = ..., taper: typing.Optional[float] = ..., radius: typing.Optional[float] = ..., param1: typing.Optional[float] = ..., param2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Tonemap(self, clip: "VideoNode", srcp: typing.Optional[int] = ..., srct: typing.Optional[int] = ..., srcl: typing.Optional[int] = ..., src_peak: typing.Optional[float] = ..., src_avg: typing.Optional[float] = ..., src_scale: typing.Optional[float] = ..., dstp: typing.Optional[int] = ..., dstt: typing.Optional[int] = ..., dstl: typing.Optional[int] = ..., dst_peak: typing.Optional[float] = ..., dst_avg: typing.Optional[float] = ..., dst_scale: typing.Optional[float] = ..., dynamic_peak_detection: typing.Optional[int] = ..., smoothing_period: typing.Optional[float] = ..., scene_threshold_low: typing.Optional[float] = ..., scene_threshold_high: typing.Optional[float] = ..., intent: typing.Optional[int] = ..., tone_mapping_algo: typing.Optional[int] = ..., tone_mapping_param: typing.Optional[float] = ..., desaturation_strength: typing.Optional[float] = ..., desaturation_exponent: typing.Optional[float] = ..., desaturation_base: typing.Optional[float] = ..., max_boost: typing.Optional[float] = ..., gamut_warning: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_bm3dcuda_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def BM3D(self, clip: "VideoNode", ref: typing.Optional["VideoNode"] = ..., sigma: typing.Union[float, typing.Sequence[float], None] = ..., block_step: typing.Union[int, typing.Sequence[int], None] = ..., bm_range: typing.Union[int, typing.Sequence[int], None] = ..., radius: typing.Optional[int] = ..., ps_num: typing.Union[int, typing.Sequence[int], None] = ..., ps_range: typing.Union[int, typing.Sequence[int], None] = ..., chroma: typing.Optional[int] = ..., device_id: typing.Optional[int] = ..., fast: typing.Optional[int] = ..., extractor_exp: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_dpid_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Dpid(self, clip: "VideoNode", width: typing.Optional[int] = ..., height: typing.Optional[int] = ..., lambda_: typing.Union[float, typing.Sequence[float], None] = ..., src_left: typing.Union[float, typing.Sequence[float], None] = ..., src_top: typing.Union[float, typing.Sequence[float], None] = ..., read_chromaloc: typing.Optional[int] = ...) -> "VideoNode": ...
    def DpidRaw(self, clip: "VideoNode", clip2: "VideoNode", lambda_: typing.Union[float, typing.Sequence[float], None] = ..., src_left: typing.Union[float, typing.Sequence[float], None] = ..., src_top: typing.Union[float, typing.Sequence[float], None] = ..., read_chromaloc: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...


class _Plugin_tla_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TempLinearApproximate(self, clip: "VideoNode", radius: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., gamma: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_dpriv_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Reconstruct(self, input: "VideoNode", stats: "VideoNode", radius: int, speed: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_average_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Mean(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"], None] = ..., preset: typing.Optional[int] = ..., discard: typing.Optional[int] = ...) -> "VideoNode": ...
    def Median(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"], None] = ...) -> "VideoNode": ...


class _Plugin_fmtc_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def bitdepth(self, clip: "VideoNode", csp: typing.Optional[int] = ..., bits: typing.Optional[int] = ..., flt: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., fulls: typing.Optional[int] = ..., fulld: typing.Optional[int] = ..., dmode: typing.Optional[int] = ..., ampo: typing.Optional[float] = ..., ampn: typing.Optional[float] = ..., dyn: typing.Optional[int] = ..., staticnoise: typing.Optional[int] = ..., cpuopt: typing.Optional[int] = ..., patsize: typing.Optional[int] = ...) -> "VideoNode": ...
    def histluma(self, clip: "VideoNode", full: typing.Optional[int] = ..., amp: typing.Optional[int] = ...) -> "VideoNode": ...
    def matrix(self, clip: "VideoNode", mat: typing.Union[str, bytes, bytearray, None] = ..., mats: typing.Union[str, bytes, bytearray, None] = ..., matd: typing.Union[str, bytes, bytearray, None] = ..., fulls: typing.Optional[int] = ..., fulld: typing.Optional[int] = ..., coef: typing.Union[float, typing.Sequence[float], None] = ..., csp: typing.Optional[int] = ..., col_fam: typing.Optional[int] = ..., bits: typing.Optional[int] = ..., singleout: typing.Optional[int] = ..., cpuopt: typing.Optional[int] = ...) -> "VideoNode": ...
    def matrix2020cl(self, clip: "VideoNode", full: typing.Optional[int] = ..., csp: typing.Optional[int] = ..., bits: typing.Optional[int] = ..., cpuopt: typing.Optional[int] = ...) -> "VideoNode": ...
    def nativetostack16(self, clip: "VideoNode") -> "VideoNode": ...
    def primaries(self, clip: "VideoNode", rs: typing.Union[float, typing.Sequence[float], None] = ..., gs: typing.Union[float, typing.Sequence[float], None] = ..., bs: typing.Union[float, typing.Sequence[float], None] = ..., ws: typing.Union[float, typing.Sequence[float], None] = ..., rd: typing.Union[float, typing.Sequence[float], None] = ..., gd: typing.Union[float, typing.Sequence[float], None] = ..., bd: typing.Union[float, typing.Sequence[float], None] = ..., wd: typing.Union[float, typing.Sequence[float], None] = ..., prims: typing.Union[str, bytes, bytearray, None] = ..., primd: typing.Union[str, bytes, bytearray, None] = ..., cpuopt: typing.Optional[int] = ...) -> "VideoNode": ...
    def resample(self, clip: "VideoNode", w: typing.Optional[int] = ..., h: typing.Optional[int] = ..., sx: typing.Union[float, typing.Sequence[float], None] = ..., sy: typing.Union[float, typing.Sequence[float], None] = ..., sw: typing.Union[float, typing.Sequence[float], None] = ..., sh: typing.Union[float, typing.Sequence[float], None] = ..., scale: typing.Optional[float] = ..., scaleh: typing.Optional[float] = ..., scalev: typing.Optional[float] = ..., kernel: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = ..., kernelh: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = ..., kernelv: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = ..., impulse: typing.Union[float, typing.Sequence[float], None] = ..., impulseh: typing.Union[float, typing.Sequence[float], None] = ..., impulsev: typing.Union[float, typing.Sequence[float], None] = ..., taps: typing.Union[int, typing.Sequence[int], None] = ..., tapsh: typing.Union[int, typing.Sequence[int], None] = ..., tapsv: typing.Union[int, typing.Sequence[int], None] = ..., a1: typing.Union[float, typing.Sequence[float], None] = ..., a2: typing.Union[float, typing.Sequence[float], None] = ..., a3: typing.Union[float, typing.Sequence[float], None] = ..., kovrspl: typing.Union[int, typing.Sequence[int], None] = ..., fh: typing.Union[float, typing.Sequence[float], None] = ..., fv: typing.Union[float, typing.Sequence[float], None] = ..., cnorm: typing.Union[int, typing.Sequence[int], None] = ..., totalh: typing.Union[float, typing.Sequence[float], None] = ..., totalv: typing.Union[float, typing.Sequence[float], None] = ..., invks: typing.Union[int, typing.Sequence[int], None] = ..., invksh: typing.Union[int, typing.Sequence[int], None] = ..., invksv: typing.Union[int, typing.Sequence[int], None] = ..., invkstaps: typing.Union[int, typing.Sequence[int], None] = ..., invkstapsh: typing.Union[int, typing.Sequence[int], None] = ..., invkstapsv: typing.Union[int, typing.Sequence[int], None] = ..., csp: typing.Optional[int] = ..., css: typing.Union[str, bytes, bytearray, None] = ..., planes: typing.Union[float, typing.Sequence[float], None] = ..., fulls: typing.Optional[int] = ..., fulld: typing.Optional[int] = ..., center: typing.Union[int, typing.Sequence[int], None] = ..., cplace: typing.Union[str, bytes, bytearray, None] = ..., cplaces: typing.Union[str, bytes, bytearray, None] = ..., cplaced: typing.Union[str, bytes, bytearray, None] = ..., interlaced: typing.Optional[int] = ..., interlacedd: typing.Optional[int] = ..., tff: typing.Optional[int] = ..., tffd: typing.Optional[int] = ..., flt: typing.Optional[int] = ..., cpuopt: typing.Optional[int] = ...) -> "VideoNode": ...
    def stack16tonative(self, clip: "VideoNode") -> "VideoNode": ...
    def transfer(self, clip: "VideoNode", transs: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = ..., transd: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = ..., cont: typing.Optional[float] = ..., gcor: typing.Optional[float] = ..., bits: typing.Optional[int] = ..., flt: typing.Optional[int] = ..., fulls: typing.Optional[int] = ..., fulld: typing.Optional[int] = ..., cpuopt: typing.Optional[int] = ..., blacklvl: typing.Optional[float] = ...) -> "VideoNode": ...


class _Plugin_delogohd_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def AddlogoHD(self, clip: "VideoNode", logofile: typing.Union[str, bytes, bytearray], logoname: typing.Union[str, bytes, bytearray, None] = ..., left: typing.Optional[int] = ..., top: typing.Optional[int] = ..., start: typing.Optional[int] = ..., end: typing.Optional[int] = ..., fadein: typing.Optional[int] = ..., fadeout: typing.Optional[int] = ..., mono: typing.Optional[int] = ..., cutoff: typing.Optional[int] = ...) -> "VideoNode": ...
    def DelogoHD(self, clip: "VideoNode", logofile: typing.Union[str, bytes, bytearray], logoname: typing.Union[str, bytes, bytearray, None] = ..., left: typing.Optional[int] = ..., top: typing.Optional[int] = ..., start: typing.Optional[int] = ..., end: typing.Optional[int] = ..., fadein: typing.Optional[int] = ..., fadeout: typing.Optional[int] = ..., mono: typing.Optional[int] = ..., cutoff: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_neo_f3kdb_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Deband(self, clip: "VideoNode", range: typing.Optional[int] = ..., y: typing.Optional[int] = ..., cb: typing.Optional[int] = ..., cr: typing.Optional[int] = ..., grainy: typing.Optional[int] = ..., grainc: typing.Optional[int] = ..., sample_mode: typing.Optional[int] = ..., seed: typing.Optional[int] = ..., blur_first: typing.Optional[int] = ..., dynamic_grain: typing.Optional[int] = ..., opt: typing.Optional[int] = ..., mt: typing.Optional[int] = ..., dither_algo: typing.Optional[int] = ..., keep_tv_range: typing.Optional[int] = ..., output_depth: typing.Optional[int] = ..., random_algo_ref: typing.Optional[int] = ..., random_algo_grain: typing.Optional[int] = ..., random_param_ref: typing.Optional[float] = ..., random_param_grain: typing.Optional[float] = ..., preset: typing.Union[str, bytes, bytearray, None] = ...) -> "VideoNode": ...


class _Plugin_neo_fft3d_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def FFT3D(self, clip: "VideoNode", sigma: typing.Optional[float] = ..., beta: typing.Optional[float] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., bw: typing.Optional[int] = ..., bh: typing.Optional[int] = ..., bt: typing.Optional[int] = ..., ow: typing.Optional[int] = ..., oh: typing.Optional[int] = ..., kratio: typing.Optional[float] = ..., sharpen: typing.Optional[float] = ..., scutoff: typing.Optional[float] = ..., svr: typing.Optional[float] = ..., smin: typing.Optional[float] = ..., smax: typing.Optional[float] = ..., measure: typing.Optional[int] = ..., interlaced: typing.Optional[int] = ..., wintype: typing.Optional[int] = ..., pframe: typing.Optional[int] = ..., px: typing.Optional[int] = ..., py: typing.Optional[int] = ..., pshow: typing.Optional[int] = ..., pcutoff: typing.Optional[float] = ..., pfactor: typing.Optional[float] = ..., sigma2: typing.Optional[float] = ..., sigma3: typing.Optional[float] = ..., sigma4: typing.Optional[float] = ..., degrid: typing.Optional[float] = ..., dehalo: typing.Optional[float] = ..., hr: typing.Optional[float] = ..., ht: typing.Optional[float] = ..., l: typing.Optional[int] = ..., t: typing.Optional[int] = ..., r: typing.Optional[int] = ..., b: typing.Optional[int] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_neo_vd_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def VagueDenoiser(self, clip: "VideoNode", threshold: typing.Optional[float] = ..., method: typing.Optional[int] = ..., nsteps: typing.Optional[int] = ..., percent: typing.Optional[float] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_vcmod_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def amp(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Optional["VideoNode"]: ...
    def fan(self, clip: "VideoNode", span: typing.Optional[int] = ..., edge: typing.Optional[int] = ..., plus: typing.Optional[int] = ..., minus: typing.Optional[int] = ..., uv: typing.Optional[int] = ...) -> "VideoNode": ...
    def gBlur(self, clip: "VideoNode", ksize: typing.Optional[int] = ..., sd: typing.Optional[float] = ...) -> "VideoNode": ...
    def hist(self, clip: "VideoNode", clipm: typing.Optional["VideoNode"] = ..., type: typing.Optional[int] = ..., table: typing.Union[int, typing.Sequence[int], None] = ..., mf: typing.Optional[int] = ..., window: typing.Optional[int] = ..., limit: typing.Optional[int] = ...) -> "VideoNode": ...
    def mBlur(self, clip: "VideoNode", type: typing.Optional[int] = ..., x: typing.Optional[int] = ..., y: typing.Optional[int] = ...) -> "VideoNode": ...
    def median(self, clip: "VideoNode", maxgrid: typing.Optional[int] = ..., plane: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def neural(self, clip: "VideoNode", txt: typing.Union[str, bytes, bytearray, None] = ..., fname: typing.Union[str, bytes, bytearray, None] = ..., tclip: typing.Optional["VideoNode"] = ..., xpts: typing.Optional[int] = ..., ypts: typing.Optional[int] = ..., tlx: typing.Optional[int] = ..., tty: typing.Optional[int] = ..., trx: typing.Optional[int] = ..., tby: typing.Optional[int] = ..., iter: typing.Optional[int] = ..., bestof: typing.Optional[int] = ..., wset: typing.Optional[int] = ..., rgb: typing.Optional[int] = ...) -> "VideoNode": ...
    def saltPepper(self, clip: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = ..., tol: typing.Optional[int] = ..., avg: typing.Optional[int] = ...) -> "VideoNode": ...
    def variance(self, clip: "VideoNode", lx: int, wd: int, ty: int, ht: int, fn: typing.Optional[int] = ..., uv: typing.Optional[int] = ..., xgrid: typing.Optional[int] = ..., ygrid: typing.Optional[int] = ...) -> "VideoNode": ...
    def veed(self, clip: "VideoNode", str: typing.Optional[int] = ..., rad: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., plimit: typing.Union[int, typing.Sequence[int], None] = ..., mlimit: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...


class _Plugin_akarin_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def DLISR(self, clip: "VideoNode", scale: typing.Optional[int] = ...) -> "VideoNode": ...
    def Expr(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]], expr: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]]], format: typing.Optional[int] = ..., opt: typing.Optional[int] = ..., boundary: typing.Optional[int] = ...) -> "VideoNode": ...
    def Version(self) -> "VideoNode": ...


class _Plugin_bilateral_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Bilateral(self, input: "VideoNode", ref: typing.Optional["VideoNode"] = ..., sigmaS: typing.Union[float, typing.Sequence[float], None] = ..., sigmaR: typing.Union[float, typing.Sequence[float], None] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., algorithm: typing.Union[int, typing.Sequence[int], None] = ..., PBFICnum: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def Gaussian(self, input: "VideoNode", sigma: typing.Union[float, typing.Sequence[float], None] = ..., sigmaV: typing.Union[float, typing.Sequence[float], None] = ...) -> "VideoNode": ...


class _Plugin_adg_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Mask(self, clip: "VideoNode", luma_scaling: typing.Optional[float] = ...) -> "VideoNode": ...


class _Plugin_w2xnvk_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Waifu2x(self, clip: "VideoNode", noise: typing.Optional[int] = ..., scale: typing.Optional[int] = ..., model: typing.Optional[int] = ..., tile_size: typing.Optional[int] = ..., gpu_id: typing.Optional[int] = ..., gpu_thread: typing.Optional[int] = ..., precision: typing.Optional[int] = ..., tile_size_w: typing.Optional[int] = ..., tile_size_h: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_f3kdb_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Deband(self, clip: "VideoNode", range: typing.Optional[int] = ..., y: typing.Optional[int] = ..., cb: typing.Optional[int] = ..., cr: typing.Optional[int] = ..., grainy: typing.Optional[int] = ..., grainc: typing.Optional[int] = ..., sample_mode: typing.Optional[int] = ..., seed: typing.Optional[int] = ..., blur_first: typing.Optional[int] = ..., dynamic_grain: typing.Optional[int] = ..., opt: typing.Optional[int] = ..., dither_algo: typing.Optional[int] = ..., keep_tv_range: typing.Optional[int] = ..., output_depth: typing.Optional[int] = ..., random_algo_ref: typing.Optional[int] = ..., random_algo_grain: typing.Optional[int] = ..., random_param_ref: typing.Optional[float] = ..., random_param_grain: typing.Optional[float] = ..., preset: typing.Union[str, bytes, bytearray, None] = ...) -> "VideoNode": ...


class _Plugin_fft3dfilter_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def FFT3DFilter(self, clip: "VideoNode", sigma: typing.Optional[float] = ..., beta: typing.Optional[float] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., bw: typing.Optional[int] = ..., bh: typing.Optional[int] = ..., bt: typing.Optional[int] = ..., ow: typing.Optional[int] = ..., oh: typing.Optional[int] = ..., kratio: typing.Optional[float] = ..., sharpen: typing.Optional[float] = ..., scutoff: typing.Optional[float] = ..., svr: typing.Optional[float] = ..., smin: typing.Optional[float] = ..., smax: typing.Optional[float] = ..., measure: typing.Optional[int] = ..., interlaced: typing.Optional[int] = ..., wintype: typing.Optional[int] = ..., pframe: typing.Optional[int] = ..., px: typing.Optional[int] = ..., py: typing.Optional[int] = ..., pshow: typing.Optional[int] = ..., pcutoff: typing.Optional[float] = ..., pfactor: typing.Optional[float] = ..., sigma2: typing.Optional[float] = ..., sigma3: typing.Optional[float] = ..., sigma4: typing.Optional[float] = ..., degrid: typing.Optional[float] = ..., dehalo: typing.Optional[float] = ..., hr: typing.Optional[float] = ..., ht: typing.Optional[float] = ..., ncpu: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_lsmas_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def LWLibavSource(self, source: typing.Union[str, bytes, bytearray], stream_index: typing.Optional[int] = ..., cache: typing.Optional[int] = ..., cachefile: typing.Union[str, bytes, bytearray, None] = ..., threads: typing.Optional[int] = ..., seek_mode: typing.Optional[int] = ..., seek_threshold: typing.Optional[int] = ..., dr: typing.Optional[int] = ..., fpsnum: typing.Optional[int] = ..., fpsden: typing.Optional[int] = ..., variable: typing.Optional[int] = ..., format: typing.Union[str, bytes, bytearray, None] = ..., decoder: typing.Union[str, bytes, bytearray, None] = ..., prefer_hw: typing.Optional[int] = ..., repeat: typing.Optional[int] = ..., dominance: typing.Optional[int] = ..., ff_loglevel: typing.Optional[int] = ...) -> "VideoNode": ...
    def LibavSMASHSource(self, source: typing.Union[str, bytes, bytearray], track: typing.Optional[int] = ..., threads: typing.Optional[int] = ..., seek_mode: typing.Optional[int] = ..., seek_threshold: typing.Optional[int] = ..., dr: typing.Optional[int] = ..., fpsnum: typing.Optional[int] = ..., fpsden: typing.Optional[int] = ..., variable: typing.Optional[int] = ..., format: typing.Union[str, bytes, bytearray, None] = ..., decoder: typing.Union[str, bytes, bytearray, None] = ..., prefer_hw: typing.Optional[int] = ..., ff_loglevel: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_descale_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Debicubic(self, src: "VideoNode", width: int, height: int, b: typing.Optional[float] = ..., c: typing.Optional[float] = ..., src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ..., src_width: typing.Optional[float] = ..., src_height: typing.Optional[float] = ...) -> "VideoNode": ...
    def Debilinear(self, src: "VideoNode", width: int, height: int, src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ..., src_width: typing.Optional[float] = ..., src_height: typing.Optional[float] = ...) -> "VideoNode": ...
    def Delanczos(self, src: "VideoNode", width: int, height: int, taps: typing.Optional[int] = ..., src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ..., src_width: typing.Optional[float] = ..., src_height: typing.Optional[float] = ...) -> "VideoNode": ...
    def Despline16(self, src: "VideoNode", width: int, height: int, src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ..., src_width: typing.Optional[float] = ..., src_height: typing.Optional[float] = ...) -> "VideoNode": ...
    def Despline36(self, src: "VideoNode", width: int, height: int, src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ..., src_width: typing.Optional[float] = ..., src_height: typing.Optional[float] = ...) -> "VideoNode": ...
    def Despline64(self, src: "VideoNode", width: int, height: int, src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ..., src_width: typing.Optional[float] = ..., src_height: typing.Optional[float] = ...) -> "VideoNode": ...


class _Plugin_descale_getnative_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def CacheSize(self, size: int) -> "VideoNode": ...
    def Debicubic(self, src: "VideoNode", width: int, height: int, b: typing.Optional[float] = ..., c: typing.Optional[float] = ..., src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ...) -> "VideoNode": ...
    def Debilinear(self, src: "VideoNode", width: int, height: int, src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ...) -> "VideoNode": ...
    def Delanczos(self, src: "VideoNode", width: int, height: int, taps: typing.Optional[int] = ..., src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ...) -> "VideoNode": ...
    def Despline16(self, src: "VideoNode", width: int, height: int, src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ...) -> "VideoNode": ...
    def Despline36(self, src: "VideoNode", width: int, height: int, src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ...) -> "VideoNode": ...


class _Plugin_mx_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Predict(self, clip: "VideoNode", symbol: typing.Union[str, bytes, bytearray], param: typing.Union[str, bytes, bytearray], patch_w: typing.Optional[int] = ..., patch_h: typing.Optional[int] = ..., scale: typing.Optional[int] = ..., output_w: typing.Optional[int] = ..., output_h: typing.Optional[int] = ..., frame_w: typing.Optional[int] = ..., frame_h: typing.Optional[int] = ..., step_w: typing.Optional[int] = ..., step_h: typing.Optional[int] = ..., outstep_w: typing.Optional[int] = ..., outstep_h: typing.Optional[int] = ..., output_format: typing.Optional[int] = ..., input_name: typing.Union[str, bytes, bytearray, None] = ..., ctx: typing.Optional[int] = ..., dev_id: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_avsw_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Eval(self, script: typing.Union[str, bytes, bytearray], clips: typing.Union["VideoNode", typing.Sequence["VideoNode"], None] = ..., clip_names: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = ..., avisynth: typing.Union[str, bytes, bytearray, None] = ..., slave: typing.Union[str, bytes, bytearray, None] = ..., slave_log: typing.Union[str, bytes, bytearray, None] = ...) -> "VideoNode": ...


class _Plugin_znedi3_Core_Unbound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def nnedi3(self, clip: "VideoNode", field: int, dh: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., nsize: typing.Optional[int] = ..., nns: typing.Optional[int] = ..., qual: typing.Optional[int] = ..., etype: typing.Optional[int] = ..., pscrn: typing.Optional[int] = ..., opt: typing.Optional[int] = ..., int16_prescreener: typing.Optional[int] = ..., int16_predictor: typing.Optional[int] = ..., exp: typing.Optional[int] = ..., show_mask: typing.Optional[int] = ..., x_nnedi3_weights_bin: typing.Union[str, bytes, bytearray, None] = ..., x_cpu: typing.Union[str, bytes, bytearray, None] = ...) -> "VideoNode": ...


class _Plugin_acrop_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def AutoCrop(self, range: typing.Optional[int] = ..., top: typing.Optional[int] = ..., bottom: typing.Optional[int] = ..., left: typing.Optional[int] = ..., right: typing.Optional[int] = ..., color: typing.Union[int, typing.Sequence[int], None] = ..., color_second: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def CropProp(self) -> "VideoNode": ...
    def CropValues(self, range: typing.Optional[int] = ..., top: typing.Optional[int] = ..., bottom: typing.Optional[int] = ..., left: typing.Optional[int] = ..., right: typing.Optional[int] = ..., color: typing.Union[int, typing.Sequence[int], None] = ..., color_second: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...


class _Plugin_ocr_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Recognize(self, datapath: typing.Union[str, bytes, bytearray, None] = ..., language: typing.Union[str, bytes, bytearray, None] = ..., options: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = ...) -> "VideoNode": ...


class _Plugin_remap_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def RemapFrames(self, filename: typing.Union[str, bytes, bytearray, None] = ..., mappings: typing.Union[str, bytes, bytearray, None] = ..., sourceclip: typing.Optional["VideoNode"] = ..., mismatch: typing.Optional[int] = ...) -> "VideoNode": ...
    def RemapFramesSimple(self, filename: typing.Union[str, bytes, bytearray, None] = ..., mappings: typing.Union[str, bytes, bytearray, None] = ...) -> "VideoNode": ...
    def Remf(self, filename: typing.Union[str, bytes, bytearray, None] = ..., mappings: typing.Union[str, bytes, bytearray, None] = ..., sourceclip: typing.Optional["VideoNode"] = ..., mismatch: typing.Optional[int] = ...) -> "VideoNode": ...
    def Remfs(self, filename: typing.Union[str, bytes, bytearray, None] = ..., mappings: typing.Union[str, bytes, bytearray, None] = ...) -> "VideoNode": ...
    def ReplaceFramesSimple(self, sourceclip: "VideoNode", filename: typing.Union[str, bytes, bytearray, None] = ..., mappings: typing.Union[str, bytes, bytearray, None] = ..., mismatch: typing.Optional[int] = ...) -> "VideoNode": ...
    def Rfs(self, sourceclip: "VideoNode", filename: typing.Union[str, bytes, bytearray, None] = ..., mappings: typing.Union[str, bytes, bytearray, None] = ..., mismatch: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_comb_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def CMaskedMerge(self, alt: "VideoNode", mask: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def CombMask(self, cthresh: typing.Optional[int] = ..., mthresh: typing.Optional[int] = ..., mi: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...


class _Plugin_focus2_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TemporalSoften2(self, radius: typing.Optional[int] = ..., luma_threshold: typing.Optional[int] = ..., chroma_threshold: typing.Optional[int] = ..., scenechange: typing.Optional[int] = ..., mode: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_knlm_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def KNLMeansCL(self, d: typing.Optional[int] = ..., a: typing.Optional[int] = ..., s: typing.Optional[int] = ..., h: typing.Optional[float] = ..., channels: typing.Union[str, bytes, bytearray, None] = ..., wmode: typing.Optional[int] = ..., wref: typing.Optional[float] = ..., rclip: typing.Optional["VideoNode"] = ..., device_type: typing.Union[str, bytes, bytearray, None] = ..., device_id: typing.Optional[int] = ..., ocl_x: typing.Optional[int] = ..., ocl_y: typing.Optional[int] = ..., ocl_r: typing.Optional[int] = ..., info: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_ftf_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def FixFades(self, mode: typing.Optional[int] = ..., threshold: typing.Optional[float] = ..., color: typing.Union[float, typing.Sequence[float], None] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_nnedi3_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def nnedi3(self, field: int, dh: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., nsize: typing.Optional[int] = ..., nns: typing.Optional[int] = ..., qual: typing.Optional[int] = ..., etype: typing.Optional[int] = ..., pscrn: typing.Optional[int] = ..., opt: typing.Optional[int] = ..., int16_prescreener: typing.Optional[int] = ..., int16_predictor: typing.Optional[int] = ..., exp: typing.Optional[int] = ..., show_mask: typing.Optional[int] = ..., combed_only: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_libp2p_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Pack(self) -> "VideoNode": ...
    def Unpack(self) -> "VideoNode": ...


class _Plugin_ccd_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def CCD(self, threshold: typing.Optional[float] = ...) -> "VideoNode": ...


class _Plugin_grain_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Add(self, var: typing.Optional[float] = ..., uvar: typing.Optional[float] = ..., hcorr: typing.Optional[float] = ..., vcorr: typing.Optional[float] = ..., seed: typing.Optional[int] = ..., constant: typing.Optional[int] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_cas_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def CAS(self, sharpness: typing.Optional[float] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_ctmf_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def CTMF(self, radius: typing.Optional[int] = ..., memsize: typing.Optional[int] = ..., opt: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...


class _Plugin_dctf_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def DCTFilter(self, factors: typing.Union[float, typing.Sequence[float]], planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...


class _Plugin_deblock_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Deblock(self, quant: typing.Optional[int] = ..., aoffset: typing.Optional[int] = ..., boffset: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...


class _Plugin_dfttest_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def DFTTest(self, ftype: typing.Optional[int] = ..., sigma: typing.Optional[float] = ..., sigma2: typing.Optional[float] = ..., pmin: typing.Optional[float] = ..., pmax: typing.Optional[float] = ..., sbsize: typing.Optional[int] = ..., smode: typing.Optional[int] = ..., sosize: typing.Optional[int] = ..., tbsize: typing.Optional[int] = ..., tmode: typing.Optional[int] = ..., tosize: typing.Optional[int] = ..., swin: typing.Optional[int] = ..., twin: typing.Optional[int] = ..., sbeta: typing.Optional[float] = ..., tbeta: typing.Optional[float] = ..., zmean: typing.Optional[int] = ..., f0beta: typing.Optional[float] = ..., nlocation: typing.Union[int, typing.Sequence[int], None] = ..., alpha: typing.Optional[float] = ..., slocation: typing.Union[float, typing.Sequence[float], None] = ..., ssx: typing.Union[float, typing.Sequence[float], None] = ..., ssy: typing.Union[float, typing.Sequence[float], None] = ..., sst: typing.Union[float, typing.Sequence[float], None] = ..., ssystem: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_eedi2_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def EEDI2(self, field: int, mthresh: typing.Optional[int] = ..., lthresh: typing.Optional[int] = ..., vthresh: typing.Optional[int] = ..., estr: typing.Optional[int] = ..., dstr: typing.Optional[int] = ..., maxd: typing.Optional[int] = ..., map: typing.Optional[int] = ..., nt: typing.Optional[int] = ..., pp: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_eedi3m_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def EEDI3(self, field: int, dh: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., alpha: typing.Optional[float] = ..., beta: typing.Optional[float] = ..., gamma: typing.Optional[float] = ..., nrad: typing.Optional[int] = ..., mdis: typing.Optional[int] = ..., hp: typing.Optional[int] = ..., ucubic: typing.Optional[int] = ..., cost3: typing.Optional[int] = ..., vcheck: typing.Optional[int] = ..., vthresh0: typing.Optional[float] = ..., vthresh1: typing.Optional[float] = ..., vthresh2: typing.Optional[float] = ..., sclip: typing.Optional["VideoNode"] = ..., mclip: typing.Optional["VideoNode"] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...
    def EEDI3CL(self, field: int, dh: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., alpha: typing.Optional[float] = ..., beta: typing.Optional[float] = ..., gamma: typing.Optional[float] = ..., nrad: typing.Optional[int] = ..., mdis: typing.Optional[int] = ..., hp: typing.Optional[int] = ..., ucubic: typing.Optional[int] = ..., cost3: typing.Optional[int] = ..., vcheck: typing.Optional[int] = ..., vthresh0: typing.Optional[float] = ..., vthresh1: typing.Optional[float] = ..., vthresh2: typing.Optional[float] = ..., sclip: typing.Optional["VideoNode"] = ..., opt: typing.Optional[int] = ..., device: typing.Optional[int] = ..., list_device: typing.Optional[int] = ..., info: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_lghost_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def LGhost(self, mode: typing.Union[int, typing.Sequence[int]], shift: typing.Union[int, typing.Sequence[int]], intensity: typing.Union[int, typing.Sequence[int]], planes: typing.Union[int, typing.Sequence[int], None] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_nnedi3cl_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def NNEDI3CL(self, field: int, dh: typing.Optional[int] = ..., dw: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., nsize: typing.Optional[int] = ..., nns: typing.Optional[int] = ..., qual: typing.Optional[int] = ..., etype: typing.Optional[int] = ..., pscrn: typing.Optional[int] = ..., device: typing.Optional[int] = ..., list_device: typing.Optional[int] = ..., info: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_tcanny_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TCanny(self, sigma: typing.Union[float, typing.Sequence[float], None] = ..., sigma_v: typing.Union[float, typing.Sequence[float], None] = ..., t_h: typing.Optional[float] = ..., t_l: typing.Optional[float] = ..., mode: typing.Optional[int] = ..., op: typing.Optional[int] = ..., gmmax: typing.Optional[float] = ..., opt: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def TCannyCL(self, sigma: typing.Union[float, typing.Sequence[float], None] = ..., sigma_v: typing.Union[float, typing.Sequence[float], None] = ..., t_h: typing.Optional[float] = ..., t_l: typing.Optional[float] = ..., mode: typing.Optional[int] = ..., op: typing.Optional[int] = ..., gmmax: typing.Optional[float] = ..., device: typing.Optional[int] = ..., list_device: typing.Optional[int] = ..., info: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...


class _Plugin_tdm_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def IsCombed(self, cthresh: typing.Optional[int] = ..., blockx: typing.Optional[int] = ..., blocky: typing.Optional[int] = ..., chroma: typing.Optional[int] = ..., mi: typing.Optional[int] = ..., metric: typing.Optional[int] = ...) -> "VideoNode": ...
    def TDeintMod(self, order: int, field: typing.Optional[int] = ..., mode: typing.Optional[int] = ..., length: typing.Optional[int] = ..., mtype: typing.Optional[int] = ..., ttype: typing.Optional[int] = ..., mtql: typing.Optional[int] = ..., mthl: typing.Optional[int] = ..., mtqc: typing.Optional[int] = ..., mthc: typing.Optional[int] = ..., nt: typing.Optional[int] = ..., minthresh: typing.Optional[int] = ..., maxthresh: typing.Optional[int] = ..., cstr: typing.Optional[int] = ..., athresh: typing.Optional[int] = ..., metric: typing.Optional[int] = ..., expand: typing.Optional[int] = ..., link: typing.Optional[int] = ..., show: typing.Optional[int] = ..., edeint: typing.Optional["VideoNode"] = ..., opt: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...


class _Plugin_ttmpsm_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TTempSmooth(self, maxr: typing.Optional[int] = ..., thresh: typing.Union[int, typing.Sequence[int], None] = ..., mdiff: typing.Union[int, typing.Sequence[int], None] = ..., strength: typing.Optional[int] = ..., scthresh: typing.Optional[float] = ..., fp: typing.Optional[int] = ..., pfclip: typing.Optional["VideoNode"] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...


class _Plugin_vsf_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TextSub(self, file: typing.Union[str, bytes, bytearray], charset: typing.Optional[int] = ..., fps: typing.Optional[float] = ..., vfr: typing.Union[str, bytes, bytearray, None] = ...) -> "VideoNode": ...
    def VobSub(self, file: typing.Union[str, bytes, bytearray]) -> "VideoNode": ...


class _Plugin_vsfm_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TextSubMod(self, file: typing.Union[str, bytes, bytearray], charset: typing.Optional[int] = ..., fps: typing.Optional[float] = ..., vfr: typing.Union[str, bytes, bytearray, None] = ..., accurate: typing.Optional[int] = ...) -> "VideoNode": ...
    def VobSub(self, file: typing.Union[str, bytes, bytearray], accurate: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_w2xc_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Waifu2x(self, noise: typing.Optional[int] = ..., scale: typing.Optional[int] = ..., block: typing.Optional[int] = ..., photo: typing.Optional[int] = ..., gpu: typing.Optional[int] = ..., processor: typing.Optional[int] = ..., list_proc: typing.Optional[int] = ..., log: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_yadifmod_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Yadifmod(self, edeint: "VideoNode", order: int, field: typing.Optional[int] = ..., mode: typing.Optional[int] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_tonemap_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Hable(self, exposure: typing.Optional[float] = ..., a: typing.Optional[float] = ..., b: typing.Optional[float] = ..., c: typing.Optional[float] = ..., d: typing.Optional[float] = ..., e: typing.Optional[float] = ..., f: typing.Optional[float] = ..., w: typing.Optional[float] = ...) -> "VideoNode": ...
    def Mobius(self, exposure: typing.Optional[float] = ..., transition: typing.Optional[float] = ..., peak: typing.Optional[float] = ...) -> "VideoNode": ...
    def Reinhard(self, exposure: typing.Optional[float] = ..., contrast: typing.Optional[float] = ..., peak: typing.Optional[float] = ...) -> "VideoNode": ...


class _Plugin_sangnom_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def SangNom(self, order: typing.Optional[int] = ..., dh: typing.Optional[int] = ..., aa: typing.Union[int, typing.Sequence[int], None] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...


class _Plugin_edgefixer_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ContinuityFixer(self, left: typing.Union[int, typing.Sequence[int]], top: typing.Union[int, typing.Sequence[int]], right: typing.Union[int, typing.Sequence[int]], bottom: typing.Union[int, typing.Sequence[int]], radius: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...


class _Plugin_warp_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ABlur(self, blur: typing.Optional[int] = ..., type: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...
    def ASobel(self, thresh: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...
    def AWarp(self, mask: "VideoNode", depth: typing.Union[int, typing.Sequence[int], None] = ..., chroma: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., opt: typing.Optional[int] = ..., cplace: typing.Union[str, bytes, bytearray, None] = ...) -> "VideoNode": ...
    def AWarpSharp2(self, thresh: typing.Optional[int] = ..., blur: typing.Optional[int] = ..., type: typing.Optional[int] = ..., depth: typing.Union[int, typing.Sequence[int], None] = ..., chroma: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., opt: typing.Optional[int] = ..., cplace: typing.Union[str, bytes, bytearray, None] = ...) -> "VideoNode": ...


class _Plugin_fb_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def FillBorders(self, left: typing.Optional[int] = ..., right: typing.Optional[int] = ..., top: typing.Optional[int] = ..., bottom: typing.Optional[int] = ..., mode: typing.Union[str, bytes, bytearray, None] = ...) -> "VideoNode": ...


class _Plugin_flux_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def SmoothST(self, temporal_threshold: typing.Optional[int] = ..., spatial_threshold: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def SmoothT(self, temporal_threshold: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...


class _Plugin_hist_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Classic(self) -> "VideoNode": ...
    def Color(self) -> "VideoNode": ...
    def Color2(self) -> "VideoNode": ...
    def Levels(self, factor: typing.Optional[float] = ...) -> "VideoNode": ...
    def Luma(self) -> "VideoNode": ...


class _Plugin_median_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Median(self, sync: typing.Optional[int] = ..., samples: typing.Optional[int] = ..., debug: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def MedianBlend(self, low: typing.Optional[int] = ..., high: typing.Optional[int] = ..., closest: typing.Optional[int] = ..., sync: typing.Optional[int] = ..., samples: typing.Optional[int] = ..., debug: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def TemporalMedian(self, radius: typing.Optional[int] = ..., debug: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...


class _Plugin_msmoosh_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def MSharpen(self, threshold: typing.Optional[float] = ..., strength: typing.Optional[float] = ..., mask: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def MSmooth(self, threshold: typing.Optional[float] = ..., strength: typing.Optional[int] = ..., mask: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...


class _Plugin_mvsf_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Analyse(self, blksize: typing.Optional[int] = ..., blksizev: typing.Optional[int] = ..., levels: typing.Optional[int] = ..., search: typing.Optional[int] = ..., searchparam: typing.Optional[int] = ..., pelsearch: typing.Optional[int] = ..., isb: typing.Optional[int] = ..., lambda_: typing.Optional[float] = ..., chroma: typing.Optional[int] = ..., delta: typing.Optional[int] = ..., truemotion: typing.Optional[int] = ..., lsad: typing.Optional[float] = ..., plevel: typing.Optional[int] = ..., global_: typing.Optional[int] = ..., pnew: typing.Optional[int] = ..., pzero: typing.Optional[int] = ..., pglobal: typing.Optional[int] = ..., overlap: typing.Optional[int] = ..., overlapv: typing.Optional[int] = ..., divide: typing.Optional[int] = ..., badsad: typing.Optional[float] = ..., badrange: typing.Optional[int] = ..., meander: typing.Optional[int] = ..., trymany: typing.Optional[int] = ..., fields: typing.Optional[int] = ..., tff: typing.Optional[int] = ..., search_coarse: typing.Optional[int] = ..., dct: typing.Optional[int] = ...) -> "VideoNode": ...
    def Analyze(self, blksize: typing.Optional[int] = ..., blksizev: typing.Optional[int] = ..., levels: typing.Optional[int] = ..., search: typing.Optional[int] = ..., searchparam: typing.Optional[int] = ..., pelsearch: typing.Optional[int] = ..., isb: typing.Optional[int] = ..., lambda_: typing.Optional[float] = ..., chroma: typing.Optional[int] = ..., delta: typing.Optional[int] = ..., truemotion: typing.Optional[int] = ..., lsad: typing.Optional[float] = ..., plevel: typing.Optional[int] = ..., global_: typing.Optional[int] = ..., pnew: typing.Optional[int] = ..., pzero: typing.Optional[int] = ..., pglobal: typing.Optional[int] = ..., overlap: typing.Optional[int] = ..., overlapv: typing.Optional[int] = ..., divide: typing.Optional[int] = ..., badsad: typing.Optional[float] = ..., badrange: typing.Optional[int] = ..., meander: typing.Optional[int] = ..., trymany: typing.Optional[int] = ..., fields: typing.Optional[int] = ..., tff: typing.Optional[int] = ..., search_coarse: typing.Optional[int] = ..., dct: typing.Optional[int] = ...) -> "VideoNode": ...
    def BlockFPS(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", num: typing.Optional[int] = ..., den: typing.Optional[int] = ..., mode: typing.Optional[int] = ..., ml: typing.Optional[float] = ..., blend: typing.Optional[int] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Compensate(self, super: "VideoNode", vectors: "VideoNode", scbehavior: typing.Optional[int] = ..., thsad: typing.Optional[float] = ..., fields: typing.Optional[int] = ..., time: typing.Optional[float] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ..., tff: typing.Optional[int] = ...) -> "VideoNode": ...
    def Degrain1(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain10(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain11(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain12(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain13(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain14(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain15(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain16(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain17(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", mvbw17: "VideoNode", mvfw17: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain18(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", mvbw17: "VideoNode", mvfw17: "VideoNode", mvbw18: "VideoNode", mvfw18: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain19(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", mvbw17: "VideoNode", mvfw17: "VideoNode", mvbw18: "VideoNode", mvfw18: "VideoNode", mvbw19: "VideoNode", mvfw19: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain2(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain20(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", mvbw17: "VideoNode", mvfw17: "VideoNode", mvbw18: "VideoNode", mvfw18: "VideoNode", mvbw19: "VideoNode", mvfw19: "VideoNode", mvbw20: "VideoNode", mvfw20: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain21(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", mvbw17: "VideoNode", mvfw17: "VideoNode", mvbw18: "VideoNode", mvfw18: "VideoNode", mvbw19: "VideoNode", mvfw19: "VideoNode", mvbw20: "VideoNode", mvfw20: "VideoNode", mvbw21: "VideoNode", mvfw21: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain22(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", mvbw17: "VideoNode", mvfw17: "VideoNode", mvbw18: "VideoNode", mvfw18: "VideoNode", mvbw19: "VideoNode", mvfw19: "VideoNode", mvbw20: "VideoNode", mvfw20: "VideoNode", mvbw21: "VideoNode", mvfw21: "VideoNode", mvbw22: "VideoNode", mvfw22: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain23(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", mvbw17: "VideoNode", mvfw17: "VideoNode", mvbw18: "VideoNode", mvfw18: "VideoNode", mvbw19: "VideoNode", mvfw19: "VideoNode", mvbw20: "VideoNode", mvfw20: "VideoNode", mvbw21: "VideoNode", mvfw21: "VideoNode", mvbw22: "VideoNode", mvfw22: "VideoNode", mvbw23: "VideoNode", mvfw23: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain24(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", mvbw10: "VideoNode", mvfw10: "VideoNode", mvbw11: "VideoNode", mvfw11: "VideoNode", mvbw12: "VideoNode", mvfw12: "VideoNode", mvbw13: "VideoNode", mvfw13: "VideoNode", mvbw14: "VideoNode", mvfw14: "VideoNode", mvbw15: "VideoNode", mvfw15: "VideoNode", mvbw16: "VideoNode", mvfw16: "VideoNode", mvbw17: "VideoNode", mvfw17: "VideoNode", mvbw18: "VideoNode", mvfw18: "VideoNode", mvbw19: "VideoNode", mvfw19: "VideoNode", mvbw20: "VideoNode", mvfw20: "VideoNode", mvbw21: "VideoNode", mvfw21: "VideoNode", mvbw22: "VideoNode", mvfw22: "VideoNode", mvbw23: "VideoNode", mvfw23: "VideoNode", mvbw24: "VideoNode", mvfw24: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain3(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain4(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain5(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain6(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain7(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain8(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Degrain9(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", mvbw4: "VideoNode", mvfw4: "VideoNode", mvbw5: "VideoNode", mvfw5: "VideoNode", mvbw6: "VideoNode", mvfw6: "VideoNode", mvbw7: "VideoNode", mvfw7: "VideoNode", mvbw8: "VideoNode", mvfw8: "VideoNode", mvbw9: "VideoNode", mvfw9: "VideoNode", thsad: typing.Union[float, typing.Sequence[float], None] = ..., plane: typing.Optional[int] = ..., limit: typing.Union[float, typing.Sequence[float], None] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Finest(self) -> "VideoNode": ...
    def Flow(self, super: "VideoNode", vectors: "VideoNode", time: typing.Optional[float] = ..., mode: typing.Optional[int] = ..., fields: typing.Optional[int] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ..., tff: typing.Optional[int] = ...) -> "VideoNode": ...
    def FlowBlur(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", blur: typing.Optional[float] = ..., prec: typing.Optional[int] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def FlowFPS(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", num: typing.Optional[int] = ..., den: typing.Optional[int] = ..., mask: typing.Optional[int] = ..., ml: typing.Optional[float] = ..., blend: typing.Optional[int] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def FlowInter(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", time: typing.Optional[float] = ..., ml: typing.Optional[float] = ..., blend: typing.Optional[int] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Mask(self, vectors: "VideoNode", ml: typing.Optional[float] = ..., gamma: typing.Optional[float] = ..., kind: typing.Optional[int] = ..., time: typing.Optional[float] = ..., ysc: typing.Optional[float] = ..., thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Recalculate(self, vectors: "VideoNode", thsad: typing.Optional[float] = ..., smooth: typing.Optional[int] = ..., blksize: typing.Optional[int] = ..., blksizev: typing.Optional[int] = ..., search: typing.Optional[int] = ..., searchparam: typing.Optional[int] = ..., lambda_: typing.Optional[float] = ..., chroma: typing.Optional[int] = ..., truemotion: typing.Optional[int] = ..., pnew: typing.Optional[int] = ..., overlap: typing.Optional[int] = ..., overlapv: typing.Optional[int] = ..., divide: typing.Optional[int] = ..., meander: typing.Optional[int] = ..., fields: typing.Optional[int] = ..., tff: typing.Optional[int] = ..., dct: typing.Optional[int] = ...) -> "VideoNode": ...
    def SCDetection(self, vectors: "VideoNode", thscd1: typing.Optional[float] = ..., thscd2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Super(self, hpad: typing.Optional[int] = ..., vpad: typing.Optional[int] = ..., pel: typing.Optional[int] = ..., levels: typing.Optional[int] = ..., chroma: typing.Optional[int] = ..., sharp: typing.Optional[int] = ..., rfilter: typing.Optional[int] = ..., pelclip: typing.Optional["VideoNode"] = ...) -> "VideoNode": ...


class _Plugin_mv_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Analyse(self, blksize: typing.Optional[int] = ..., blksizev: typing.Optional[int] = ..., levels: typing.Optional[int] = ..., search: typing.Optional[int] = ..., searchparam: typing.Optional[int] = ..., pelsearch: typing.Optional[int] = ..., isb: typing.Optional[int] = ..., lambda_: typing.Optional[int] = ..., chroma: typing.Optional[int] = ..., delta: typing.Optional[int] = ..., truemotion: typing.Optional[int] = ..., lsad: typing.Optional[int] = ..., plevel: typing.Optional[int] = ..., global_: typing.Optional[int] = ..., pnew: typing.Optional[int] = ..., pzero: typing.Optional[int] = ..., pglobal: typing.Optional[int] = ..., overlap: typing.Optional[int] = ..., overlapv: typing.Optional[int] = ..., divide: typing.Optional[int] = ..., badsad: typing.Optional[int] = ..., badrange: typing.Optional[int] = ..., opt: typing.Optional[int] = ..., meander: typing.Optional[int] = ..., trymany: typing.Optional[int] = ..., fields: typing.Optional[int] = ..., tff: typing.Optional[int] = ..., search_coarse: typing.Optional[int] = ..., dct: typing.Optional[int] = ...) -> "VideoNode": ...
    def BlockFPS(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", num: typing.Optional[int] = ..., den: typing.Optional[int] = ..., mode: typing.Optional[int] = ..., ml: typing.Optional[float] = ..., blend: typing.Optional[int] = ..., thscd1: typing.Optional[int] = ..., thscd2: typing.Optional[int] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...
    def Compensate(self, super: "VideoNode", vectors: "VideoNode", scbehavior: typing.Optional[int] = ..., thsad: typing.Optional[int] = ..., fields: typing.Optional[int] = ..., time: typing.Optional[float] = ..., thscd1: typing.Optional[int] = ..., thscd2: typing.Optional[int] = ..., opt: typing.Optional[int] = ..., tff: typing.Optional[int] = ...) -> "VideoNode": ...
    def Degrain1(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", thsad: typing.Optional[int] = ..., thsadc: typing.Optional[int] = ..., plane: typing.Optional[int] = ..., limit: typing.Optional[int] = ..., limitc: typing.Optional[int] = ..., thscd1: typing.Optional[int] = ..., thscd2: typing.Optional[int] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...
    def Degrain2(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", thsad: typing.Optional[int] = ..., thsadc: typing.Optional[int] = ..., plane: typing.Optional[int] = ..., limit: typing.Optional[int] = ..., limitc: typing.Optional[int] = ..., thscd1: typing.Optional[int] = ..., thscd2: typing.Optional[int] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...
    def Degrain3(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", mvbw2: "VideoNode", mvfw2: "VideoNode", mvbw3: "VideoNode", mvfw3: "VideoNode", thsad: typing.Optional[int] = ..., thsadc: typing.Optional[int] = ..., plane: typing.Optional[int] = ..., limit: typing.Optional[int] = ..., limitc: typing.Optional[int] = ..., thscd1: typing.Optional[int] = ..., thscd2: typing.Optional[int] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...
    def DepanAnalyse(self, vectors: "VideoNode", mask: typing.Optional["VideoNode"] = ..., zoom: typing.Optional[int] = ..., rot: typing.Optional[int] = ..., pixaspect: typing.Optional[float] = ..., error: typing.Optional[float] = ..., info: typing.Optional[int] = ..., wrong: typing.Optional[float] = ..., zerow: typing.Optional[float] = ..., thscd1: typing.Optional[int] = ..., thscd2: typing.Optional[int] = ..., fields: typing.Optional[int] = ..., tff: typing.Optional[int] = ...) -> "VideoNode": ...
    def DepanCompensate(self, data: "VideoNode", offset: typing.Optional[float] = ..., subpixel: typing.Optional[int] = ..., pixaspect: typing.Optional[float] = ..., matchfields: typing.Optional[int] = ..., mirror: typing.Optional[int] = ..., blur: typing.Optional[int] = ..., info: typing.Optional[int] = ..., fields: typing.Optional[int] = ..., tff: typing.Optional[int] = ...) -> "VideoNode": ...
    def DepanEstimate(self, trust: typing.Optional[float] = ..., winx: typing.Optional[int] = ..., winy: typing.Optional[int] = ..., wleft: typing.Optional[int] = ..., wtop: typing.Optional[int] = ..., dxmax: typing.Optional[int] = ..., dymax: typing.Optional[int] = ..., zoommax: typing.Optional[float] = ..., stab: typing.Optional[float] = ..., pixaspect: typing.Optional[float] = ..., info: typing.Optional[int] = ..., show: typing.Optional[int] = ..., fields: typing.Optional[int] = ..., tff: typing.Optional[int] = ...) -> "VideoNode": ...
    def DepanStabilise(self, data: "VideoNode", cutoff: typing.Optional[float] = ..., damping: typing.Optional[float] = ..., initzoom: typing.Optional[float] = ..., addzoom: typing.Optional[int] = ..., prev: typing.Optional[int] = ..., next: typing.Optional[int] = ..., mirror: typing.Optional[int] = ..., blur: typing.Optional[int] = ..., dxmax: typing.Optional[float] = ..., dymax: typing.Optional[float] = ..., zoommax: typing.Optional[float] = ..., rotmax: typing.Optional[float] = ..., subpixel: typing.Optional[int] = ..., pixaspect: typing.Optional[float] = ..., fitlast: typing.Optional[int] = ..., tzoom: typing.Optional[float] = ..., info: typing.Optional[int] = ..., method: typing.Optional[int] = ..., fields: typing.Optional[int] = ...) -> "VideoNode": ...
    def Finest(self, opt: typing.Optional[int] = ...) -> "VideoNode": ...
    def Flow(self, super: "VideoNode", vectors: "VideoNode", time: typing.Optional[float] = ..., mode: typing.Optional[int] = ..., fields: typing.Optional[int] = ..., thscd1: typing.Optional[int] = ..., thscd2: typing.Optional[int] = ..., opt: typing.Optional[int] = ..., tff: typing.Optional[int] = ...) -> "VideoNode": ...
    def FlowBlur(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", blur: typing.Optional[float] = ..., prec: typing.Optional[int] = ..., thscd1: typing.Optional[int] = ..., thscd2: typing.Optional[int] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...
    def FlowFPS(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", num: typing.Optional[int] = ..., den: typing.Optional[int] = ..., mask: typing.Optional[int] = ..., ml: typing.Optional[float] = ..., blend: typing.Optional[int] = ..., thscd1: typing.Optional[int] = ..., thscd2: typing.Optional[int] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...
    def FlowInter(self, super: "VideoNode", mvbw: "VideoNode", mvfw: "VideoNode", time: typing.Optional[float] = ..., ml: typing.Optional[float] = ..., blend: typing.Optional[int] = ..., thscd1: typing.Optional[int] = ..., thscd2: typing.Optional[int] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...
    def Mask(self, vectors: "VideoNode", ml: typing.Optional[float] = ..., gamma: typing.Optional[float] = ..., kind: typing.Optional[int] = ..., time: typing.Optional[float] = ..., ysc: typing.Optional[int] = ..., thscd1: typing.Optional[int] = ..., thscd2: typing.Optional[int] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...
    def Recalculate(self, vectors: "VideoNode", thsad: typing.Optional[int] = ..., smooth: typing.Optional[int] = ..., blksize: typing.Optional[int] = ..., blksizev: typing.Optional[int] = ..., search: typing.Optional[int] = ..., searchparam: typing.Optional[int] = ..., lambda_: typing.Optional[int] = ..., chroma: typing.Optional[int] = ..., truemotion: typing.Optional[int] = ..., pnew: typing.Optional[int] = ..., overlap: typing.Optional[int] = ..., overlapv: typing.Optional[int] = ..., divide: typing.Optional[int] = ..., opt: typing.Optional[int] = ..., meander: typing.Optional[int] = ..., fields: typing.Optional[int] = ..., tff: typing.Optional[int] = ..., dct: typing.Optional[int] = ...) -> "VideoNode": ...
    def SCDetection(self, vectors: "VideoNode", thscd1: typing.Optional[int] = ..., thscd2: typing.Optional[int] = ...) -> "VideoNode": ...
    def Super(self, hpad: typing.Optional[int] = ..., vpad: typing.Optional[int] = ..., pel: typing.Optional[int] = ..., levels: typing.Optional[int] = ..., chroma: typing.Optional[int] = ..., sharp: typing.Optional[int] = ..., rfilter: typing.Optional[int] = ..., pelclip: typing.Optional["VideoNode"] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_scxvid_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Scxvid(self, log: typing.Union[str, bytes, bytearray, None] = ..., use_slices: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_tedgemask_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TEdgeMask(self, threshold: typing.Union[float, typing.Sequence[float], None] = ..., type: typing.Optional[int] = ..., link: typing.Optional[int] = ..., scale: typing.Optional[float] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_tmedian_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TemporalMedian(self, radius: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...


class _Plugin_tivtc_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TDecimate(self, mode: typing.Optional[int] = ..., cycleR: typing.Optional[int] = ..., cycle: typing.Optional[int] = ..., rate: typing.Optional[float] = ..., dupThresh: typing.Optional[float] = ..., vidThresh: typing.Optional[float] = ..., sceneThresh: typing.Optional[float] = ..., hybrid: typing.Optional[int] = ..., vidDetect: typing.Optional[int] = ..., conCycle: typing.Optional[int] = ..., conCycleTP: typing.Optional[int] = ..., ovr: typing.Union[str, bytes, bytearray, None] = ..., output: typing.Union[str, bytes, bytearray, None] = ..., input: typing.Union[str, bytes, bytearray, None] = ..., tfmIn: typing.Union[str, bytes, bytearray, None] = ..., mkvOut: typing.Union[str, bytes, bytearray, None] = ..., nt: typing.Optional[int] = ..., blockx: typing.Optional[int] = ..., blocky: typing.Optional[int] = ..., debug: typing.Optional[int] = ..., display: typing.Optional[int] = ..., vfrDec: typing.Optional[int] = ..., batch: typing.Optional[int] = ..., tcfv1: typing.Optional[int] = ..., se: typing.Optional[int] = ..., chroma: typing.Optional[int] = ..., exPP: typing.Optional[int] = ..., maxndl: typing.Optional[int] = ..., m2PA: typing.Optional[int] = ..., denoise: typing.Optional[int] = ..., noblend: typing.Optional[int] = ..., ssd: typing.Optional[int] = ..., hint: typing.Optional[int] = ..., clip2: typing.Optional["VideoNode"] = ..., sdlim: typing.Optional[int] = ..., opt: typing.Optional[int] = ..., orgOut: typing.Union[str, bytes, bytearray, None] = ...) -> "VideoNode": ...
    def TFM(self, order: typing.Optional[int] = ..., field: typing.Optional[int] = ..., mode: typing.Optional[int] = ..., PP: typing.Optional[int] = ..., ovr: typing.Union[str, bytes, bytearray, None] = ..., input: typing.Union[str, bytes, bytearray, None] = ..., output: typing.Union[str, bytes, bytearray, None] = ..., outputC: typing.Union[str, bytes, bytearray, None] = ..., debug: typing.Optional[int] = ..., display: typing.Optional[int] = ..., slow: typing.Optional[int] = ..., mChroma: typing.Optional[int] = ..., cNum: typing.Optional[int] = ..., cthresh: typing.Optional[int] = ..., MI: typing.Optional[int] = ..., chroma: typing.Optional[int] = ..., blockx: typing.Optional[int] = ..., blocky: typing.Optional[int] = ..., y0: typing.Optional[int] = ..., y1: typing.Optional[int] = ..., mthresh: typing.Optional[int] = ..., clip2: typing.Optional["VideoNode"] = ..., d2v: typing.Union[str, bytes, bytearray, None] = ..., ovrDefault: typing.Optional[int] = ..., flags: typing.Optional[int] = ..., scthresh: typing.Optional[float] = ..., micout: typing.Optional[int] = ..., micmatching: typing.Optional[int] = ..., trimIn: typing.Union[str, bytes, bytearray, None] = ..., hint: typing.Optional[int] = ..., metric: typing.Optional[int] = ..., batch: typing.Optional[int] = ..., ubsco: typing.Optional[int] = ..., mmsco: typing.Optional[int] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_wwxd_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def WWXD(self) -> "VideoNode": ...


class _Plugin_d2v_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ApplyRFF(self, d2v: typing.Union[str, bytes, bytearray]) -> "VideoNode": ...


class _Plugin_svp1_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Analyse(self, sdata: int, src: "VideoNode", opt: typing.Union[str, bytes, bytearray]) -> "VideoNode": ...
    def Super(self, opt: typing.Union[str, bytes, bytearray]) -> "VideoNode": ...


class _Plugin_svp2_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def SmoothFps(self, super: "VideoNode", sdata: int, vectors: "VideoNode", vdata: int, opt: typing.Union[str, bytes, bytearray], src: typing.Optional["VideoNode"] = ..., fps: typing.Optional[float] = ...) -> "VideoNode": ...
    def SmoothFps_NVOF(self, opt: typing.Union[str, bytes, bytearray], nvof_src: typing.Optional["VideoNode"] = ..., src: typing.Optional["VideoNode"] = ..., fps: typing.Optional[float] = ...) -> "VideoNode": ...


class _Plugin_area_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def AreaResize(self, width: int, height: int, gamma: typing.Optional[float] = ...) -> "VideoNode": ...


class _Plugin_bm3d_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Basic(self, ref: typing.Optional["VideoNode"] = ..., profile: typing.Union[str, bytes, bytearray, None] = ..., sigma: typing.Union[float, typing.Sequence[float], None] = ..., block_size: typing.Optional[int] = ..., block_step: typing.Optional[int] = ..., group_size: typing.Optional[int] = ..., bm_range: typing.Optional[int] = ..., bm_step: typing.Optional[int] = ..., th_mse: typing.Optional[float] = ..., hard_thr: typing.Optional[float] = ..., matrix: typing.Optional[int] = ...) -> "VideoNode": ...
    def Final(self, ref: "VideoNode", profile: typing.Union[str, bytes, bytearray, None] = ..., sigma: typing.Union[float, typing.Sequence[float], None] = ..., block_size: typing.Optional[int] = ..., block_step: typing.Optional[int] = ..., group_size: typing.Optional[int] = ..., bm_range: typing.Optional[int] = ..., bm_step: typing.Optional[int] = ..., th_mse: typing.Optional[float] = ..., matrix: typing.Optional[int] = ...) -> "VideoNode": ...
    def OPP2RGB(self, sample: typing.Optional[int] = ...) -> "VideoNode": ...
    def RGB2OPP(self, sample: typing.Optional[int] = ...) -> "VideoNode": ...
    def VAggregate(self, radius: typing.Optional[int] = ..., sample: typing.Optional[int] = ...) -> "VideoNode": ...
    def VBasic(self, ref: typing.Optional["VideoNode"] = ..., profile: typing.Union[str, bytes, bytearray, None] = ..., sigma: typing.Union[float, typing.Sequence[float], None] = ..., radius: typing.Optional[int] = ..., block_size: typing.Optional[int] = ..., block_step: typing.Optional[int] = ..., group_size: typing.Optional[int] = ..., bm_range: typing.Optional[int] = ..., bm_step: typing.Optional[int] = ..., ps_num: typing.Optional[int] = ..., ps_range: typing.Optional[int] = ..., ps_step: typing.Optional[int] = ..., th_mse: typing.Optional[float] = ..., hard_thr: typing.Optional[float] = ..., matrix: typing.Optional[int] = ...) -> "VideoNode": ...
    def VFinal(self, ref: "VideoNode", profile: typing.Union[str, bytes, bytearray, None] = ..., sigma: typing.Union[float, typing.Sequence[float], None] = ..., radius: typing.Optional[int] = ..., block_size: typing.Optional[int] = ..., block_step: typing.Optional[int] = ..., group_size: typing.Optional[int] = ..., bm_range: typing.Optional[int] = ..., bm_step: typing.Optional[int] = ..., ps_num: typing.Optional[int] = ..., ps_range: typing.Optional[int] = ..., ps_step: typing.Optional[int] = ..., th_mse: typing.Optional[float] = ..., matrix: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_hqdn3d_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Hqdn3d(self, lum_spac: typing.Optional[float] = ..., chrom_spac: typing.Optional[float] = ..., lum_tmp: typing.Optional[float] = ..., chrom_tmp: typing.Optional[float] = ..., restart_lap: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_imwri_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Write(self, imgformat: typing.Union[str, bytes, bytearray], filename: typing.Union[str, bytes, bytearray], firstnum: typing.Optional[int] = ..., quality: typing.Optional[int] = ..., dither: typing.Optional[int] = ..., compression_type: typing.Union[str, bytes, bytearray, None] = ..., overwrite: typing.Optional[int] = ..., alpha: typing.Optional["VideoNode"] = ...) -> "VideoNode": ...


class _Plugin_jinc_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def JincResize(self, width: int, height: int, tap: typing.Optional[int] = ..., src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ..., src_width: typing.Optional[float] = ..., src_height: typing.Optional[float] = ..., quant_x: typing.Optional[int] = ..., quant_y: typing.Optional[int] = ..., blur: typing.Optional[float] = ...) -> "VideoNode": ...


class _Plugin_rsnv_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def RealSR(self, scale: typing.Optional[int] = ..., tilesize_x: typing.Optional[int] = ..., tilesize_y: typing.Optional[int] = ..., gpu_id: typing.Optional[int] = ..., gpu_thread: typing.Optional[int] = ..., tta: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_rgsf_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def BackwardClense(self, planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def Clense(self, previous: typing.Optional["VideoNode"] = ..., next: typing.Optional["VideoNode"] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def ForwardClense(self, planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def RemoveGrain(self, mode: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def Repair(self, repairclip: "VideoNode", mode: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def VerticalCleaner(self, mode: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...


class _Plugin_rgvs_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def BackwardClense(self, planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def Clense(self, previous: typing.Optional["VideoNode"] = ..., next: typing.Optional["VideoNode"] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def ForwardClense(self, planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def RemoveGrain(self, mode: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def Repair(self, repairclip: "VideoNode", mode: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def VerticalCleaner(self, mode: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...


class _Plugin_resize_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Bicubic(self, width: typing.Optional[int] = ..., height: typing.Optional[int] = ..., format: typing.Optional[int] = ..., matrix: typing.Optional[int] = ..., matrix_s: typing.Union[str, bytes, bytearray, None] = ..., transfer: typing.Optional[int] = ..., transfer_s: typing.Union[str, bytes, bytearray, None] = ..., primaries: typing.Optional[int] = ..., primaries_s: typing.Union[str, bytes, bytearray, None] = ..., range: typing.Optional[int] = ..., range_s: typing.Union[str, bytes, bytearray, None] = ..., chromaloc: typing.Optional[int] = ..., chromaloc_s: typing.Union[str, bytes, bytearray, None] = ..., matrix_in: typing.Optional[int] = ..., matrix_in_s: typing.Union[str, bytes, bytearray, None] = ..., transfer_in: typing.Optional[int] = ..., transfer_in_s: typing.Union[str, bytes, bytearray, None] = ..., primaries_in: typing.Optional[int] = ..., primaries_in_s: typing.Union[str, bytes, bytearray, None] = ..., range_in: typing.Optional[int] = ..., range_in_s: typing.Union[str, bytes, bytearray, None] = ..., chromaloc_in: typing.Optional[int] = ..., chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = ..., filter_param_a: typing.Optional[float] = ..., filter_param_b: typing.Optional[float] = ..., resample_filter_uv: typing.Union[str, bytes, bytearray, None] = ..., filter_param_a_uv: typing.Optional[float] = ..., filter_param_b_uv: typing.Optional[float] = ..., dither_type: typing.Union[str, bytes, bytearray, None] = ..., cpu_type: typing.Union[str, bytes, bytearray, None] = ..., prefer_props: typing.Optional[int] = ..., src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ..., src_width: typing.Optional[float] = ..., src_height: typing.Optional[float] = ..., nominal_luminance: typing.Optional[float] = ...) -> "VideoNode": ...
    def Bilinear(self, width: typing.Optional[int] = ..., height: typing.Optional[int] = ..., format: typing.Optional[int] = ..., matrix: typing.Optional[int] = ..., matrix_s: typing.Union[str, bytes, bytearray, None] = ..., transfer: typing.Optional[int] = ..., transfer_s: typing.Union[str, bytes, bytearray, None] = ..., primaries: typing.Optional[int] = ..., primaries_s: typing.Union[str, bytes, bytearray, None] = ..., range: typing.Optional[int] = ..., range_s: typing.Union[str, bytes, bytearray, None] = ..., chromaloc: typing.Optional[int] = ..., chromaloc_s: typing.Union[str, bytes, bytearray, None] = ..., matrix_in: typing.Optional[int] = ..., matrix_in_s: typing.Union[str, bytes, bytearray, None] = ..., transfer_in: typing.Optional[int] = ..., transfer_in_s: typing.Union[str, bytes, bytearray, None] = ..., primaries_in: typing.Optional[int] = ..., primaries_in_s: typing.Union[str, bytes, bytearray, None] = ..., range_in: typing.Optional[int] = ..., range_in_s: typing.Union[str, bytes, bytearray, None] = ..., chromaloc_in: typing.Optional[int] = ..., chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = ..., filter_param_a: typing.Optional[float] = ..., filter_param_b: typing.Optional[float] = ..., resample_filter_uv: typing.Union[str, bytes, bytearray, None] = ..., filter_param_a_uv: typing.Optional[float] = ..., filter_param_b_uv: typing.Optional[float] = ..., dither_type: typing.Union[str, bytes, bytearray, None] = ..., cpu_type: typing.Union[str, bytes, bytearray, None] = ..., prefer_props: typing.Optional[int] = ..., src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ..., src_width: typing.Optional[float] = ..., src_height: typing.Optional[float] = ..., nominal_luminance: typing.Optional[float] = ...) -> "VideoNode": ...
    def Lanczos(self, width: typing.Optional[int] = ..., height: typing.Optional[int] = ..., format: typing.Optional[int] = ..., matrix: typing.Optional[int] = ..., matrix_s: typing.Union[str, bytes, bytearray, None] = ..., transfer: typing.Optional[int] = ..., transfer_s: typing.Union[str, bytes, bytearray, None] = ..., primaries: typing.Optional[int] = ..., primaries_s: typing.Union[str, bytes, bytearray, None] = ..., range: typing.Optional[int] = ..., range_s: typing.Union[str, bytes, bytearray, None] = ..., chromaloc: typing.Optional[int] = ..., chromaloc_s: typing.Union[str, bytes, bytearray, None] = ..., matrix_in: typing.Optional[int] = ..., matrix_in_s: typing.Union[str, bytes, bytearray, None] = ..., transfer_in: typing.Optional[int] = ..., transfer_in_s: typing.Union[str, bytes, bytearray, None] = ..., primaries_in: typing.Optional[int] = ..., primaries_in_s: typing.Union[str, bytes, bytearray, None] = ..., range_in: typing.Optional[int] = ..., range_in_s: typing.Union[str, bytes, bytearray, None] = ..., chromaloc_in: typing.Optional[int] = ..., chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = ..., filter_param_a: typing.Optional[float] = ..., filter_param_b: typing.Optional[float] = ..., resample_filter_uv: typing.Union[str, bytes, bytearray, None] = ..., filter_param_a_uv: typing.Optional[float] = ..., filter_param_b_uv: typing.Optional[float] = ..., dither_type: typing.Union[str, bytes, bytearray, None] = ..., cpu_type: typing.Union[str, bytes, bytearray, None] = ..., prefer_props: typing.Optional[int] = ..., src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ..., src_width: typing.Optional[float] = ..., src_height: typing.Optional[float] = ..., nominal_luminance: typing.Optional[float] = ...) -> "VideoNode": ...
    def Point(self, width: typing.Optional[int] = ..., height: typing.Optional[int] = ..., format: typing.Optional[int] = ..., matrix: typing.Optional[int] = ..., matrix_s: typing.Union[str, bytes, bytearray, None] = ..., transfer: typing.Optional[int] = ..., transfer_s: typing.Union[str, bytes, bytearray, None] = ..., primaries: typing.Optional[int] = ..., primaries_s: typing.Union[str, bytes, bytearray, None] = ..., range: typing.Optional[int] = ..., range_s: typing.Union[str, bytes, bytearray, None] = ..., chromaloc: typing.Optional[int] = ..., chromaloc_s: typing.Union[str, bytes, bytearray, None] = ..., matrix_in: typing.Optional[int] = ..., matrix_in_s: typing.Union[str, bytes, bytearray, None] = ..., transfer_in: typing.Optional[int] = ..., transfer_in_s: typing.Union[str, bytes, bytearray, None] = ..., primaries_in: typing.Optional[int] = ..., primaries_in_s: typing.Union[str, bytes, bytearray, None] = ..., range_in: typing.Optional[int] = ..., range_in_s: typing.Union[str, bytes, bytearray, None] = ..., chromaloc_in: typing.Optional[int] = ..., chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = ..., filter_param_a: typing.Optional[float] = ..., filter_param_b: typing.Optional[float] = ..., resample_filter_uv: typing.Union[str, bytes, bytearray, None] = ..., filter_param_a_uv: typing.Optional[float] = ..., filter_param_b_uv: typing.Optional[float] = ..., dither_type: typing.Union[str, bytes, bytearray, None] = ..., cpu_type: typing.Union[str, bytes, bytearray, None] = ..., prefer_props: typing.Optional[int] = ..., src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ..., src_width: typing.Optional[float] = ..., src_height: typing.Optional[float] = ..., nominal_luminance: typing.Optional[float] = ...) -> "VideoNode": ...
    def Spline16(self, width: typing.Optional[int] = ..., height: typing.Optional[int] = ..., format: typing.Optional[int] = ..., matrix: typing.Optional[int] = ..., matrix_s: typing.Union[str, bytes, bytearray, None] = ..., transfer: typing.Optional[int] = ..., transfer_s: typing.Union[str, bytes, bytearray, None] = ..., primaries: typing.Optional[int] = ..., primaries_s: typing.Union[str, bytes, bytearray, None] = ..., range: typing.Optional[int] = ..., range_s: typing.Union[str, bytes, bytearray, None] = ..., chromaloc: typing.Optional[int] = ..., chromaloc_s: typing.Union[str, bytes, bytearray, None] = ..., matrix_in: typing.Optional[int] = ..., matrix_in_s: typing.Union[str, bytes, bytearray, None] = ..., transfer_in: typing.Optional[int] = ..., transfer_in_s: typing.Union[str, bytes, bytearray, None] = ..., primaries_in: typing.Optional[int] = ..., primaries_in_s: typing.Union[str, bytes, bytearray, None] = ..., range_in: typing.Optional[int] = ..., range_in_s: typing.Union[str, bytes, bytearray, None] = ..., chromaloc_in: typing.Optional[int] = ..., chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = ..., filter_param_a: typing.Optional[float] = ..., filter_param_b: typing.Optional[float] = ..., resample_filter_uv: typing.Union[str, bytes, bytearray, None] = ..., filter_param_a_uv: typing.Optional[float] = ..., filter_param_b_uv: typing.Optional[float] = ..., dither_type: typing.Union[str, bytes, bytearray, None] = ..., cpu_type: typing.Union[str, bytes, bytearray, None] = ..., prefer_props: typing.Optional[int] = ..., src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ..., src_width: typing.Optional[float] = ..., src_height: typing.Optional[float] = ..., nominal_luminance: typing.Optional[float] = ...) -> "VideoNode": ...
    def Spline36(self, width: typing.Optional[int] = ..., height: typing.Optional[int] = ..., format: typing.Optional[int] = ..., matrix: typing.Optional[int] = ..., matrix_s: typing.Union[str, bytes, bytearray, None] = ..., transfer: typing.Optional[int] = ..., transfer_s: typing.Union[str, bytes, bytearray, None] = ..., primaries: typing.Optional[int] = ..., primaries_s: typing.Union[str, bytes, bytearray, None] = ..., range: typing.Optional[int] = ..., range_s: typing.Union[str, bytes, bytearray, None] = ..., chromaloc: typing.Optional[int] = ..., chromaloc_s: typing.Union[str, bytes, bytearray, None] = ..., matrix_in: typing.Optional[int] = ..., matrix_in_s: typing.Union[str, bytes, bytearray, None] = ..., transfer_in: typing.Optional[int] = ..., transfer_in_s: typing.Union[str, bytes, bytearray, None] = ..., primaries_in: typing.Optional[int] = ..., primaries_in_s: typing.Union[str, bytes, bytearray, None] = ..., range_in: typing.Optional[int] = ..., range_in_s: typing.Union[str, bytes, bytearray, None] = ..., chromaloc_in: typing.Optional[int] = ..., chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = ..., filter_param_a: typing.Optional[float] = ..., filter_param_b: typing.Optional[float] = ..., resample_filter_uv: typing.Union[str, bytes, bytearray, None] = ..., filter_param_a_uv: typing.Optional[float] = ..., filter_param_b_uv: typing.Optional[float] = ..., dither_type: typing.Union[str, bytes, bytearray, None] = ..., cpu_type: typing.Union[str, bytes, bytearray, None] = ..., prefer_props: typing.Optional[int] = ..., src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ..., src_width: typing.Optional[float] = ..., src_height: typing.Optional[float] = ..., nominal_luminance: typing.Optional[float] = ...) -> "VideoNode": ...
    def Spline64(self, width: typing.Optional[int] = ..., height: typing.Optional[int] = ..., format: typing.Optional[int] = ..., matrix: typing.Optional[int] = ..., matrix_s: typing.Union[str, bytes, bytearray, None] = ..., transfer: typing.Optional[int] = ..., transfer_s: typing.Union[str, bytes, bytearray, None] = ..., primaries: typing.Optional[int] = ..., primaries_s: typing.Union[str, bytes, bytearray, None] = ..., range: typing.Optional[int] = ..., range_s: typing.Union[str, bytes, bytearray, None] = ..., chromaloc: typing.Optional[int] = ..., chromaloc_s: typing.Union[str, bytes, bytearray, None] = ..., matrix_in: typing.Optional[int] = ..., matrix_in_s: typing.Union[str, bytes, bytearray, None] = ..., transfer_in: typing.Optional[int] = ..., transfer_in_s: typing.Union[str, bytes, bytearray, None] = ..., primaries_in: typing.Optional[int] = ..., primaries_in_s: typing.Union[str, bytes, bytearray, None] = ..., range_in: typing.Optional[int] = ..., range_in_s: typing.Union[str, bytes, bytearray, None] = ..., chromaloc_in: typing.Optional[int] = ..., chromaloc_in_s: typing.Union[str, bytes, bytearray, None] = ..., filter_param_a: typing.Optional[float] = ..., filter_param_b: typing.Optional[float] = ..., resample_filter_uv: typing.Union[str, bytes, bytearray, None] = ..., filter_param_a_uv: typing.Optional[float] = ..., filter_param_b_uv: typing.Optional[float] = ..., dither_type: typing.Union[str, bytes, bytearray, None] = ..., cpu_type: typing.Union[str, bytes, bytearray, None] = ..., prefer_props: typing.Optional[int] = ..., src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ..., src_width: typing.Optional[float] = ..., src_height: typing.Optional[float] = ..., nominal_luminance: typing.Optional[float] = ...) -> "VideoNode": ...


class _Plugin_retinex_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def MSRCP(self, sigma: typing.Union[float, typing.Sequence[float], None] = ..., lower_thr: typing.Optional[float] = ..., upper_thr: typing.Optional[float] = ..., fulls: typing.Optional[int] = ..., fulld: typing.Optional[int] = ..., chroma_protect: typing.Optional[float] = ...) -> "VideoNode": ...
    def MSRCR(self, sigma: typing.Union[float, typing.Sequence[float], None] = ..., lower_thr: typing.Optional[float] = ..., upper_thr: typing.Optional[float] = ..., fulls: typing.Optional[int] = ..., fulld: typing.Optional[int] = ..., restore: typing.Optional[float] = ...) -> "VideoNode": ...


class _Plugin_srmdnv_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def SRMD(self, scale: typing.Optional[int] = ..., noise: typing.Optional[int] = ..., tilesize_x: typing.Optional[int] = ..., tilesize_y: typing.Optional[int] = ..., gpu_id: typing.Optional[int] = ..., gpu_thread: typing.Optional[int] = ..., tta: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_std_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def AddBorders(self, left: typing.Optional[int] = ..., right: typing.Optional[int] = ..., top: typing.Optional[int] = ..., bottom: typing.Optional[int] = ..., color: typing.Union[float, typing.Sequence[float], None] = ...) -> "VideoNode": ...
    def AssumeFPS(self, src: typing.Optional["VideoNode"] = ..., fpsnum: typing.Optional[int] = ..., fpsden: typing.Optional[int] = ...) -> "VideoNode": ...
    def AverageFrames(self, weights: typing.Union[float, typing.Sequence[float]], scale: typing.Optional[float] = ..., scenechange: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def Binarize(self, threshold: typing.Union[float, typing.Sequence[float], None] = ..., v0: typing.Union[float, typing.Sequence[float], None] = ..., v1: typing.Union[float, typing.Sequence[float], None] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def BinarizeMask(self, threshold: typing.Union[float, typing.Sequence[float], None] = ..., v0: typing.Union[float, typing.Sequence[float], None] = ..., v1: typing.Union[float, typing.Sequence[float], None] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def BlankClip(self, width: typing.Optional[int] = ..., height: typing.Optional[int] = ..., format: typing.Optional[int] = ..., length: typing.Optional[int] = ..., fpsnum: typing.Optional[int] = ..., fpsden: typing.Optional[int] = ..., color: typing.Union[float, typing.Sequence[float], None] = ..., keep: typing.Optional[int] = ...) -> "VideoNode": ...
    def BoxBlur(self, planes: typing.Union[int, typing.Sequence[int], None] = ..., hradius: typing.Optional[int] = ..., hpasses: typing.Optional[int] = ..., vradius: typing.Optional[int] = ..., vpasses: typing.Optional[int] = ...) -> "VideoNode": ...
    def Cache(self, size: typing.Optional[int] = ..., fixed: typing.Optional[int] = ..., make_linear: typing.Optional[int] = ...) -> "VideoNode": ...
    def ClipToProp(self, mclip: "VideoNode", prop: typing.Union[str, bytes, bytearray, None] = ...) -> "VideoNode": ...
    def Convolution(self, matrix: typing.Union[float, typing.Sequence[float]], bias: typing.Optional[float] = ..., divisor: typing.Optional[float] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., saturate: typing.Optional[int] = ..., mode: typing.Union[str, bytes, bytearray, None] = ...) -> "VideoNode": ...
    def CopyFrameProps(self, prop_src: "VideoNode") -> "VideoNode": ...
    def Crop(self, left: typing.Optional[int] = ..., right: typing.Optional[int] = ..., top: typing.Optional[int] = ..., bottom: typing.Optional[int] = ...) -> "VideoNode": ...
    def CropAbs(self, width: int, height: int, left: typing.Optional[int] = ..., top: typing.Optional[int] = ..., x: typing.Optional[int] = ..., y: typing.Optional[int] = ...) -> "VideoNode": ...
    def CropRel(self, left: typing.Optional[int] = ..., right: typing.Optional[int] = ..., top: typing.Optional[int] = ..., bottom: typing.Optional[int] = ...) -> "VideoNode": ...
    def Deflate(self, planes: typing.Union[int, typing.Sequence[int], None] = ..., threshold: typing.Optional[float] = ...) -> "VideoNode": ...
    def DeleteFrames(self, frames: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def DoubleWeave(self, tff: typing.Optional[int] = ...) -> "VideoNode": ...
    def DuplicateFrames(self, frames: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def Expr(self, expr: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]]], format: typing.Optional[int] = ...) -> "VideoNode": ...
    def FlipHorizontal(self) -> "VideoNode": ...
    def FlipVertical(self) -> "VideoNode": ...
    def FrameEval(self, eval: typing.Callable[..., typing.Any], prop_src: typing.Union["VideoNode", typing.Sequence["VideoNode"], None] = ..., clip_src: typing.Union["VideoNode", typing.Sequence["VideoNode"], None] = ...) -> "VideoNode": ...
    def FreezeFrames(self, first: typing.Union[int, typing.Sequence[int]], last: typing.Union[int, typing.Sequence[int]], replacement: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def Inflate(self, planes: typing.Union[int, typing.Sequence[int], None] = ..., threshold: typing.Optional[float] = ...) -> "VideoNode": ...
    def Interleave(self, extend: typing.Optional[int] = ..., mismatch: typing.Optional[int] = ..., modify_duration: typing.Optional[int] = ...) -> "VideoNode": ...
    def Invert(self, planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def InvertMask(self, planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def Levels(self, min_in: typing.Union[float, typing.Sequence[float], None] = ..., max_in: typing.Union[float, typing.Sequence[float], None] = ..., gamma: typing.Union[float, typing.Sequence[float], None] = ..., min_out: typing.Union[float, typing.Sequence[float], None] = ..., max_out: typing.Union[float, typing.Sequence[float], None] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def Limiter(self, min: typing.Union[float, typing.Sequence[float], None] = ..., max: typing.Union[float, typing.Sequence[float], None] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def Loop(self, times: typing.Optional[int] = ...) -> "VideoNode": ...
    def Lut(self, planes: typing.Union[int, typing.Sequence[int], None] = ..., lut: typing.Union[int, typing.Sequence[int], None] = ..., lutf: typing.Union[float, typing.Sequence[float], None] = ..., function: typing.Optional[typing.Callable[..., typing.Any]] = ..., bits: typing.Optional[int] = ..., floatout: typing.Optional[int] = ...) -> "VideoNode": ...
    def Lut2(self, clipb: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = ..., lut: typing.Union[int, typing.Sequence[int], None] = ..., lutf: typing.Union[float, typing.Sequence[float], None] = ..., function: typing.Optional[typing.Callable[..., typing.Any]] = ..., bits: typing.Optional[int] = ..., floatout: typing.Optional[int] = ...) -> "VideoNode": ...
    def MakeDiff(self, clipb: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def MaskedMerge(self, clipb: "VideoNode", mask: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = ..., first_plane: typing.Optional[int] = ..., premultiplied: typing.Optional[int] = ...) -> "VideoNode": ...
    def Maximum(self, planes: typing.Union[int, typing.Sequence[int], None] = ..., threshold: typing.Optional[float] = ..., coordinates: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def Median(self, planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def Merge(self, clipb: "VideoNode", weight: typing.Union[float, typing.Sequence[float], None] = ...) -> "VideoNode": ...
    def MergeDiff(self, clipb: "VideoNode", planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def Minimum(self, planes: typing.Union[int, typing.Sequence[int], None] = ..., threshold: typing.Optional[float] = ..., coordinates: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def ModifyFrame(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"]], selector: typing.Callable[..., typing.Any]) -> "VideoNode": ...
    def PEMVerifier(self, upper: typing.Union[float, typing.Sequence[float], None] = ..., lower: typing.Union[float, typing.Sequence[float], None] = ...) -> "VideoNode": ...
    def PlaneStats(self, clipb: typing.Optional["VideoNode"] = ..., plane: typing.Optional[int] = ..., prop: typing.Union[str, bytes, bytearray, None] = ...) -> "VideoNode": ...
    def PreMultiply(self, alpha: "VideoNode") -> "VideoNode": ...
    def Prewitt(self, planes: typing.Union[int, typing.Sequence[int], None] = ..., scale: typing.Optional[float] = ...) -> "VideoNode": ...
    def PropToClip(self, prop: typing.Union[str, bytes, bytearray, None] = ...) -> "VideoNode": ...
    def RemoveFrameProps(self, props: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = ...) -> "VideoNode": ...
    def Reverse(self) -> "VideoNode": ...
    def SelectEvery(self, cycle: int, offsets: typing.Union[int, typing.Sequence[int]], modify_duration: typing.Optional[int] = ...) -> "VideoNode": ...
    def SeparateFields(self, tff: typing.Optional[int] = ..., modify_duration: typing.Optional[int] = ...) -> "VideoNode": ...
    def SetFieldBased(self, value: int) -> "VideoNode": ...
    def SetFrameProp(self, prop: typing.Union[str, bytes, bytearray], intval: typing.Union[int, typing.Sequence[int], None] = ..., floatval: typing.Union[float, typing.Sequence[float], None] = ..., data: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = ...) -> "VideoNode": ...
    def SetFrameProps(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Optional["VideoNode"]: ...
    def SetVideoCache(self, mode: typing.Optional[int] = ..., fixedsize: typing.Optional[int] = ..., maxsize: typing.Optional[int] = ..., maxhistory: typing.Optional[int] = ...) -> "VideoNode": ...
    def ShufflePlanes(self, planes: typing.Union[int, typing.Sequence[int]], colorfamily: int) -> "VideoNode": ...
    def Sobel(self, planes: typing.Union[int, typing.Sequence[int], None] = ..., scale: typing.Optional[float] = ...) -> "VideoNode": ...
    def Splice(self, mismatch: typing.Optional[int] = ...) -> "VideoNode": ...
    def SplitPlanes(self) -> "VideoNode": ...
    def StackHorizontal(self) -> "VideoNode": ...
    def StackVertical(self) -> "VideoNode": ...
    def Transpose(self) -> "VideoNode": ...
    def Trim(self, first: typing.Optional[int] = ..., last: typing.Optional[int] = ..., length: typing.Optional[int] = ...) -> "VideoNode": ...
    def Turn180(self) -> "VideoNode": ...


class _Plugin_text_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def ClipInfo(self, alignment: typing.Optional[int] = ..., scale: typing.Optional[int] = ...) -> "VideoNode": ...
    def CoreInfo(self, alignment: typing.Optional[int] = ..., scale: typing.Optional[int] = ...) -> "VideoNode": ...
    def FrameNum(self, alignment: typing.Optional[int] = ..., scale: typing.Optional[int] = ...) -> "VideoNode": ...
    def FrameProps(self, props: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = ..., alignment: typing.Optional[int] = ..., scale: typing.Optional[int] = ...) -> "VideoNode": ...
    def Text(self, text: typing.Union[str, bytes, bytearray], alignment: typing.Optional[int] = ..., scale: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_placebo_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Deband(self, planes: typing.Optional[int] = ..., iterations: typing.Optional[int] = ..., threshold: typing.Optional[float] = ..., radius: typing.Optional[float] = ..., grain: typing.Optional[float] = ..., dither: typing.Optional[int] = ..., dither_algo: typing.Optional[int] = ..., renderer_api: typing.Optional[int] = ...) -> "VideoNode": ...
    def Resample(self, width: int, height: int, filter: typing.Union[str, bytes, bytearray, None] = ..., clamp: typing.Optional[float] = ..., blur: typing.Optional[float] = ..., taper: typing.Optional[float] = ..., radius: typing.Optional[float] = ..., param1: typing.Optional[float] = ..., param2: typing.Optional[float] = ..., sx: typing.Optional[float] = ..., sy: typing.Optional[float] = ..., antiring: typing.Optional[float] = ..., lut_entries: typing.Optional[int] = ..., cutoff: typing.Optional[float] = ..., sigmoidize: typing.Optional[int] = ..., sigmoid_center: typing.Optional[float] = ..., sigmoid_slope: typing.Optional[float] = ..., linearize: typing.Optional[int] = ..., trc: typing.Optional[int] = ...) -> "VideoNode": ...
    def Shader(self, shader: typing.Union[str, bytes, bytearray], width: typing.Optional[int] = ..., height: typing.Optional[int] = ..., chroma_loc: typing.Optional[int] = ..., matrix: typing.Optional[int] = ..., trc: typing.Optional[int] = ..., linearize: typing.Optional[int] = ..., sigmoidize: typing.Optional[int] = ..., sigmoid_center: typing.Optional[float] = ..., sigmoid_slope: typing.Optional[float] = ..., lut_entries: typing.Optional[int] = ..., antiring: typing.Optional[float] = ..., filter: typing.Union[str, bytes, bytearray, None] = ..., clamp: typing.Optional[float] = ..., blur: typing.Optional[float] = ..., taper: typing.Optional[float] = ..., radius: typing.Optional[float] = ..., param1: typing.Optional[float] = ..., param2: typing.Optional[float] = ...) -> "VideoNode": ...
    def Tonemap(self, srcp: typing.Optional[int] = ..., srct: typing.Optional[int] = ..., srcl: typing.Optional[int] = ..., src_peak: typing.Optional[float] = ..., src_avg: typing.Optional[float] = ..., src_scale: typing.Optional[float] = ..., dstp: typing.Optional[int] = ..., dstt: typing.Optional[int] = ..., dstl: typing.Optional[int] = ..., dst_peak: typing.Optional[float] = ..., dst_avg: typing.Optional[float] = ..., dst_scale: typing.Optional[float] = ..., dynamic_peak_detection: typing.Optional[int] = ..., smoothing_period: typing.Optional[float] = ..., scene_threshold_low: typing.Optional[float] = ..., scene_threshold_high: typing.Optional[float] = ..., intent: typing.Optional[int] = ..., tone_mapping_algo: typing.Optional[int] = ..., tone_mapping_param: typing.Optional[float] = ..., desaturation_strength: typing.Optional[float] = ..., desaturation_exponent: typing.Optional[float] = ..., desaturation_base: typing.Optional[float] = ..., max_boost: typing.Optional[float] = ..., gamut_warning: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_bm3dcuda_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def BM3D(self, ref: typing.Optional["VideoNode"] = ..., sigma: typing.Union[float, typing.Sequence[float], None] = ..., block_step: typing.Union[int, typing.Sequence[int], None] = ..., bm_range: typing.Union[int, typing.Sequence[int], None] = ..., radius: typing.Optional[int] = ..., ps_num: typing.Union[int, typing.Sequence[int], None] = ..., ps_range: typing.Union[int, typing.Sequence[int], None] = ..., chroma: typing.Optional[int] = ..., device_id: typing.Optional[int] = ..., fast: typing.Optional[int] = ..., extractor_exp: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_dpid_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Dpid(self, width: typing.Optional[int] = ..., height: typing.Optional[int] = ..., lambda_: typing.Union[float, typing.Sequence[float], None] = ..., src_left: typing.Union[float, typing.Sequence[float], None] = ..., src_top: typing.Union[float, typing.Sequence[float], None] = ..., read_chromaloc: typing.Optional[int] = ...) -> "VideoNode": ...
    def DpidRaw(self, clip2: "VideoNode", lambda_: typing.Union[float, typing.Sequence[float], None] = ..., src_left: typing.Union[float, typing.Sequence[float], None] = ..., src_top: typing.Union[float, typing.Sequence[float], None] = ..., read_chromaloc: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...


class _Plugin_tla_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def TempLinearApproximate(self, radius: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., gamma: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_dpriv_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Reconstruct(self, stats: "VideoNode", radius: int, speed: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_average_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Mean(self, preset: typing.Optional[int] = ..., discard: typing.Optional[int] = ...) -> "VideoNode": ...
    def Median(self) -> "VideoNode": ...


class _Plugin_fmtc_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def bitdepth(self, csp: typing.Optional[int] = ..., bits: typing.Optional[int] = ..., flt: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., fulls: typing.Optional[int] = ..., fulld: typing.Optional[int] = ..., dmode: typing.Optional[int] = ..., ampo: typing.Optional[float] = ..., ampn: typing.Optional[float] = ..., dyn: typing.Optional[int] = ..., staticnoise: typing.Optional[int] = ..., cpuopt: typing.Optional[int] = ..., patsize: typing.Optional[int] = ...) -> "VideoNode": ...
    def histluma(self, full: typing.Optional[int] = ..., amp: typing.Optional[int] = ...) -> "VideoNode": ...
    def matrix(self, mat: typing.Union[str, bytes, bytearray, None] = ..., mats: typing.Union[str, bytes, bytearray, None] = ..., matd: typing.Union[str, bytes, bytearray, None] = ..., fulls: typing.Optional[int] = ..., fulld: typing.Optional[int] = ..., coef: typing.Union[float, typing.Sequence[float], None] = ..., csp: typing.Optional[int] = ..., col_fam: typing.Optional[int] = ..., bits: typing.Optional[int] = ..., singleout: typing.Optional[int] = ..., cpuopt: typing.Optional[int] = ...) -> "VideoNode": ...
    def matrix2020cl(self, full: typing.Optional[int] = ..., csp: typing.Optional[int] = ..., bits: typing.Optional[int] = ..., cpuopt: typing.Optional[int] = ...) -> "VideoNode": ...
    def nativetostack16(self) -> "VideoNode": ...
    def primaries(self, rs: typing.Union[float, typing.Sequence[float], None] = ..., gs: typing.Union[float, typing.Sequence[float], None] = ..., bs: typing.Union[float, typing.Sequence[float], None] = ..., ws: typing.Union[float, typing.Sequence[float], None] = ..., rd: typing.Union[float, typing.Sequence[float], None] = ..., gd: typing.Union[float, typing.Sequence[float], None] = ..., bd: typing.Union[float, typing.Sequence[float], None] = ..., wd: typing.Union[float, typing.Sequence[float], None] = ..., prims: typing.Union[str, bytes, bytearray, None] = ..., primd: typing.Union[str, bytes, bytearray, None] = ..., cpuopt: typing.Optional[int] = ...) -> "VideoNode": ...
    def resample(self, w: typing.Optional[int] = ..., h: typing.Optional[int] = ..., sx: typing.Union[float, typing.Sequence[float], None] = ..., sy: typing.Union[float, typing.Sequence[float], None] = ..., sw: typing.Union[float, typing.Sequence[float], None] = ..., sh: typing.Union[float, typing.Sequence[float], None] = ..., scale: typing.Optional[float] = ..., scaleh: typing.Optional[float] = ..., scalev: typing.Optional[float] = ..., kernel: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = ..., kernelh: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = ..., kernelv: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = ..., impulse: typing.Union[float, typing.Sequence[float], None] = ..., impulseh: typing.Union[float, typing.Sequence[float], None] = ..., impulsev: typing.Union[float, typing.Sequence[float], None] = ..., taps: typing.Union[int, typing.Sequence[int], None] = ..., tapsh: typing.Union[int, typing.Sequence[int], None] = ..., tapsv: typing.Union[int, typing.Sequence[int], None] = ..., a1: typing.Union[float, typing.Sequence[float], None] = ..., a2: typing.Union[float, typing.Sequence[float], None] = ..., a3: typing.Union[float, typing.Sequence[float], None] = ..., kovrspl: typing.Union[int, typing.Sequence[int], None] = ..., fh: typing.Union[float, typing.Sequence[float], None] = ..., fv: typing.Union[float, typing.Sequence[float], None] = ..., cnorm: typing.Union[int, typing.Sequence[int], None] = ..., totalh: typing.Union[float, typing.Sequence[float], None] = ..., totalv: typing.Union[float, typing.Sequence[float], None] = ..., invks: typing.Union[int, typing.Sequence[int], None] = ..., invksh: typing.Union[int, typing.Sequence[int], None] = ..., invksv: typing.Union[int, typing.Sequence[int], None] = ..., invkstaps: typing.Union[int, typing.Sequence[int], None] = ..., invkstapsh: typing.Union[int, typing.Sequence[int], None] = ..., invkstapsv: typing.Union[int, typing.Sequence[int], None] = ..., csp: typing.Optional[int] = ..., css: typing.Union[str, bytes, bytearray, None] = ..., planes: typing.Union[float, typing.Sequence[float], None] = ..., fulls: typing.Optional[int] = ..., fulld: typing.Optional[int] = ..., center: typing.Union[int, typing.Sequence[int], None] = ..., cplace: typing.Union[str, bytes, bytearray, None] = ..., cplaces: typing.Union[str, bytes, bytearray, None] = ..., cplaced: typing.Union[str, bytes, bytearray, None] = ..., interlaced: typing.Optional[int] = ..., interlacedd: typing.Optional[int] = ..., tff: typing.Optional[int] = ..., tffd: typing.Optional[int] = ..., flt: typing.Optional[int] = ..., cpuopt: typing.Optional[int] = ...) -> "VideoNode": ...
    def stack16tonative(self) -> "VideoNode": ...
    def transfer(self, transs: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = ..., transd: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = ..., cont: typing.Optional[float] = ..., gcor: typing.Optional[float] = ..., bits: typing.Optional[int] = ..., flt: typing.Optional[int] = ..., fulls: typing.Optional[int] = ..., fulld: typing.Optional[int] = ..., cpuopt: typing.Optional[int] = ..., blacklvl: typing.Optional[float] = ...) -> "VideoNode": ...


class _Plugin_delogohd_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def AddlogoHD(self, logofile: typing.Union[str, bytes, bytearray], logoname: typing.Union[str, bytes, bytearray, None] = ..., left: typing.Optional[int] = ..., top: typing.Optional[int] = ..., start: typing.Optional[int] = ..., end: typing.Optional[int] = ..., fadein: typing.Optional[int] = ..., fadeout: typing.Optional[int] = ..., mono: typing.Optional[int] = ..., cutoff: typing.Optional[int] = ...) -> "VideoNode": ...
    def DelogoHD(self, logofile: typing.Union[str, bytes, bytearray], logoname: typing.Union[str, bytes, bytearray, None] = ..., left: typing.Optional[int] = ..., top: typing.Optional[int] = ..., start: typing.Optional[int] = ..., end: typing.Optional[int] = ..., fadein: typing.Optional[int] = ..., fadeout: typing.Optional[int] = ..., mono: typing.Optional[int] = ..., cutoff: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_neo_f3kdb_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Deband(self, range: typing.Optional[int] = ..., y: typing.Optional[int] = ..., cb: typing.Optional[int] = ..., cr: typing.Optional[int] = ..., grainy: typing.Optional[int] = ..., grainc: typing.Optional[int] = ..., sample_mode: typing.Optional[int] = ..., seed: typing.Optional[int] = ..., blur_first: typing.Optional[int] = ..., dynamic_grain: typing.Optional[int] = ..., opt: typing.Optional[int] = ..., mt: typing.Optional[int] = ..., dither_algo: typing.Optional[int] = ..., keep_tv_range: typing.Optional[int] = ..., output_depth: typing.Optional[int] = ..., random_algo_ref: typing.Optional[int] = ..., random_algo_grain: typing.Optional[int] = ..., random_param_ref: typing.Optional[float] = ..., random_param_grain: typing.Optional[float] = ..., preset: typing.Union[str, bytes, bytearray, None] = ...) -> "VideoNode": ...


class _Plugin_neo_fft3d_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def FFT3D(self, sigma: typing.Optional[float] = ..., beta: typing.Optional[float] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., bw: typing.Optional[int] = ..., bh: typing.Optional[int] = ..., bt: typing.Optional[int] = ..., ow: typing.Optional[int] = ..., oh: typing.Optional[int] = ..., kratio: typing.Optional[float] = ..., sharpen: typing.Optional[float] = ..., scutoff: typing.Optional[float] = ..., svr: typing.Optional[float] = ..., smin: typing.Optional[float] = ..., smax: typing.Optional[float] = ..., measure: typing.Optional[int] = ..., interlaced: typing.Optional[int] = ..., wintype: typing.Optional[int] = ..., pframe: typing.Optional[int] = ..., px: typing.Optional[int] = ..., py: typing.Optional[int] = ..., pshow: typing.Optional[int] = ..., pcutoff: typing.Optional[float] = ..., pfactor: typing.Optional[float] = ..., sigma2: typing.Optional[float] = ..., sigma3: typing.Optional[float] = ..., sigma4: typing.Optional[float] = ..., degrid: typing.Optional[float] = ..., dehalo: typing.Optional[float] = ..., hr: typing.Optional[float] = ..., ht: typing.Optional[float] = ..., l: typing.Optional[int] = ..., t: typing.Optional[int] = ..., r: typing.Optional[int] = ..., b: typing.Optional[int] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_neo_vd_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def VagueDenoiser(self, threshold: typing.Optional[float] = ..., method: typing.Optional[int] = ..., nsteps: typing.Optional[int] = ..., percent: typing.Optional[float] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., opt: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_vcmod_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def amp(self, *args: typing.Any, **kwargs: typing.Any) -> typing.Optional["VideoNode"]: ...
    def fan(self, span: typing.Optional[int] = ..., edge: typing.Optional[int] = ..., plus: typing.Optional[int] = ..., minus: typing.Optional[int] = ..., uv: typing.Optional[int] = ...) -> "VideoNode": ...
    def gBlur(self, ksize: typing.Optional[int] = ..., sd: typing.Optional[float] = ...) -> "VideoNode": ...
    def hist(self, clipm: typing.Optional["VideoNode"] = ..., type: typing.Optional[int] = ..., table: typing.Union[int, typing.Sequence[int], None] = ..., mf: typing.Optional[int] = ..., window: typing.Optional[int] = ..., limit: typing.Optional[int] = ...) -> "VideoNode": ...
    def mBlur(self, type: typing.Optional[int] = ..., x: typing.Optional[int] = ..., y: typing.Optional[int] = ...) -> "VideoNode": ...
    def median(self, maxgrid: typing.Optional[int] = ..., plane: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def neural(self, txt: typing.Union[str, bytes, bytearray, None] = ..., fname: typing.Union[str, bytes, bytearray, None] = ..., tclip: typing.Optional["VideoNode"] = ..., xpts: typing.Optional[int] = ..., ypts: typing.Optional[int] = ..., tlx: typing.Optional[int] = ..., tty: typing.Optional[int] = ..., trx: typing.Optional[int] = ..., tby: typing.Optional[int] = ..., iter: typing.Optional[int] = ..., bestof: typing.Optional[int] = ..., wset: typing.Optional[int] = ..., rgb: typing.Optional[int] = ...) -> "VideoNode": ...
    def saltPepper(self, planes: typing.Union[int, typing.Sequence[int], None] = ..., tol: typing.Optional[int] = ..., avg: typing.Optional[int] = ...) -> "VideoNode": ...
    def variance(self, lx: int, wd: int, ty: int, ht: int, fn: typing.Optional[int] = ..., uv: typing.Optional[int] = ..., xgrid: typing.Optional[int] = ..., ygrid: typing.Optional[int] = ...) -> "VideoNode": ...
    def veed(self, str: typing.Optional[int] = ..., rad: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., plimit: typing.Union[int, typing.Sequence[int], None] = ..., mlimit: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...


class _Plugin_akarin_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def DLISR(self, scale: typing.Optional[int] = ...) -> "VideoNode": ...
    def Expr(self, expr: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]]], format: typing.Optional[int] = ..., opt: typing.Optional[int] = ..., boundary: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_bilateral_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Bilateral(self, ref: typing.Optional["VideoNode"] = ..., sigmaS: typing.Union[float, typing.Sequence[float], None] = ..., sigmaR: typing.Union[float, typing.Sequence[float], None] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., algorithm: typing.Union[int, typing.Sequence[int], None] = ..., PBFICnum: typing.Union[int, typing.Sequence[int], None] = ...) -> "VideoNode": ...
    def Gaussian(self, sigma: typing.Union[float, typing.Sequence[float], None] = ..., sigmaV: typing.Union[float, typing.Sequence[float], None] = ...) -> "VideoNode": ...


class _Plugin_adg_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Mask(self, luma_scaling: typing.Optional[float] = ...) -> "VideoNode": ...


class _Plugin_w2xnvk_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Waifu2x(self, noise: typing.Optional[int] = ..., scale: typing.Optional[int] = ..., model: typing.Optional[int] = ..., tile_size: typing.Optional[int] = ..., gpu_id: typing.Optional[int] = ..., gpu_thread: typing.Optional[int] = ..., precision: typing.Optional[int] = ..., tile_size_w: typing.Optional[int] = ..., tile_size_h: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_f3kdb_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Deband(self, range: typing.Optional[int] = ..., y: typing.Optional[int] = ..., cb: typing.Optional[int] = ..., cr: typing.Optional[int] = ..., grainy: typing.Optional[int] = ..., grainc: typing.Optional[int] = ..., sample_mode: typing.Optional[int] = ..., seed: typing.Optional[int] = ..., blur_first: typing.Optional[int] = ..., dynamic_grain: typing.Optional[int] = ..., opt: typing.Optional[int] = ..., dither_algo: typing.Optional[int] = ..., keep_tv_range: typing.Optional[int] = ..., output_depth: typing.Optional[int] = ..., random_algo_ref: typing.Optional[int] = ..., random_algo_grain: typing.Optional[int] = ..., random_param_ref: typing.Optional[float] = ..., random_param_grain: typing.Optional[float] = ..., preset: typing.Union[str, bytes, bytearray, None] = ...) -> "VideoNode": ...


class _Plugin_fft3dfilter_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def FFT3DFilter(self, sigma: typing.Optional[float] = ..., beta: typing.Optional[float] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., bw: typing.Optional[int] = ..., bh: typing.Optional[int] = ..., bt: typing.Optional[int] = ..., ow: typing.Optional[int] = ..., oh: typing.Optional[int] = ..., kratio: typing.Optional[float] = ..., sharpen: typing.Optional[float] = ..., scutoff: typing.Optional[float] = ..., svr: typing.Optional[float] = ..., smin: typing.Optional[float] = ..., smax: typing.Optional[float] = ..., measure: typing.Optional[int] = ..., interlaced: typing.Optional[int] = ..., wintype: typing.Optional[int] = ..., pframe: typing.Optional[int] = ..., px: typing.Optional[int] = ..., py: typing.Optional[int] = ..., pshow: typing.Optional[int] = ..., pcutoff: typing.Optional[float] = ..., pfactor: typing.Optional[float] = ..., sigma2: typing.Optional[float] = ..., sigma3: typing.Optional[float] = ..., sigma4: typing.Optional[float] = ..., degrid: typing.Optional[float] = ..., dehalo: typing.Optional[float] = ..., hr: typing.Optional[float] = ..., ht: typing.Optional[float] = ..., ncpu: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_descale_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Debicubic(self, width: int, height: int, b: typing.Optional[float] = ..., c: typing.Optional[float] = ..., src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ..., src_width: typing.Optional[float] = ..., src_height: typing.Optional[float] = ...) -> "VideoNode": ...
    def Debilinear(self, width: int, height: int, src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ..., src_width: typing.Optional[float] = ..., src_height: typing.Optional[float] = ...) -> "VideoNode": ...
    def Delanczos(self, width: int, height: int, taps: typing.Optional[int] = ..., src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ..., src_width: typing.Optional[float] = ..., src_height: typing.Optional[float] = ...) -> "VideoNode": ...
    def Despline16(self, width: int, height: int, src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ..., src_width: typing.Optional[float] = ..., src_height: typing.Optional[float] = ...) -> "VideoNode": ...
    def Despline36(self, width: int, height: int, src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ..., src_width: typing.Optional[float] = ..., src_height: typing.Optional[float] = ...) -> "VideoNode": ...
    def Despline64(self, width: int, height: int, src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ..., src_width: typing.Optional[float] = ..., src_height: typing.Optional[float] = ...) -> "VideoNode": ...


class _Plugin_descale_getnative_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Debicubic(self, width: int, height: int, b: typing.Optional[float] = ..., c: typing.Optional[float] = ..., src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ...) -> "VideoNode": ...
    def Debilinear(self, width: int, height: int, src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ...) -> "VideoNode": ...
    def Delanczos(self, width: int, height: int, taps: typing.Optional[int] = ..., src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ...) -> "VideoNode": ...
    def Despline16(self, width: int, height: int, src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ...) -> "VideoNode": ...
    def Despline36(self, width: int, height: int, src_left: typing.Optional[float] = ..., src_top: typing.Optional[float] = ...) -> "VideoNode": ...


class _Plugin_mx_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Predict(self, symbol: typing.Union[str, bytes, bytearray], param: typing.Union[str, bytes, bytearray], patch_w: typing.Optional[int] = ..., patch_h: typing.Optional[int] = ..., scale: typing.Optional[int] = ..., output_w: typing.Optional[int] = ..., output_h: typing.Optional[int] = ..., frame_w: typing.Optional[int] = ..., frame_h: typing.Optional[int] = ..., step_w: typing.Optional[int] = ..., step_h: typing.Optional[int] = ..., outstep_w: typing.Optional[int] = ..., outstep_h: typing.Optional[int] = ..., output_format: typing.Optional[int] = ..., input_name: typing.Union[str, bytes, bytearray, None] = ..., ctx: typing.Optional[int] = ..., dev_id: typing.Optional[int] = ...) -> "VideoNode": ...


class _Plugin_avsw_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def Eval(self, clips: typing.Union["VideoNode", typing.Sequence["VideoNode"], None] = ..., clip_names: typing.Union[str, bytes, bytearray, typing.Sequence[typing.Union[str, bytes, bytearray]], None] = ..., avisynth: typing.Union[str, bytes, bytearray, None] = ..., slave: typing.Union[str, bytes, bytearray, None] = ..., slave_log: typing.Union[str, bytes, bytearray, None] = ...) -> "VideoNode": ...


class _Plugin_znedi3_VideoNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def nnedi3(self, field: int, dh: typing.Optional[int] = ..., planes: typing.Union[int, typing.Sequence[int], None] = ..., nsize: typing.Optional[int] = ..., nns: typing.Optional[int] = ..., qual: typing.Optional[int] = ..., etype: typing.Optional[int] = ..., pscrn: typing.Optional[int] = ..., opt: typing.Optional[int] = ..., int16_prescreener: typing.Optional[int] = ..., int16_predictor: typing.Optional[int] = ..., exp: typing.Optional[int] = ..., show_mask: typing.Optional[int] = ..., x_nnedi3_weights_bin: typing.Union[str, bytes, bytearray, None] = ..., x_cpu: typing.Union[str, bytes, bytearray, None] = ...) -> "VideoNode": ...


class _Plugin_std_AudioNode_Bound(Plugin):
    """
    This class implements the module definitions for the corresponding VapourSynth plugin.
    This class cannot be imported.
    """
    def AssumeSampleRate(self, src: typing.Optional["AudioNode"] = ..., samplerate: typing.Optional[int] = ...) -> "VideoNode": ...
    def AudioGain(self, gain: typing.Union[float, typing.Sequence[float], None] = ...) -> "VideoNode": ...
    def AudioLoop(self, times: typing.Optional[int] = ...) -> "VideoNode": ...
    def AudioMix(self, matrix: typing.Union[float, typing.Sequence[float]], channels_out: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def AudioReverse(self) -> "VideoNode": ...
    def AudioSplice(self) -> "VideoNode": ...
    def AudioTrim(self, first: typing.Optional[int] = ..., last: typing.Optional[int] = ..., length: typing.Optional[int] = ...) -> "VideoNode": ...
    def BlankAudio(self, channels: typing.Optional[int] = ..., bits: typing.Optional[int] = ..., sampletype: typing.Optional[int] = ..., samplerate: typing.Optional[int] = ..., length: typing.Optional[int] = ..., keep: typing.Optional[int] = ...) -> "VideoNode": ...
    def SetAudioCache(self, mode: typing.Optional[int] = ..., fixedsize: typing.Optional[int] = ..., maxsize: typing.Optional[int] = ..., maxhistory: typing.Optional[int] = ...) -> "VideoNode": ...
    def ShuffleChannels(self, channels_in: typing.Union[int, typing.Sequence[int]], channels_out: typing.Union[int, typing.Sequence[int]]) -> "VideoNode": ...
    def SplitChannels(self) -> "VideoNode": ...




class VideoNode:
    @property
    def acrop(self) -> _Plugin_acrop_VideoNode_Bound:
        """
        VapourSynth Auto Crop
        """
    @property
    def ocr(self) -> _Plugin_ocr_VideoNode_Bound:
        """
        Tesseract OCR Filter
        """
    @property
    def remap(self) -> _Plugin_remap_VideoNode_Bound:
        """
        Remaps frame indices based on a file/string
        """
    @property
    def comb(self) -> _Plugin_comb_VideoNode_Bound:
        """
        comb filters v0.0.1
        """
    @property
    def focus2(self) -> _Plugin_focus2_VideoNode_Bound:
        """
        VapourSynth TemporalSoften Filter v1
        """
    @property
    def knlm(self) -> _Plugin_knlm_VideoNode_Bound:
        """
        KNLMeansCL for VapourSynth
        """
    @property
    def ftf(self) -> _Plugin_ftf_VideoNode_Bound:
        """
        Fix Telecined Fades
        """
    @property
    def nnedi3(self) -> _Plugin_nnedi3_VideoNode_Bound:
        """
        Neural network edge directed interpolation (3rd gen.), v12
        """
    @property
    def libp2p(self) -> _Plugin_libp2p_VideoNode_Bound:
        """
        libp2p rgb formats packer/unpacker
        """
    @property
    def ccd(self) -> _Plugin_ccd_VideoNode_Bound:
        """
        chroma denoiser
        """
    @property
    def grain(self) -> _Plugin_grain_VideoNode_Bound:
        """
        Add some correlated color gaussian noise
        """
    @property
    def cas(self) -> _Plugin_cas_VideoNode_Bound:
        """
        Contrast Adaptive Sharpening
        """
    @property
    def ctmf(self) -> _Plugin_ctmf_VideoNode_Bound:
        """
        Constant Time Median Filtering
        """
    @property
    def dctf(self) -> _Plugin_dctf_VideoNode_Bound:
        """
        DCT/IDCT Frequency Suppressor
        """
    @property
    def deblock(self) -> _Plugin_deblock_VideoNode_Bound:
        """
        It does a deblocking of the picture, using the deblocking filter of h264
        """
    @property
    def dfttest(self) -> _Plugin_dfttest_VideoNode_Bound:
        """
        2D/3D frequency domain denoiser
        """
    @property
    def eedi2(self) -> _Plugin_eedi2_VideoNode_Bound:
        """
        EEDI2
        """
    @property
    def eedi3m(self) -> _Plugin_eedi3m_VideoNode_Bound:
        """
        Enhanced Edge Directed Interpolation 3
        """
    @property
    def lghost(self) -> _Plugin_lghost_VideoNode_Bound:
        """
        Ghost Reduction
        """
    @property
    def nnedi3cl(self) -> _Plugin_nnedi3cl_VideoNode_Bound:
        """
        An intra-field only deinterlacer
        """
    @property
    def tcanny(self) -> _Plugin_tcanny_VideoNode_Bound:
        """
        Build an edge map using canny edge detection
        """
    @property
    def tdm(self) -> _Plugin_tdm_VideoNode_Bound:
        """
        A bi-directionally motion adaptive deinterlacer
        """
    @property
    def ttmpsm(self) -> _Plugin_ttmpsm_VideoNode_Bound:
        """
        A basic, motion adaptive, temporal smoothing filter
        """
    @property
    def vsf(self) -> _Plugin_vsf_VideoNode_Bound:
        """
        VSFilter
        """
    @property
    def vsfm(self) -> _Plugin_vsfm_VideoNode_Bound:
        """
        VSFilterMod
        """
    @property
    def w2xc(self) -> _Plugin_w2xc_VideoNode_Bound:
        """
        Image Super-Resolution using Deep Convolutional Neural Networks
        """
    @property
    def yadifmod(self) -> _Plugin_yadifmod_VideoNode_Bound:
        """
        Modification of Fizick's yadif avisynth filter
        """
    @property
    def tonemap(self) -> _Plugin_tonemap_VideoNode_Bound:
        """
        Simple tone mapping for VapourSynth
        """
    @property
    def sangnom(self) -> _Plugin_sangnom_VideoNode_Bound:
        """
        VapourSynth Single Field Deinterlacer
        """
    @property
    def edgefixer(self) -> _Plugin_edgefixer_VideoNode_Bound:
        """
        VapourSynth edgefixer port
        """
    @property
    def warp(self) -> _Plugin_warp_VideoNode_Bound:
        """
        Sharpen images by warping
        """
    @property
    def fb(self) -> _Plugin_fb_VideoNode_Bound:
        """
        FillBorders plugin for VapourSynth
        """
    @property
    def flux(self) -> _Plugin_flux_VideoNode_Bound:
        """
        FluxSmooth plugin for VapourSynth
        """
    @property
    def hist(self) -> _Plugin_hist_VideoNode_Bound:
        """
        VapourSynth Histogram Plugin
        """
    @property
    def median(self) -> _Plugin_median_VideoNode_Bound:
        """
        Median of clips
        """
    @property
    def msmoosh(self) -> _Plugin_msmoosh_VideoNode_Bound:
        """
        MSmooth and MSharpen
        """
    @property
    def mvsf(self) -> _Plugin_mvsf_VideoNode_Bound:
        """
        MVTools Single Precision
        """
    @property
    def mv(self) -> _Plugin_mv_VideoNode_Bound:
        """
        MVTools v23
        """
    @property
    def scxvid(self) -> _Plugin_scxvid_VideoNode_Bound:
        """
        VapourSynth Scxvid Plugin
        """
    @property
    def tedgemask(self) -> _Plugin_tedgemask_VideoNode_Bound:
        """
        Edge detection plugin
        """
    @property
    def tmedian(self) -> _Plugin_tmedian_VideoNode_Bound:
        """
        Calculates temporal median
        """
    @property
    def tivtc(self) -> _Plugin_tivtc_VideoNode_Bound:
        """
        Field matching and decimation
        """
    @property
    def wwxd(self) -> _Plugin_wwxd_VideoNode_Bound:
        """
        Scene change detection approximately like Xvid's
        """
    @property
    def d2v(self) -> _Plugin_d2v_VideoNode_Bound:
        """
        D2V Source
        """
    @property
    def svp1(self) -> _Plugin_svp1_VideoNode_Bound:
        """
        SVPFlow1
        """
    @property
    def svp2(self) -> _Plugin_svp2_VideoNode_Bound:
        """
        SVPFlow2
        """
    @property
    def area(self) -> _Plugin_area_VideoNode_Bound:
        """
        area average downscaler plugin
        """
    @property
    def bm3d(self) -> _Plugin_bm3d_VideoNode_Bound:
        """
        Implementation of BM3D denoising filter for VapourSynth.
        """
    @property
    def hqdn3d(self) -> _Plugin_hqdn3d_VideoNode_Bound:
        """
        HQDn3D port as used in avisynth/mplayer
        """
    @property
    def imwri(self) -> _Plugin_imwri_VideoNode_Bound:
        """
        VapourSynth ImageMagick 7 HDRI Writer/Reader
        """
    @property
    def jinc(self) -> _Plugin_jinc_VideoNode_Bound:
        """
        VapourSynth EWA resampling
        """
    @property
    def rsnv(self) -> _Plugin_rsnv_VideoNode_Bound:
        """
        RealSR ncnn Vulkan plugin
        """
    @property
    def rgsf(self) -> _Plugin_rgsf_VideoNode_Bound:
        """
        RemoveGrain Single Precision
        """
    @property
    def rgvs(self) -> _Plugin_rgvs_VideoNode_Bound:
        """
        RemoveGrain VapourSynth Port
        """
    @property
    def resize(self) -> _Plugin_resize_VideoNode_Bound:
        """
        VapourSynth Resize
        """
    @property
    def retinex(self) -> _Plugin_retinex_VideoNode_Bound:
        """
        Implementation of Retinex algorithm for VapourSynth.
        """
    @property
    def srmdnv(self) -> _Plugin_srmdnv_VideoNode_Bound:
        """
        SRMD ncnn Vulkan plugin
        """
    @property
    def std(self) -> _Plugin_std_VideoNode_Bound:
        """
        VapourSynth Core Functions
        """
    @property
    def text(self) -> _Plugin_text_VideoNode_Bound:
        """
        VapourSynth Text
        """
    @property
    def placebo(self) -> _Plugin_placebo_VideoNode_Bound:
        """
        libplacebo plugin for VapourSynth
        """
    @property
    def bm3dcuda(self) -> _Plugin_bm3dcuda_VideoNode_Bound:
        """
        BM3D algorithm implemented in CUDA
        """
    @property
    def dpid(self) -> _Plugin_dpid_VideoNode_Bound:
        """
        Rapid, Detail-Preserving Image Downscaling
        """
    @property
    def tla(self) -> _Plugin_tla_VideoNode_Bound:
        """
        VapourSynth Temporal Linear Approximation plugin
        """
    @property
    def dpriv(self) -> _Plugin_dpriv_VideoNode_Bound:
        """
        Reconstruction assistance
        """
    @property
    def average(self) -> _Plugin_average_VideoNode_Bound:
        """
        vs-average
        """
    @property
    def fmtc(self) -> _Plugin_fmtc_VideoNode_Bound:
        """
        Format converter, r22
        """
    @property
    def delogohd(self) -> _Plugin_delogohd_VideoNode_Bound:
        """
        VapourSynth DelogoHD Filter r9
        """
    @property
    def neo_f3kdb(self) -> _Plugin_neo_f3kdb_VideoNode_Bound:
        """
        Neo F3KDB Deband Filter r7
        """
    @property
    def neo_fft3d(self) -> _Plugin_neo_fft3d_VideoNode_Bound:
        """
        Neo FFT3D Filter r9
        """
    @property
    def neo_vd(self) -> _Plugin_neo_vd_VideoNode_Bound:
        """
        Neo Vague Denoiser Filter r2
        """
    @property
    def vcmod(self) -> _Plugin_vcmod_VideoNode_Bound:
        """
        VapourSynth Pixel Amplitude modification 
        """
    @property
    def akarin(self) -> _Plugin_akarin_VideoNode_Bound:
        """
        Akarin's Experimental Filters
        """
    @property
    def bilateral(self) -> _Plugin_bilateral_VideoNode_Bound:
        """
        Bilateral filter and Gaussian filter for VapourSynth.
        """
    @property
    def adg(self) -> _Plugin_adg_VideoNode_Bound:
        """
        Adaptive grain
        """
    @property
    def w2xnvk(self) -> _Plugin_w2xnvk_VideoNode_Bound:
        """
        VapourSynth Waifu2x NCNN Vulkan Plugin
        """
    @property
    def f3kdb(self) -> _Plugin_f3kdb_VideoNode_Bound:
        """
        flash3kyuu_deband
        """
    @property
    def fft3dfilter(self) -> _Plugin_fft3dfilter_VideoNode_Bound:
        """
        FFT3DFilter
        """
    @property
    def descale(self) -> _Plugin_descale_VideoNode_Bound:
        """
        Undo linear interpolation
        """
    @property
    def descale_getnative(self) -> _Plugin_descale_getnative_VideoNode_Bound:
        """
        Undo linear interpolation
        """
    @property
    def mx(self) -> _Plugin_mx_VideoNode_Bound:
        """
        Use MXNet to accelerated Image-Processing in VapourSynth
        """
    @property
    def avsw(self) -> _Plugin_avsw_VideoNode_Bound:
        """
        avsproxy
        """
    @property
    def znedi3(self) -> _Plugin_znedi3_VideoNode_Bound:
        """
        Neural network edge directed interpolation (3rd gen.)
        """

    format: typing.Optional[VideoFormat]

    fps: fractions.Fraction
    fps_den: int
    fps_num: int

    height: int
    width: int

    num_frames: int

    # RawNode methods
    def get_frame_async_raw(self, n: int, cb: _Future[VideoFrame], future_wrapper: typing.Optional[typing.Callable[..., None]] = ...) -> _Future[VideoFrame]: ...
    def get_frame_async(self, n: int) -> _Future[VideoFrame]: ...
    def frames(self, prefetch: typing.Optional[int] = ..., backlog: typing.Optional[int] = ...) -> typing.Iterator[VideoFrame]: ...

    def get_frame(self, n: int) -> VideoFrame: ...
    def set_output(self, index: int = 0, alpha: typing.Optional['VideoNode'] = ..., alt_output: int = 0) -> None: ...
    def output(self, fileobj: typing.BinaryIO, y4m: bool = False, progress_update: typing.Optional[typing.Callable[[int, int], None]] = ..., prefetch: int = 0, backlog: int = -1) -> None: ...

    def __add__(self, other: 'VideoNode') -> 'VideoNode': ...
    def __radd__(self, other: 'VideoNode') -> 'VideoNode': ...
    def __mul__(self, other: int) -> 'VideoNode': ...
    def __rmul__(self, other: int) -> 'VideoNode': ...
    def __getitem__(self, other: typing.Union[int, slice]) -> 'VideoNode': ...
    def __len__(self) -> int: ...


class AudioFrame:
    sample_type: SampleType
    bits_per_sample: int
    bytes_per_sample: int
    channel_layout: int
    num_channels: int

    def copy(self) -> 'AudioFrame': ...
    def __getitem__(self, index: int) -> memoryview: ...
    def __len__(self) -> int: ...


class AudioNode:
    @property
    def std(self) -> _Plugin_std_AudioNode_Bound:
        """
        VapourSynth Core Functions
        """

    sample_type: SampleType
    bits_per_sample: int
    bytes_per_sample: int
    channel_layout: int
    num_channels: int
    sample_rate: int
    num_samples: int

    num_frames: int

    # RawNode methods
    def get_frame_async_raw(self, n: int, cb: _Future[AudioFrame], future_wrapper: typing.Optional[typing.Callable[..., None]] = ...) -> _Future[AudioFrame]: ...
    def get_frame_async(self, n: int) -> _Future[AudioFrame]: ...
    def frames(self, prefetch: typing.Optional[int] = ..., backlog: typing.Optional[int] = ...) -> typing.Iterator[AudioFrame]: ...

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
    @property
    def acrop(self) -> _Plugin_acrop_Core_Unbound:
        """
        VapourSynth Auto Crop
        """
    @property
    def ocr(self) -> _Plugin_ocr_Core_Unbound:
        """
        Tesseract OCR Filter
        """
    @property
    def remap(self) -> _Plugin_remap_Core_Unbound:
        """
        Remaps frame indices based on a file/string
        """
    @property
    def comb(self) -> _Plugin_comb_Core_Unbound:
        """
        comb filters v0.0.1
        """
    @property
    def focus2(self) -> _Plugin_focus2_Core_Unbound:
        """
        VapourSynth TemporalSoften Filter v1
        """
    @property
    def knlm(self) -> _Plugin_knlm_Core_Unbound:
        """
        KNLMeansCL for VapourSynth
        """
    @property
    def ftf(self) -> _Plugin_ftf_Core_Unbound:
        """
        Fix Telecined Fades
        """
    @property
    def nnedi3(self) -> _Plugin_nnedi3_Core_Unbound:
        """
        Neural network edge directed interpolation (3rd gen.), v12
        """
    @property
    def libp2p(self) -> _Plugin_libp2p_Core_Unbound:
        """
        libp2p rgb formats packer/unpacker
        """
    @property
    def ccd(self) -> _Plugin_ccd_Core_Unbound:
        """
        chroma denoiser
        """
    @property
    def grain(self) -> _Plugin_grain_Core_Unbound:
        """
        Add some correlated color gaussian noise
        """
    @property
    def cas(self) -> _Plugin_cas_Core_Unbound:
        """
        Contrast Adaptive Sharpening
        """
    @property
    def ctmf(self) -> _Plugin_ctmf_Core_Unbound:
        """
        Constant Time Median Filtering
        """
    @property
    def dctf(self) -> _Plugin_dctf_Core_Unbound:
        """
        DCT/IDCT Frequency Suppressor
        """
    @property
    def deblock(self) -> _Plugin_deblock_Core_Unbound:
        """
        It does a deblocking of the picture, using the deblocking filter of h264
        """
    @property
    def dfttest(self) -> _Plugin_dfttest_Core_Unbound:
        """
        2D/3D frequency domain denoiser
        """
    @property
    def eedi2(self) -> _Plugin_eedi2_Core_Unbound:
        """
        EEDI2
        """
    @property
    def eedi3m(self) -> _Plugin_eedi3m_Core_Unbound:
        """
        Enhanced Edge Directed Interpolation 3
        """
    @property
    def lghost(self) -> _Plugin_lghost_Core_Unbound:
        """
        Ghost Reduction
        """
    @property
    def nnedi3cl(self) -> _Plugin_nnedi3cl_Core_Unbound:
        """
        An intra-field only deinterlacer
        """
    @property
    def mpls(self) -> _Plugin_mpls_Core_Unbound:
        """
        Get m2ts clip id from a playlist and return a dict
        """
    @property
    def tcanny(self) -> _Plugin_tcanny_Core_Unbound:
        """
        Build an edge map using canny edge detection
        """
    @property
    def tdm(self) -> _Plugin_tdm_Core_Unbound:
        """
        A bi-directionally motion adaptive deinterlacer
        """
    @property
    def ttmpsm(self) -> _Plugin_ttmpsm_Core_Unbound:
        """
        A basic, motion adaptive, temporal smoothing filter
        """
    @property
    def vsf(self) -> _Plugin_vsf_Core_Unbound:
        """
        VSFilter
        """
    @property
    def vsfm(self) -> _Plugin_vsfm_Core_Unbound:
        """
        VSFilterMod
        """
    @property
    def w2xc(self) -> _Plugin_w2xc_Core_Unbound:
        """
        Image Super-Resolution using Deep Convolutional Neural Networks
        """
    @property
    def yadifmod(self) -> _Plugin_yadifmod_Core_Unbound:
        """
        Modification of Fizick's yadif avisynth filter
        """
    @property
    def tonemap(self) -> _Plugin_tonemap_Core_Unbound:
        """
        Simple tone mapping for VapourSynth
        """
    @property
    def sangnom(self) -> _Plugin_sangnom_Core_Unbound:
        """
        VapourSynth Single Field Deinterlacer
        """
    @property
    def edgefixer(self) -> _Plugin_edgefixer_Core_Unbound:
        """
        VapourSynth edgefixer port
        """
    @property
    def warp(self) -> _Plugin_warp_Core_Unbound:
        """
        Sharpen images by warping
        """
    @property
    def fb(self) -> _Plugin_fb_Core_Unbound:
        """
        FillBorders plugin for VapourSynth
        """
    @property
    def flux(self) -> _Plugin_flux_Core_Unbound:
        """
        FluxSmooth plugin for VapourSynth
        """
    @property
    def hist(self) -> _Plugin_hist_Core_Unbound:
        """
        VapourSynth Histogram Plugin
        """
    @property
    def median(self) -> _Plugin_median_Core_Unbound:
        """
        Median of clips
        """
    @property
    def msmoosh(self) -> _Plugin_msmoosh_Core_Unbound:
        """
        MSmooth and MSharpen
        """
    @property
    def mvsf(self) -> _Plugin_mvsf_Core_Unbound:
        """
        MVTools Single Precision
        """
    @property
    def mv(self) -> _Plugin_mv_Core_Unbound:
        """
        MVTools v23
        """
    @property
    def scxvid(self) -> _Plugin_scxvid_Core_Unbound:
        """
        VapourSynth Scxvid Plugin
        """
    @property
    def tedgemask(self) -> _Plugin_tedgemask_Core_Unbound:
        """
        Edge detection plugin
        """
    @property
    def tmedian(self) -> _Plugin_tmedian_Core_Unbound:
        """
        Calculates temporal median
        """
    @property
    def tivtc(self) -> _Plugin_tivtc_Core_Unbound:
        """
        Field matching and decimation
        """
    @property
    def wwxd(self) -> _Plugin_wwxd_Core_Unbound:
        """
        Scene change detection approximately like Xvid's
        """
    @property
    def d2v(self) -> _Plugin_d2v_Core_Unbound:
        """
        D2V Source
        """
    @property
    def svp1(self) -> _Plugin_svp1_Core_Unbound:
        """
        SVPFlow1
        """
    @property
    def svp2(self) -> _Plugin_svp2_Core_Unbound:
        """
        SVPFlow2
        """
    @property
    def area(self) -> _Plugin_area_Core_Unbound:
        """
        area average downscaler plugin
        """
    @property
    def avs(self) -> _Plugin_avs_Core_Unbound:
        """
        VapourSynth Avisynth Compatibility
        """
    @property
    def bm3d(self) -> _Plugin_bm3d_Core_Unbound:
        """
        Implementation of BM3D denoising filter for VapourSynth.
        """
    @property
    def dgdecodenv(self) -> _Plugin_dgdecodenv_Core_Unbound:
        """
        DGDecodeNV for VapourSynth
        """
    @property
    def ffms2(self) -> _Plugin_ffms2_Core_Unbound:
        """
        FFmpegSource 2 for VapourSynth
        """
    @property
    def hqdn3d(self) -> _Plugin_hqdn3d_Core_Unbound:
        """
        HQDn3D port as used in avisynth/mplayer
        """
    @property
    def imwri(self) -> _Plugin_imwri_Core_Unbound:
        """
        VapourSynth ImageMagick 7 HDRI Writer/Reader
        """
    @property
    def jinc(self) -> _Plugin_jinc_Core_Unbound:
        """
        VapourSynth EWA resampling
        """
    @property
    def rsnv(self) -> _Plugin_rsnv_Core_Unbound:
        """
        RealSR ncnn Vulkan plugin
        """
    @property
    def rgsf(self) -> _Plugin_rgsf_Core_Unbound:
        """
        RemoveGrain Single Precision
        """
    @property
    def rgvs(self) -> _Plugin_rgvs_Core_Unbound:
        """
        RemoveGrain VapourSynth Port
        """
    @property
    def resize(self) -> _Plugin_resize_Core_Unbound:
        """
        VapourSynth Resize
        """
    @property
    def retinex(self) -> _Plugin_retinex_Core_Unbound:
        """
        Implementation of Retinex algorithm for VapourSynth.
        """
    @property
    def srmdnv(self) -> _Plugin_srmdnv_Core_Unbound:
        """
        SRMD ncnn Vulkan plugin
        """
    @property
    def std(self) -> _Plugin_std_Core_Unbound:
        """
        VapourSynth Core Functions
        """
    @property
    def text(self) -> _Plugin_text_Core_Unbound:
        """
        VapourSynth Text
        """
    @property
    def placebo(self) -> _Plugin_placebo_Core_Unbound:
        """
        libplacebo plugin for VapourSynth
        """
    @property
    def bm3dcuda(self) -> _Plugin_bm3dcuda_Core_Unbound:
        """
        BM3D algorithm implemented in CUDA
        """
    @property
    def dpid(self) -> _Plugin_dpid_Core_Unbound:
        """
        Rapid, Detail-Preserving Image Downscaling
        """
    @property
    def tla(self) -> _Plugin_tla_Core_Unbound:
        """
        VapourSynth Temporal Linear Approximation plugin
        """
    @property
    def dpriv(self) -> _Plugin_dpriv_Core_Unbound:
        """
        Reconstruction assistance
        """
    @property
    def average(self) -> _Plugin_average_Core_Unbound:
        """
        vs-average
        """
    @property
    def fmtc(self) -> _Plugin_fmtc_Core_Unbound:
        """
        Format converter, r22
        """
    @property
    def delogohd(self) -> _Plugin_delogohd_Core_Unbound:
        """
        VapourSynth DelogoHD Filter r9
        """
    @property
    def neo_f3kdb(self) -> _Plugin_neo_f3kdb_Core_Unbound:
        """
        Neo F3KDB Deband Filter r7
        """
    @property
    def neo_fft3d(self) -> _Plugin_neo_fft3d_Core_Unbound:
        """
        Neo FFT3D Filter r9
        """
    @property
    def neo_vd(self) -> _Plugin_neo_vd_Core_Unbound:
        """
        Neo Vague Denoiser Filter r2
        """
    @property
    def vcmod(self) -> _Plugin_vcmod_Core_Unbound:
        """
        VapourSynth Pixel Amplitude modification 
        """
    @property
    def akarin(self) -> _Plugin_akarin_Core_Unbound:
        """
        Akarin's Experimental Filters
        """
    @property
    def bilateral(self) -> _Plugin_bilateral_Core_Unbound:
        """
        Bilateral filter and Gaussian filter for VapourSynth.
        """
    @property
    def adg(self) -> _Plugin_adg_Core_Unbound:
        """
        Adaptive grain
        """
    @property
    def w2xnvk(self) -> _Plugin_w2xnvk_Core_Unbound:
        """
        VapourSynth Waifu2x NCNN Vulkan Plugin
        """
    @property
    def f3kdb(self) -> _Plugin_f3kdb_Core_Unbound:
        """
        flash3kyuu_deband
        """
    @property
    def fft3dfilter(self) -> _Plugin_fft3dfilter_Core_Unbound:
        """
        FFT3DFilter
        """
    @property
    def lsmas(self) -> _Plugin_lsmas_Core_Unbound:
        """
        LSMASHSource for VapourSynth
        """
    @property
    def descale(self) -> _Plugin_descale_Core_Unbound:
        """
        Undo linear interpolation
        """
    @property
    def descale_getnative(self) -> _Plugin_descale_getnative_Core_Unbound:
        """
        Undo linear interpolation
        """
    @property
    def mx(self) -> _Plugin_mx_Core_Unbound:
        """
        Use MXNet to accelerated Image-Processing in VapourSynth
        """
    @property
    def avsw(self) -> _Plugin_avsw_Core_Unbound:
        """
        avsproxy
        """
    @property
    def znedi3(self) -> _Plugin_znedi3_Core_Unbound:
        """
        Neural network edge directed interpolation (3rd gen.)
        """

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
    def add_log_handler(self, handler_func: typing.Optional[typing.Callable[[MessageType, str], None]]) -> None: ...
    def remove_log_handler(self, handle: LogHandle) -> None: ...

    def version(self) -> str: ...
    def version_number(self) -> int: ...


class _CoreProxy(Core):
    @property
    def core(self) -> Core: ...


core: _CoreProxy