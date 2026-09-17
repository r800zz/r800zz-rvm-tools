[English](README_sh_en.md) | [Русский](README_sh_ru.md) | [Español](README_sh_es.md) | [ภาษาไทย](README_sh_th.md) | [中文](README_sh_zh.md) | [한국어](README_sh_ko.md) | [日本語](README_sh_ja.md)

## Unix-like operating systems (Linux, WSL, macOS).

R800ZZ RVM Tools can also be used on Linux and macOS.

Linux operation has been tested by R800ZZ using **Ubuntu under WSL2 on Windows 11**.

The tested WSL2 environment successfully used an **NVIDIA GPU** for RVM inference through CUDA and successfully generated both Green-screen MP4 and WebM VP9 Alpha videos.

macOS was not used for this test.

## Quick Usage Guide

Install Python, FFmpeg, and the required Python packages first.

To create a Green-screen MP4:

```bash
bash green.sh "input.mp4"
```

Example:

```bash
bash green.sh "aaa.mp4"
```

Output:

```text
aaa_RVM_Green.mp4
```

To create a WebM VP9 Alpha video:

```bash
bash alphavp9.sh "input.mp4"
```

Example:

```bash
bash alphavp9.sh "aaa.mp4"
```

Output:

```text
aaa_RVM_Alpha.webm
```

The video file path may also be an absolute path.

For example:

```bash
bash green.sh "/home/user/Videos/aaa.mp4"
```

Under WSL2, a video stored on the Windows C: drive can be specified using a WSL path such as:

```bash
bash green.sh "/mnt/c/Videos/aaa.mp4"
```

## Linux requirements

Install Python, FFmpeg, Git, and Python virtual-environment support.

On Ubuntu / WSL2:

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv ffmpeg git
```

Check the installations:

```bash
python3 --version
ffmpeg -version
```

## Python environment

Create a Python virtual environment:

```bash
python3 -m venv .venv_linux
source .venv_linux/bin/activate
```

Upgrade pip:

```bash
python -m pip install --upgrade pip
```

## NVIDIA GPU on Linux / WSL2

When using an NVIDIA GPU with CUDA support, install the CUDA-enabled version of PyTorch.

The exact PyTorch CUDA package should match the currently supported PyTorch environment.

After installation, you can check whether PyTorch can use the NVIDIA GPU with:

```bash
python -c "import torch; print(torch.__version__); print(torch.version.cuda); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
```

If:

```text
True
```

is displayed for CUDA availability, RVM can use the NVIDIA GPU.

## FFmpeg

On Linux, the system FFmpeg installed through the package manager is used.

The following commands must be available from the terminal:

```bash
ffmpeg
ffprobe
```

Unlike the Windows version, you do not need to place `ffmpeg.exe` or `ffprobe.exe` in the R800ZZ RVM Tools directory.

## WSL2 NVIDIA GPU support

When using WSL2, NVIDIA GPU access must already be available inside WSL.

You can check it with:

```bash
nvidia-smi
```

If the NVIDIA GPU is displayed, CUDA-enabled PyTorch can use the GPU after the appropriate PyTorch package has been installed.

## Green-screen MP4

To convert an ordinary video into a Green-screen MP4:

```bash
bash green.sh "input.mp4"
```

RVM extracts the human foreground and composites it over a pure green background.

Example:

```text
Input:
aaa.mp4

Output:
aaa_RVM_Green.mp4
```

When NVIDIA GPU acceleration is available, RVM inference can use CUDA.

Green-screen MP4 conversion can also use NVIDIA hardware H.264 encoding when supported by the installed FFmpeg build.

## WebM VP9 Alpha

To create a WebM VP9 video with a real alpha channel:

```bash
bash alphavp9.sh "input.mp4"
```

Example:

```text
Input:
aaa.mp4

Output:
aaa_RVM_Alpha.webm
```

RVM generates the human alpha matte, which is stored as the transparency information in the WebM VP9 output.

RVM inference can use the NVIDIA GPU when CUDA is available.

The WebM VP9 Alpha encoding stage uses FFmpeg `libvpx-vp9` and is CPU-based, so this conversion is normally slower than Green-screen MP4 conversion.

## macOS

The Linux/macOS shell-script version is intended to support macOS as well.

However, the current Linux/macOS version has been tested by R800ZZ on **Ubuntu under WSL2**, not on physical macOS hardware.

GPU acceleration behavior on macOS has therefore not been verified by R800ZZ.

CPU operation does not require an NVIDIA GPU.
