# 0.4.0
- Add AudioExtracter support
  Old scripts can just replace BasicTool by AudioExtracter
- Add binary_path module
- Remove xml_file in PassthroughAudioEncoder
- QAACEncoder handles all modes
- OpusEncoder handles all modes for both ffmpeg and opusenc implementation
- Add FDKAACEncoder for both ffmpeg and fdkaac implementation
- Improve errors printing
- Use workdir attribute where it should be used in FileInfo
- Fix incorrect xml tag file path in AudioEncoder objects
- Add an optional uploading method in SelfRunner
- Add an optional renaming method in SelfRunner