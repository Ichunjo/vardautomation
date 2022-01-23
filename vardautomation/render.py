"""Node rendering helpers"""

__all__ = [
    'clip_async_render',
    'WaveHeader', 'audio_async_render'
]

# pylint: disable=no-member

import struct
from enum import IntEnum
from typing import BinaryIO, Callable, Dict, List, Optional, TextIO, Tuple, Union, overload

import numpy as np
import vapoursynth as vs
from rich.progress import BarColumn, Progress, ProgressColumn, Task, TextColumn, TimeRemainingColumn
from rich.text import Text

from ._logging import logger
from .utils import Properties


class FPSColumn(ProgressColumn):
    def render(self, task: Task) -> Text:
        return Text(f"{task.speed or 0:.02f} fps")


def get_render_progress() -> Progress:
    return Progress(
        TextColumn("{task.description}"),
        BarColumn(),
        TextColumn("{task.completed}/{task.total}"),
        TextColumn("{task.percentage:>3.02f}%"),
        FPSColumn(),
        TimeRemainingColumn(),
    )


RenderCallback = Callable[[int, vs.VideoFrame], None]


@overload
def clip_async_render(clip: vs.VideoNode,  # type: ignore [misc]
                      outfile: Optional[BinaryIO] = None,
                      timecodes: None = ...,
                      progress: Optional[str] = "Rendering clip...",
                      callback: Union[RenderCallback, List[RenderCallback], None] = None) -> None:
    ...


@overload
def clip_async_render(clip: vs.VideoNode,
                      outfile: Optional[BinaryIO] = None,
                      timecodes: TextIO = ...,
                      progress: Optional[str] = "Rendering clip...",
                      callback: Union[RenderCallback, List[RenderCallback], None] = None) -> List[float]:
    ...


@logger.catch
def clip_async_render(clip: vs.VideoNode,  # noqa: C901
                      outfile: Optional[BinaryIO] = None,
                      timecodes: Optional[TextIO] = None,
                      progress: Optional[str] = "Rendering clip...",
                      callback: Union[RenderCallback, List[RenderCallback], None] = None) -> Union[None, List[float]]:
    """
    Render a clip by requesting frames asynchronously using clip.frames,
    providing for callback with frame number and frame object.

    This is mostly a re-implementation of VideoNode.output, but a little bit slower since it's pure python.
    You only really need this when you want to render a clip while operating on each frame in order
    or you want timecodes without using vspipe.

    Original function borrowed from lvsfunc.render.clip_async_render.

    :param clip:      Clip to render.
    :param outfile:   Y4MPEG render output BinaryIO handle. If None, no Y4M output is performed.
                      Use ``sys.stdout.buffer`` for stdout. (Default: None)
    :param timecodes: Timecode v2 file TextIO handle. If None, timecodes will not be written.
    :param progress:  String to use for render progress display.
                      If empty or ``None``, no progress display.
    :param callback:  Single or list of callbacks to be preformed. The callbacks are called
                      when each sequential frame is output, not when each frame is done.

    :return:          List of timecodes from rendered clip.
    """
    cbl = [] if callback is None else callback if isinstance(callback, list) else [callback]

    if progress:
        p = get_render_progress()
        task = p.add_task(progress, total=clip.num_frames)
        p.start()

        def _progress_cb(n: int, f: vs.VideoFrame) -> None:
            p.update(task, advance=1)

        cbl.append(_progress_cb)

    if outfile:
        if clip.format is None:
            raise ValueError("clip_async_render: 'Cannot render a variable format clip to y4m!'")
        if clip.format.color_family not in (vs.YUV, vs.GRAY):
            raise ValueError("clip_async_render: 'Can only render YUV and GRAY clips to y4m!'")
        if clip.format.color_family == vs.GRAY:
            y4mformat = "mono"
        else:
            try:
                formats: Dict[Tuple[int, int], str] = {
                    (1, 1): "420",
                    (1, 0): "422",
                    (0, 0): "444",
                    (2, 2): "410",
                    (2, 0): "411",
                    (0, 1): "440",
                }
                y4mformat = formats[(clip.format.subsampling_w, clip.format.subsampling_h)]
            except KeyError as key_err:
                raise ValueError("clip_async_render: 'What have you done'") from key_err

        y4mformat = f"{y4mformat}p{clip.format.bits_per_sample}" if clip.format.bits_per_sample > 8 else y4mformat
        header = f"YUV4MPEG2 C{y4mformat} W{clip.width} H{clip.height} F{clip.fps.numerator}:{clip.fps.denominator} Ip A0:0\n"
        outfile.write(header.encode("utf-8"))

    if timecodes:
        timecodes.write("# timestamp format v2\n")

    tc_list = [0.0]

    for n, f in enumerate(clip.frames(close=True)):
        for cb in cbl:
            cb(n, f)
        if timecodes:
            _write_timecodes(f, timecodes, tc_list)
        if outfile:
            _finish_frame_video(f, outfile)
    if progress:
        p.stop()  # type: ignore

    return tc_list if timecodes else None


def _finish_frame_video(frame: vs.VideoFrame, outfile: BinaryIO) -> None:
    outfile.write("FRAME\n".encode("utf-8"))
    for plane in frame:  # type: ignore [attr-defined]
        outfile.write(plane)


def _write_timecodes(frame: vs.VideoFrame, timecodes: TextIO, tc_list: List[float]) -> None:
    tc = tc_list[-1] + Properties.get_prop(frame, '_DurationNum', int) / Properties.get_prop(frame, '_DurationDen', int)
    tc_list.append(tc)
    timecodes.write(f"{round(tc * 1000):d}\n")


class WaveFormat(IntEnum):
    """
    WAVE form wFormatTag IDs
    Complete list is in mmreg.h in Windows 10 SDK.
    """
    PCM = 0x0001
    IEEE_FLOAT = 0x0003
    EXTENSIBLE = 0xFFFE


class WaveHeader(IntEnum):
    """
    Wave headers
    """
    WAVE = 0
    WAVE64 = 1
    AUTO = 2


WAVE_RIFF_TAG = b'RIFF'
WAVE_WAVE_TAG = b'WAVE'
WAVE_FMT_TAG = b'fmt '
WAVE_DATA_TAG = b'data'

WAVE64_RIFF_UUID = (0x72, 0x69, 0x66, 0x66, 0x2E, 0x91, 0xCF, 0x11, 0xA5, 0xD6, 0x28, 0xDB, 0x04, 0xC1, 0x00, 0x00)
WAVE64_WAVE_UUID = (0x77, 0x61, 0x76, 0x65, 0xF3, 0xAC, 0xD3, 0x11, 0x8C, 0xD1, 0x00, 0xC0, 0x4F, 0x8E, 0xDB, 0x8A)
WAVE64_FMT_UUID = (0x66, 0x6D, 0x74, 0x20, 0xF3, 0xAC, 0xD3, 0x11, 0x8C, 0xD1, 0x00, 0xC0, 0x4F, 0x8E, 0xDB, 0x8A)
WAVE64_DATA_UUID = (0x64, 0x61, 0x74, 0x61, 0xF3, 0xAC, 0xD3, 0x11, 0x8C, 0xD1, 0x00, 0xC0, 0x4F, 0x8E, 0xDB, 0x8A)
WAVE_FMT_EXTENSIBLE_SUBFORMAT = (
    (WaveFormat.PCM, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x80, 0x00, 0x00, 0xAA, 0x00, 0x38, 0x9B, 0x71),
    (WaveFormat.IEEE_FLOAT, 0x00, 0x00, 0x00, 0x00, 0x00, 0x10, 0x00, 0x80, 0x00, 0x00, 0xAA, 0x00, 0x38, 0x9B, 0x71)
)


@logger.catch
def audio_async_render(audio: vs.AudioNode,
                       outfile: BinaryIO,
                       header: WaveHeader = WaveHeader.AUTO,
                       progress: Optional[str] = "Rendering audio...") -> None:
    """
    Render an audio by requesting frames asynchronously using audio.frames.

    Implementation-like of VideoNode.output for an AudioNode that isn't in the Cython side yet.

    :param audio:       Audio to render.
    :param outfile:     Render output BinaryIO handle.
    :param header:      Kind of Wave header.
                        WaveHeader.AUTO adds a Wave64 header if the audio

                        * Has more than 2 channels
                        * Has a bitdepth > 16
                        * Has more than 44100 samples

    :param progress:    String to use for render progress display.
                        If empty or ``None``, no progress display.
    """
    if progress:
        p = get_render_progress()
        task = p.add_task(progress, total=audio.num_frames)
        p.start()

    bytes_per_output_sample = (audio.bits_per_sample + 7) // 8
    block_align = audio.num_channels * bytes_per_output_sample
    bytes_per_second = audio.sample_rate * block_align
    data_size = audio.num_samples * block_align

    if header == WaveHeader.AUTO:
        conditions = (audio.num_channels > 2, audio.bits_per_sample > 16, audio.num_samples > 44100)
        header_func, use_w64 = (_w64_header, WaveHeader.WAVE64) if any(conditions) else (_wav_header, WaveHeader.WAVE)
    else:
        use_w64 = header
        header_func = (_wav_header, _w64_header)[header]

    outfile.write(header_func(audio, bytes_per_second, block_align, data_size))

    for f in audio.frames(close=True):
        if progress:
            p.update(task, advance=1)  # type: ignore
        _finish_frame_audio(f, outfile, audio.bits_per_sample == 24)
    # Determine file size and place the value at the correct position
    # at the beginning of the file
    size = outfile.tell()
    if use_w64:
        outfile.seek(16)
        outfile.write(struct.pack('<Q', size))
    else:
        outfile.seek(4)
        outfile.write(struct.pack('<I', size - 8))
    if progress:
        p.stop()  # type: ignore


@logger.catch
def _wav_header(audio: vs.AudioNode, bps: int, block_align: int, data_size: int) -> bytes:
    header = WAVE_RIFF_TAG
    # Add 4 bytes for the length later
    header += b'\x00\x00\x00\x00'
    header += WAVE_WAVE_TAG

    header += WAVE_FMT_TAG
    format_tag = WaveFormat.IEEE_FLOAT if audio.sample_type == vs.FLOAT else WaveFormat.PCM

    fmt_chunk_data = struct.pack(
        '<HHIIHH', format_tag, audio.num_channels, audio.sample_rate,
        bps, block_align, audio.bits_per_sample
    )
    header += struct.pack('<I', len(fmt_chunk_data))
    header += fmt_chunk_data

    if len(header) + data_size > 0xFFFFFFFE:
        raise ValueError('Data exceeds wave file size limit')

    header += WAVE_DATA_TAG
    header += struct.pack('<I', data_size)
    return header


def _w64_header(audio: vs.AudioNode, bps: int, block_align: int, data_size: int) -> bytes:
    # RIFF-GUID
    header = bytes(WAVE64_RIFF_UUID)
    # Add 8 bytes for the length later
    header += b'\x00\x00\x00\x00\x00\x00\x00\x00'
    # WAVE-GUID
    header += bytes(WAVE64_WAVE_UUID)
    # FMT-GUID
    fmt_guid = bytes(WAVE64_FMT_UUID)
    header += fmt_guid

    # We only support WAVEFORMATEXTENSIBLE for WAVE64 header
    format_tag = WaveFormat.EXTENSIBLE

    # cb_size should be 22 for WAVEFORMATEXTENSIBLE with PCM
    cb_size = 22
    fmt_chunk_data = struct.pack(
        '<HHIIHHHHI', format_tag, audio.num_channels, audio.sample_rate,
        bps, block_align, audio.bits_per_sample, cb_size,
        audio.bits_per_sample,  # valid bit per sample
        audio.channel_layout
    )
    # Add the subformat GUID, first 2 bytes have format type, 1 being PCM
    fmt_chunk_data += bytes(WAVE_FMT_EXTENSIBLE_SUBFORMAT[audio.sample_type])

    # Add the FMT size
    # Length of the FMT-GUID + length of FMT data and 8 for the bytes themself
    header += struct.pack('<Q', len(fmt_guid) + 8 + len(fmt_chunk_data))
    header += fmt_chunk_data

    # DATA-GUID
    data_uuid = bytes(WAVE64_DATA_UUID)
    header += data_uuid
    header += struct.pack('<Q', data_size + len(data_uuid) + 8)
    return header


def _finish_frame_audio(frame: vs.AudioFrame, outfile: BinaryIO, _24bit: bool) -> None:
    # For some reason f[i] is faster than list(f) or just passing f to stack
    data = np.stack([frame[i] for i in range(frame.num_channels)], axis=1)  # type: ignore

    if _24bit:
        if data.ndim == 1:
            # Convert to a 2D array with a single column
            data.shape += (1, )
        # Data values are stored in 32 bits so we must convert them to 24 bits
        # Then by shifting first 0 bits, then 8, then 16, the resulting output is 24 bit little-endian.
        data = ((data // 2 ** 8).reshape(data.shape + (1, )) >> np.array([0, 8, 16]))  # type: ignore [attr-defined]
        outfile.write(data.ravel().astype(np.uint8).tobytes())  # type: ignore
    else:
        outfile.write(data.ravel().view(np.int8).tobytes())  # type: ignore


class SceneChangeMode(IntEnum):
    WWXD = 11
    SCXVID = 22
    MV = 44


def find_scene_changes(  # noqa: C901
    clip: vs.VideoNode, mode: Union[int, SceneChangeMode] = SceneChangeMode.WWXD, *,
    scxvid_use_slices: bool = False,
    mv_vectors: Optional[vs.VideoNode] = None,
    mv_thscd1: Optional[int] = None, mv_thscd2: Optional[int] = None,
) -> List[int]:
    """
    Generate a list of scene changes (keyframes).

    Dependencies:

    * vapoursynth-wwxd
    * vapoursynth-scxvid (Optional: scxvid mode)

    :param clip:   Clip to search for scene changes. Will be rendered in its entirety.
    :param mode:   Scene change detection mode:

                   * WWXD: Use wwxd
                   * SCXVID: Use scxvid
                   * WWXD_SCXVID_UNION: Union of wwxd and sxcvid (must be detected by at least one)
                   * WWXD_SCXVID_INTERSECTION: Intersection of wwxd and scxvid (must be detected by both)

    :return:       List of scene changes.
    """
    frames: List[int] = []
    props: List[str] = []
    clip = clip.resize.Bilinear(640, 360, format=vs.YUV420P8)
    SCM = SceneChangeMode
    wwxd_unions = {SCM.WWXD | SCM.SCXVID, SCM.WWXD | SCM.MV, SCM.WWXD | SCM.SCXVID | SCM.MV}
    wwxd_inters = {SCM.WWXD & SCM.SCXVID, SCM.WWXD & SCM.MV, SCM.WWXD & SCM.SCXVID & SCM.MV}
    scxvid_unions = {SCM.SCXVID | SCM.WWXD, SCM.SCXVID | SCM.MV, SCM.SCXVID | SCM.WWXD | SCM.MV}
    scxvid_inters = {SCM.SCXVID & SCM.WWXD, SCM.SCXVID & SCM.MV, SCM.SCXVID & SCM.WWXD & SCM.MV}
    mv_unions = {SCM.MV | SCM.WWXD, SCM.MV | SCM.SCXVID, SCM.MV | SCM.WWXD | SCM.SCXVID}
    mv_inters = {SCM.MV & SCM.WWXD, SCM.MV & SCM.SCXVID, SCM.MV & SCM.WWXD & SCM.SCXVID}

    # SCXVID and mv share the same prop
    # https://github.com/dubhater/vapoursynth-scxvid/issues/3
    if mode in {SCM.WWXD} | wwxd_unions | wwxd_inters:
        clip = clip.wwxd.WWXD()
        props.append('Scenechange')
    if mode in {SCM.SCXVID} | scxvid_unions | scxvid_inters:
        clip = clip.scxvid.Scxvid(use_slices=scxvid_use_slices)
        props.append('_SceneChangePrev')
    if mode in {SCM.MV} | mv_unions | mv_inters:
        if not mv_vectors:
            mv_vectors = clip.mv.Super().mv.Analyse()
        clip = clip.mv.SCDetection(mv_vectors, mv_thscd1, mv_thscd2)
        props.append('_SceneChangePrev')

    def _cb(n: int, f: vs.VideoFrame) -> None:
        if mode in {SCM.WWXD, SCM.SCXVID, SCM.MV}:
            if Properties.get_prop(f, props[0], int) == 1:
                frames.append(n)
        elif mode in wwxd_unions | scxvid_unions | mv_unions:
            if any(Properties.get_prop(f, p, int) == 1 for p in props):
                frames.append(n)
        elif mode in wwxd_inters | scxvid_inters | mv_inters:
            if all(Properties.get_prop(f, p, int) == 1 for p in props):
                frames.append(n)

    clip_async_render(clip, progress="Detecting scene changes...", callback=_cb)

    return sorted(frames)
