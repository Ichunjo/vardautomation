from typing import List

import vapoursynth as vs
from vardautomation import FileInfo

core = vs.core


FILEINFO_ATTR: List[str] = [
    'path',
    'path_without_ext',
    'work_filename',
    'idx',
    'preset',
    'name',
    'workdir',
    'a_src',
    'a_src_cut',
    'a_enc_cut',
    'chapter',
    'clip',
    '_trims_or_dfs',
    'clip_cut',
    'name_clip_output',
    'name_file_final',
    'name_clip_output_lossless',
    'do_lossless',
    'qpfile',
    'do_qpfile'
]


def test_file_info_attr() -> None:
    file = FileInfo('tests/video_file.mkv', idx=core.lsmas.LWLibavSource)

    assert len(vars(file)) == len(FILEINFO_ATTR)

    for attr in vars(file):
        assert attr in FILEINFO_ATTR

    assert False


# def test_file_info_trims() -> None:
#     file = FileInfo('tests/video_file.mkv', trims_or_dfs=(24, -24))
