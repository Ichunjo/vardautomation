import vapoursynth as vs
from vardautomation import FileInfo, PresetAAC, PresetBD, X265Encoder
from vsutil import depth

core = vs.core

FILE = FileInfo('path/to/your/file.m2ts', (24, -24), preset=[PresetBD, PresetAAC])
clip = depth(FILE.clip_cut, 32)

...
"""Filtering process"""
...

out = depth(clip, 10)


if __name__ == '__main__':
    X265Encoder('path/to/your/x265/settings').run_enc(out, FILE)
else:
    out.set_output(0)
