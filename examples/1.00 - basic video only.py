import vapoursynth as vs
from vsutil import depth

from vardautomation import X265, FileInfo, PresetAAC, PresetBD

core = vs.core

FILE = FileInfo('path/to/your/file.m2ts', (24, -24), preset=[PresetBD, PresetAAC])
clip = depth(FILE.clip_cut, 32)

...
"""Filtering process"""
...

out = depth(clip, 10)


if __name__ == '__main__':
    X265('path/to/your/x265/settings').run_enc(out, FILE)
else:
    out.set_output(0)
