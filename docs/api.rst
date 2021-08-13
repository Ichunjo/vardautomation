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
.. autoclass:: vardautomation.tooling.FlacCompressionLevel
   :members:
.. autoclass:: vardautomation.tooling.FlacEncoder
   :members:
   :inherited-members:
   :show-inheritance:

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

Types
======
.. autodata:: vardautomation.types.AnyPath
.. autodata:: vardautomation.types.DuplicateFrame
.. autodata:: vardautomation.types.Trim
.. autodata:: vardautomation.types.UpdateFunc
.. autodata:: vardautomation.types.VPSIdx

Comparison
============
.. autofunction:: vardautomation.comp.make_comps
.. autoclass:: vardautomation.comp.Writer
   :members:
