"""Deprecated things module"""

__all__ = ['NvenccEncoder', 'FFV1Encoder', 'X264Encoder', 'X265Encoder']

from typing import Any

from .tooling import FFV1, X264, X265, NVEncCLossless
from .status import Status


class NvenccEncoder(NVEncCLossless):
    def __init__(self) -> None:
        Status.warn('"NvenccEncoder" is deprecated; use "NVEncCLossless" instead')
        super().__init__()


class FFV1Encoder(FFV1):
    def __init__(self, *, threads: int = 0) -> None:
        Status.warn('"FFV1Encoder" is deprecated; use "FFV1" instead')
        super().__init__(threads=threads)


class X264Encoder(X264):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        Status.warn('"X264Encoder" is deprecated; use "X264" instead')
        super().__init__(*args, **kwargs)


class X265Encoder(X265):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        Status.warn('"X265Encoder" is deprecated; use "X265" instead')
        super().__init__(*args, **kwargs)
