"""Constants module"""
from __future__ import annotations

__all__ = ['BinaryPath']

from .vpathlib import VPath


class BinaryPath:
    """Class storing the path of the variable binaries used in vardautomation"""
    eac3to: VPath = VPath('eac3to')
    fdkaac: VPath = VPath('fdkaac')
    ffmpeg: VPath = VPath('ffmpeg')
    ffmsindex: VPath = VPath('ffmsindex')
    flac: VPath = VPath('flac')
    mkvextract: VPath = VPath('mkvextract')
    mkvmerge: VPath = VPath('mkvmerge')
    nvencc: VPath = VPath('nvencc')
    opusenc: VPath = VPath('opusenc')
    qaac: VPath = VPath('qaac')
    sox: VPath = VPath('sox')
    x264: VPath = VPath('x264')
    x265: VPath = VPath('x265')
