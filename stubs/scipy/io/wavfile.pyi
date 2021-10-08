from io import BufferedReader, BufferedWriter
from os import PathLike
from typing import Tuple

from numpy import float32, int16, int32, uint8
from numpy.typing import NDArray


class WavFileWarning(UserWarning): ...


def read(filename: str | PathLike[str] | BufferedReader, mmap: bool = ...) -> Tuple[int, NDArray[uint8 | int16 | int32 | float32]]: ...

def write(filename: str | PathLike[str] | BufferedWriter, rate: int, data: NDArray[uint8 | int16 | int32 | float32]) -> None: ...
