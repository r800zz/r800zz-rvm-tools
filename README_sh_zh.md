[English](README_sh_en.md) | [Русский](README_sh_ru.md) | [Español](README_sh_es.md) | [ภาษาไทย](README_sh_th.md) | [中文](README_sh_zh.md) | [한국어](README_sh_ko.md) | [日本語](README_sh_ja.md)

## 类 UNIX 操作系统（Linux、WSL、macOS）

R800ZZ RVM Tools 也可以在 Linux 和 macOS 上使用。

R800ZZ 已使用 **Windows 11 上 WSL2 中的 Ubuntu** 测试了 Linux 环境下的运行。

在测试的 WSL2 环境中，成功通过 CUDA 使用 **NVIDIA GPU** 进行 RVM 推理，并成功生成了 Green-screen MP4 和 WebM VP9 Alpha 两种视频。

本次测试未使用 macOS。

## 快速使用指南

请先安装 Python、FFmpeg 和所需的 Python 软件包。

创建 Green-screen MP4:

```bash
bash green.sh "input.mp4"
```

示例:

```bash
bash green.sh "aaa.mp4"
```

输出:

```text
aaa_RVM_Green.mp4
```

创建 WebM VP9 Alpha 视频:

```bash
bash alphavp9.sh "input.mp4"
```

示例:

```bash
bash alphavp9.sh "aaa.mp4"
```

输出:

```text
aaa_RVM_Alpha.webm
```

视频文件路径也可以使用绝对路径。

例如:

```bash
bash green.sh "/home/user/Videos/aaa.mp4"
```

在 WSL2 中，存储在 Windows C: 盘上的视频可以使用如下 WSL 路径指定:

```bash
bash green.sh "/mnt/c/Videos/aaa.mp4"
```

## Linux 要求

安装 Python、FFmpeg、Git 和 Python 虚拟环境支持。

在 Ubuntu / WSL2 上:

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv ffmpeg git
```

检查安装:

```bash
python3 --version
ffmpeg -version
```

## Python 环境

创建 Python 虚拟环境:

```bash
python3 -m venv .venv_linux
source .venv_linux/bin/activate
```

升级 pip:

```bash
python -m pip install --upgrade pip
```

## Linux / WSL2 上的 NVIDIA GPU

使用支持 CUDA 的 NVIDIA GPU 时，请安装支持 CUDA 的 PyTorch 版本。

具体的 PyTorch CUDA 软件包应与当前受支持的 PyTorch 环境相匹配。

安装后，可以使用以下命令检查 PyTorch 是否可以使用 NVIDIA GPU:

```bash
python -c "import torch; print(torch.__version__); print(torch.version.cuda); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
```

如果 CUDA 可用性显示:

```text
True
```

则 RVM 可以使用 NVIDIA GPU。

## FFmpeg

在 Linux 上，使用通过包管理器安装的系统 FFmpeg。

以下命令必须可以从终端运行:

```bash
ffmpeg
ffprobe
```

与 Windows 版本不同，不需要将 `ffmpeg.exe` 或 `ffprobe.exe` 放入 R800ZZ RVM Tools 目录。

## WSL2 NVIDIA GPU 支持

使用 WSL2 时，必须已经能够从 WSL 内部访问 NVIDIA GPU。

可以使用以下命令检查:

```bash
nvidia-smi
```

如果显示 NVIDIA GPU，则在安装适当的 PyTorch 软件包后，支持 CUDA 的 PyTorch 可以使用该 GPU。

## Green-screen MP4

将普通视频转换为 Green-screen MP4:

```bash
bash green.sh "input.mp4"
```

RVM 会提取人物前景，并将其合成到纯绿色背景上。

示例:

```text
Input:
aaa.mp4

Output:
aaa_RVM_Green.mp4
```

当 NVIDIA GPU 加速可用时，RVM 推理可以使用 CUDA。

如果已安装的 FFmpeg 构建支持，Green-screen MP4 转换还可以使用 NVIDIA 硬件 H.264 编码。

## WebM VP9 Alpha

创建具有真实 Alpha 通道的 WebM VP9 视频:

```bash
bash alphavp9.sh "input.mp4"
```

示例:

```text
Input:
aaa.mp4

Output:
aaa_RVM_Alpha.webm
```

RVM 会生成人物 Alpha 遮罩，并将其作为透明度信息存储在 WebM VP9 输出中。

当 CUDA 可用时，RVM 推理可以使用 NVIDIA GPU。

WebM VP9 Alpha 编码阶段使用 FFmpeg `libvpx-vp9`，并基于 CPU 运行，因此这种转换通常比 Green-screen MP4 转换更慢。

## macOS

Linux/macOS 的 shell 脚本版本也计划支持 macOS。

但是，当前 Linux/macOS 版本由 R800ZZ 在 **WSL2 下的 Ubuntu** 上进行了测试，而不是在实际 macOS 硬件上测试。

因此，R800ZZ 尚未验证 macOS 上的 GPU 加速行为。

CPU 运行不需要 NVIDIA GPU。
