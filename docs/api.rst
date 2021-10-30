=============
API Reference
=============

.. automodule:: vardautomation

Configuration
==============
.. autoclass:: vardautomation.config.FileInfo
   :members:
.. autoclass:: vardautomation.config.BlurayShow
   :members:

Presets
----------------
.. autodata:: vardautomation.config.PresetGeneric
.. autodata:: vardautomation.config.PresetBD
.. autodata:: vardautomation.config.PresetWEB
.. autodata:: vardautomation.config.PresetAAC
.. autodata:: vardautomation.config.PresetOpus
.. autodata:: vardautomation.config.PresetEAC3
.. autodata:: vardautomation.config.PresetFLAC
.. autodata:: vardautomation.config.PresetChapOGM
.. autodata:: vardautomation.config.PresetChapXML

Tools
======
.. autoclass:: vardautomation.tooling.abstract.Tool
   :members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.base.BasicTool
   :members:
   :inherited-members:
   :show-inheritance:

Video encoders
----------------
.. autoclass:: vardautomation.tooling.video.VideoEncoder
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.video.VideoLanEncoder
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.video.X265Encoder
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.video.X264Encoder
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.video.LosslessEncoder
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.video.NvenccEncoder
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.video.FFV1Encoder
   :members:
   :inherited-members:
   :show-inheritance:

Audio extracters
----------------
.. autoclass:: vardautomation.tooling.audio.AudioExtracter
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.audio.MKVAudioExtracter
   :members:
   :inherited-members:
.. autoclass:: vardautomation.tooling.audio.Eac3toAudioExtracter
   :members:
   :inherited-members:
.. autoclass:: vardautomation.tooling.audio.FFmpegAudioExtracter
   :members:
   :inherited-members:

Audio cutters
----------------
.. autoclass:: vardautomation.tooling.audio.AudioCutter
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.audio.ScipyCutter
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.audio.EztrimCutter
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.audio.SoxCutter
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.audio.PassthroughCutter
   :members:
   :inherited-members:
   :show-inheritance:

Audio encoders
----------------
.. autoclass:: vardautomation.tooling.audio.AudioEncoder
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.audio.PassthroughAudioEncoder
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.audio.QAACEncoder
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.audio.OpusEncoder
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.audio.FDKAACEncoder
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.audio.FlacEncoder
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.audio.BitrateMode
   :members:
.. autoclass:: vardautomation.tooling.audio.FlacCompressionLevel
   :members:

Muxing
-------
.. autoclass:: vardautomation.tooling.mux.Mux
   :members:
.. autoclass:: vardautomation.tooling.mux.Stream
   :members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.mux.MediaStream
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.mux.VideoStream
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.mux.AudioStream
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.mux.ChapterStream
   :members:
   :inherited-members:
   :show-inheritance:

Utility
-------
.. autoclass:: vardautomation.tooling.misc.Qpfile
   :members:
.. autofunction:: vardautomation.tooling.misc.make_qpfile
.. autofunction:: vardautomation.tooling.misc.get_vs_core

Automation
============
.. autoclass:: vardautomation.automation.SelfRunner
   :members:
.. autoclass:: vardautomation.automation.RunnerConfig
   :members:
.. autoclass:: vardautomation.automation.Patch
   :members:

Chapters stuff
===============
.. autoclass:: vardautomation.chapterisation.Chapter
   :members:
.. autoclass:: vardautomation.chapterisation.Chapters
   :members:
   :show-inheritance:
.. autoclass:: vardautomation.chapterisation.OGMChapters
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.chapterisation.MatroskaXMLChapters
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.chapterisation.MplsChapters
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.chapterisation.IfoChapters
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.chapterisation.MplsReader
   :members:
.. autoclass:: vardautomation.chapterisation.IfoReader
   :members:

Comparison
============
.. autoclass:: vardautomation.comp.Writer
   :members:
.. autoclass:: vardautomation.comp.PictureType
   :members:
.. autoclass:: vardautomation.comp.SlowPicsConf
   :members:
.. autodata:: vardautomation.comp.default_conf
.. autoclass:: vardautomation.comp.Comparison
   :members:
.. autofunction:: vardautomation.comp.make_comps

Binary Path
============
.. autoclass:: vardautomation.binary_path.BinaryPath
   :members:

Language
============
.. autoclass:: vardautomation.language.Lang
   :members:
.. autodata:: vardautomation.language.FRENCH
.. autodata:: vardautomation.language.ENGLISH
.. autodata:: vardautomation.language.JAPANESE
.. autodata:: vardautomation.language.UNDEFINED

VPath
============
.. autoclass:: vardautomation.vpathlib.VPath
   :members:

Types
======
.. autodata:: vardautomation.types.AnyPath
.. autodata:: vardautomation.types.UpdateFunc
.. autodata:: vardautomation.types.VPSIdx

Internal functions
==================
.. autoclass:: vardautomation.utils.Properties
   :members:
