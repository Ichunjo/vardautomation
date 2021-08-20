from typing import Any, Optional, Sequence

import numpy as np
from numpy.typing import NDArray

IMWRITE_PNG_COMPRESSION: int


def imwrite(filename: str, img: NDArray[Any], params: Optional[Sequence[Any]] = ...) -> None:
    "imwrite(filename, img[, params]) -> retval\n.   @brief Saves an image to a specified file.\n.   \n.   The function imwrite saves the image to the specified file. The image format is chosen based on the\n.   filename extension (see cv::imread for the list of extensions). In general, only 8-bit\n.   single-channel or 3-channel (with 'BGR' channel order) images\n.   can be saved using this function, with these exceptions:\n.   \n.   - 16-bit unsigned (CV_16U) images can be saved in the case of PNG, JPEG 2000, and TIFF formats\n.   - 32-bit float (CV_32F) images can be saved in PFM, TIFF, OpenEXR, and Radiance HDR formats;\n.     3-channel (CV_32FC3) TIFF images will be saved using the LogLuv high dynamic range encoding\n.     (4 bytes per pixel)\n.   - PNG images with an alpha channel can be saved using this function. To do this, create\n.   8-bit (or 16-bit) 4-channel image BGRA, where the alpha channel goes last. Fully transparent pixels\n.   should have alpha set to 0, fully opaque pixels should have alpha set to 255/65535 (see the code sample below).\n.   - Multiple images (vector of Mat) can be saved in TIFF format (see the code sample below).\n.   \n.   If the format, depth or channel order is different, use\n.   Mat::convertTo and cv::cvtColor to convert it before saving. Or, use the universal FileStorage I/O\n.   functions to save the image to XML or YAML format.\n.   \n.   The sample below shows how to create a BGRA image, how to set custom compression parameters and save it to a PNG file.\n.   It also demonstrates how to save multiple images in a TIFF file:\n.   @include snippets/imgcodecs_imwrite.cpp\n.   @param filename Name of the file.\n.   @param img (Mat or vector of Mat) Image or Images to be saved.\n.   @param params Format-specific parameters encoded as pairs (paramId_1, paramValue_1, paramId_2, paramValue_2, ... .) see cv::ImwriteFlags"
    ...

def merge(mv: Sequence[NDArray[Any]], dst: Optional[NDArray[Any]] = ...) -> NDArray[Any]:
    'merge(mv[, dst]) -> dst\n.   @overload\n.   @param mv input vector of matrices to be merged; all the matrices in mv must have the same\n.   size and the same depth.\n.   @param dst output array of the same size and the same depth as mv[0]; The number of channels will\n.   be the total number of channels in the matrix array.'
    ...
