from vardautomation import FileInfo

FILEINFO_ATTR: list[str] = [
    "workdir",
    "path",
    "path_without_ext",
    "work_filename",
    "idx",
    "name",
    "a_src",
    "a_src_cut",
    "a_enc_cut",
    "_chapter",
    "preset",
    "clip",
    "_trims_or_dfs",
    "clip_cut",
    "name_clip_output",
    "name_file_final",
]


def test_file_info_attr() -> None:
    file = FileInfo("tests/video_file.mkv")

    assert len(vars(file)) == len(FILEINFO_ATTR)

    for attr in vars(file):
        assert attr in FILEINFO_ATTR


# def test_file_info_trims() -> None:
#     file = FileInfo('tests/video_file.mkv', trims_or_dfs=(24, -24))
