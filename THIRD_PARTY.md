# Third-Party Software

R800ZZ RVM Tools uses or works with the following third-party software.

The third-party projects listed below are developed and distributed independently from R800ZZ RVM Tools.  
Their respective licenses and terms apply to those projects.

## Robust Video Matting (RVM)

**Project:** Robust Video Matting  
**Repository:** https://github.com/PeterL1n/RobustVideoMatting  
**License:** GNU General Public License v3.0 (GPL-3.0)

R800ZZ RVM Tools uses Robust Video Matting for human foreground extraction.

The RVM source code and pretrained model files are **not included in this repository**.  
They are obtained from the upstream project when required.

For the exact license terms applying to RVM and its distributed files, please refer to the upstream repository.

## PyTorch

**Project:** PyTorch  
**Website:** https://pytorch.org/  
**Repository:** https://github.com/pytorch/pytorch  
**Main project license:** BSD 3-Clause License

PyTorch is used to run the RVM neural network.

PyTorch may include or depend on additional third-party components distributed under their own licenses.  
For the complete license information, please refer to the PyTorch repository and the license notices included with the installed package.

## DirectML / Torch-DirectML

**Project:** Microsoft DirectML  
**Repository:** https://github.com/microsoft/DirectML  
**License:** MIT License

DirectML is used by the AMD and Intel GPU configurations.

The `torch-directml` Python package provides the PyTorch DirectML backend used by R800ZZ RVM Tools.

Please refer to Microsoft's DirectML distribution and documentation for the applicable license and third-party notices.

## FFmpeg

**Project:** FFmpeg  
**Website:** https://ffmpeg.org/  
**License information:** https://ffmpeg.org/legal.html

FFmpeg is used for video decoding, audio handling, and video encoding.

FFmpeg is **not included in this repository**. Users install or provide their own FFmpeg build.

FFmpeg licensing depends on how a particular FFmpeg binary was built.  
FFmpeg is primarily distributed under the GNU Lesser General Public License version 2.1 or later (LGPL-2.1+), while builds that enable GPL components are distributed under the GNU General Public License version 2 or later (GPL-2.0+).

Users should check the license information supplied with the FFmpeg build they choose to use.

## Notes

R800ZZ RVM Tools does not claim ownership of any of the third-party projects listed above.

Product names, project names, and trademarks belong to their respective owners.
