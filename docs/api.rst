=============
API Reference
=============

.. automodule:: vardautomation

Get ready
=========

.. autoclass:: vardautomation.config.FileInfo
   :members:

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
.. autoclass:: vardautomation.tooling.Tool
   :members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.BasicTool
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.Qpfile
   :members:
.. autofunction:: vardautomation.tooling.make_qpfile

Video encoders
----------------
.. autoclass:: vardautomation.tooling.VideoEncoder
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.LosslessEncoder
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.NvenccEncoder
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.FFV1Encoder
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.VideoLanEncoder
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.X265Encoder
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.X264Encoder
   :members:
   :inherited-members:
   :show-inheritance:

Audio extracters
----------------
.. autoclass:: vardautomation.tooling.AudioExtracter
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.MKVAudioExtracter
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.Eac3toAudioExtracter
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.FfmpegAudioExtracter
   :members:
   :inherited-members:
   :show-inheritance:

Audio cutters
----------------
.. autoclass:: vardautomation.tooling.AudioCutter
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.ScipyCutter
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.EztrimCutter
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.SoxCutter
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.PassthroughCutter
   :members:
   :inherited-members:
   :show-inheritance:

Audio encoders
----------------
.. autoclass:: vardautomation.tooling.AudioEncoder
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.PassthroughAudioEncoder
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.QAACEncoder
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.OpusEncoder
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.FDKAACEncoder
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.FlacEncoder
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.BitrateMode
   :members:
.. autoclass:: vardautomation.tooling.FlacCompressionLevel
   :members:

Muxing
-------
.. autoclass:: vardautomation.tooling.Mux
   :members:
.. autoclass:: vardautomation.tooling.Stream
   :members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.MediaStream
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.VideoStream
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.AudioStream
   :members:
   :inherited-members:
   :show-inheritance:
.. autoclass:: vardautomation.tooling.ChapterStream
   :members:
   :inherited-members:
   :show-inheritance:

Automation
============
.. autoclass:: vardautomation.automation.SelfRunner
   :members:
.. autoclass:: vardautomation.automation.RunnerConfig
   :members:

Patch
============
.. autoclass:: vardautomation.patch.Patch
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

Time conversion
===============
.. autoclass:: vardautomation.timeconv.Convert
   :members:

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
