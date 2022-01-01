"""
This module implements just one class that stores the path of the binaries used in vardautomation.\n
Just edit one of these attributes if the binary is not in your environment path like this::

    from vardautomation import BinaryPath, VPath

    BinaryPath.mkvmerge = VPath('path/to/your/mkvmerge')

"""

__all__ = ['BinaryPath']

from typing import NoReturn

from .vpathlib import VPath


class BinaryPath:
    """
    Class storing the path of the variable binaries used in vardautomation.\n
    Just edit one of these attributes if the binary is not in your environment path
    """

    def __init__(self) -> NoReturn:  # type: ignore[misc]
        raise RuntimeError('Cannot directly instantiate this class.')

    eac3to: VPath = VPath('eac3to')
    """
    https://www.videohelp.com/software/eac3to\n
    https://en.wikibooks.org/wiki/Eac3to/How_to_Use
    """

    fdkaac: VPath = VPath('fdkaac')
    """
    https://github.com/nu774/fdkaac\n
    https://en.wikipedia.org/wiki/Fraunhofer_FDK_AAC\n
    Also available in ffmpeg with ``--enable-libfdk-aac``
    """

    ffmpeg: VPath = VPath('ffmpeg')
    """
    https://www.ffmpeg.org/
    """

    ffmsindex: VPath = VPath('ffmsindex')
    """
    https://github.com/FFMS/ffms2
    """

    flac: VPath = VPath('flac')
    """
    https://xiph.org/flac/index.html
    """

    mkvextract: VPath = VPath('mkvextract')
    """
    https://mkvtoolnix.download/\n
    https://mkvtoolnix.download/doc/mkvextract.html
    """

    mkvmerge: VPath = VPath('mkvmerge')
    """
    https://mkvtoolnix.download/\n
    https://mkvtoolnix.download/doc/mkvextract.html
    """

    nvencc: VPath = VPath('nvencc')
    """
    https://github.com/rigaya/NVEnc
    """

    opusenc: VPath = VPath('opusenc')
    """
    https://github.com/xiph/opus-tools\n
    Also available in ffmpeg
    """

    qaac: VPath = VPath('qaac')
    """
    https://sites.google.com/site/qaacpage/
    """

    rclone: VPath = VPath('rclone')
    """
    https://rclone.org/
    """

    sox: VPath = VPath('sox')
    """
    http://sox.sourceforge.net/
    """

    x264: VPath = VPath('x264')
    """
    https://www.videolan.org/developers/x264.html
    """

    x265: VPath = VPath('x265')
    """
    http://msystem.waw.pl/x265/\n
    https://bitbucket.org/multicoreware/x265_git/wiki/Home
    """
