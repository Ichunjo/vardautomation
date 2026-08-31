"""Shader file paths for vs.placebo module"""

__all__ = ["Shader"]

from enum import Enum


class Shader(str, Enum):
    FSRCNNX_56_16_4_1 = r"C:\Users\Varde\mpv\Shaders\FSRCNNX_x2_56-16-4-1.glsl"
    FSRCNNX_16_0_4_1 = r"C:\Users\Varde\mpv\Shaders\FSRCNNX_x2_16-0-4-1-edit.glsl"
    KRIGBILATERAL = r"C:\Users\Varde\mpv\Shaders\KrigBilateral.glsl"
    SSIMDOWNSCALER = r"C:\Users\Varde\mpv\Shaders\SSimDownscaler.glsl"
