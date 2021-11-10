import vapoursynth as vs
from vardautomation import (EztrimCutter, FileInfo, Mux, PresetAAC, PresetBD,
                            QAACEncoder, X265Encoder, FFmpegAudioExtracter, RunnerConfig, SelfRunner)
from vsutil import depth

core = vs.core

FILE = FileInfo('path/to/your/file.m2ts', (24, -24), preset=[PresetBD, PresetAAC])
clip = depth(FILE.clip_cut, 32)

...
"""Filtering process"""
...

out = depth(clip, 10)


if __name__ == '__main__':
    config = RunnerConfig(
        X265Encoder('path/to/your/x265/settings'),
        a_extracters=FFmpegAudioExtracter(FILE, track_in=1, track_out=1),
        a_cutters=EztrimCutter(FILE, track=1),
        a_encoders=QAACEncoder(FILE, track=1),
        muxer=Mux(FILE)
    )

    SelfRunner(out, FILE, config).run()
else:
    out.set_output(0)
