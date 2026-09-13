# R800ZZ RVM Tools

[English](README.md) | [Русский](README_ru.md) | [Español](README_es.md) | [ภาษาไทย](README_th.md) | [中文](README_zh.md) | [한국어](README_ko.md) | [日本語](README_ja.md)

R800ZZ RVM Tools 可将普通视频文件转换为适合背景透明显示的视频。

它使用 **Robust Video Matting (RVM)** 提取人物前景，并使用 **FFmpeg** 进行视频解码和编码。

支持两种输出模式：

- **绿幕 MP4** — 将提取出的人物合成到纯绿色背景上，并生成 H.264 MP4。
- **WebM VP9 Alpha** — 生成带有真实 Alpha 通道的 WebM VP9 视频。

不要求使用高性能 GPU。该工具可以仅使用 CPU 运行，不过使用 GPU 加速可以大幅提高 RVM 处理速度。

## 快速使用说明

- 前提条件：安装 Python 和 FFmpeg。

- 第一次使用时，请运行 `install_python_packages_NVIDIA.bat`。

- 如果要转换为绿色背景视频，请将视频文件拖放到 `R800ZZ_Make_Green_MP4_NVIDIA.bat` 上。

- 如果要转换为 Alpha 透明（WebM VP9）视频，请将视频文件拖放到 `R800ZZ_Make_WebM_Alpha_NVIDIA.bat` 上。

## 什么是 RVM？

RVM 是 **Robust Video Matting** 的缩写。

RVM 是一种基于神经网络的人像视频抠图模型，用于在保留视频帧之间时间信息的同时将人物与背景分离。

本工具通过 PyTorch Torch Hub 使用上游 RVM 项目。

RVM 的源代码和预训练模型**不包含在本仓库中**。需要时会从上游项目自动下载。

## 输出模式

### 绿幕 MP4

RVM 提取出的人物会被合成到纯绿色背景上，并编码为 H.264 MP4。

输出示例：

```text
aaa_RVM_Green.mp4
```

此模式适用于支持 chroma key 透明功能的 VR 视频播放器。

示例：

- [适用于 PICO/Meta 的 R800ZZbrowser](https://vr180g.com/browser/browser.php?l=cn)
- [适用于 PICO 4 Ultra/PICO4 的 r800zzvrplayer](https://vr180g.com/pico/vrplayer.php?l=cn)

绿幕转换通常比 WebM VP9 Alpha 转换快很多。

在支持的环境中，本工具会使用 H.264 硬件编码：

| 硬件 | RVM 推理 | H.264 编码器 |
| --- | --- | --- |
| NVIDIA GPU | PyTorch CUDA | `h264_nvenc` |
| AMD GPU | PyTorch DirectML | `h264_amf` |
| Intel GPU / Intel 核显 | PyTorch DirectML | `h264_qsv` |
| 仅 CPU | PyTorch CPU | `libx264` |

### WebM VP9 Alpha

此模式会生成使用 VP9 编码并带有真实 Alpha 通道的 WebM 视频。

输出示例：

```text
aaa_RVM_Alpha.webm
```

这**不是 R800ZZ 自定义的 Alpha 视频格式**。

VP9 是 WebM Project 的开放视频编解码器，WebM 支持带 Alpha 通道的视频。Alpha 数据使用 WebM 的 Alpha 机制进行保存，而不是把自定义遮罩图像放在视频帧的未使用区域。

本工具生成的 WebM VP9 Alpha 当前使用 FFmpeg `libvpx-vp9` 编码。即使 RVM 推理使用 GPU，VP9 Alpha 编码阶段仍由 CPU 完成。因此，WebM VP9 Alpha 转换可能明显慢于绿幕 MP4 转换。

### 支持这些输出的 VR 播放器

对于绿幕 MP4，支持 chroma key 功能的 VR 播放器示例包括：

- [适用于 PICO/Meta 的 R800ZZbrowser](https://vr180g.com/browser/browser.php?l=cn)
- [适用于 PICO 4 Ultra/PICO4 的 r800zzvrplayer](https://vr180g.com/pico/vrplayer.php?l=cn)

对于 WebM VP9 Alpha，我已确认支持的 VR 播放器是：

- **[r800zzvrplayer 0.4 或更高版本](https://vr180g.com/pico/vrplayer.php?l=cn)**

截至本文编写时，我尚未确认有其他 VR 视频播放器能够直接播放 WebM VP9 视频，并将其 Alpha 通道作为 VR 透明度使用。

这并不是说不存在其他兼容的 VR 播放器。如果您知道其他播放器，请告诉我。

## 系统要求

- Windows 10 或 Windows 11
- Python
- FFmpeg
- 初始设置以及第一次运行 RVM 时需要互联网连接
- CPU，或受支持的 NVIDIA / AMD / Intel GPU

为了尽可能兼容所提供的 NVIDIA、AMD 和 Intel 设置脚本，建议使用 **Python 3.10 至 3.12**。

## 安装

### 1. 安装 Python

安装 Windows 版 Python。

Python 本身**不会由 R800ZZ RVM Tools 自动安装**。

安装 Python 时，建议启用将 Python 添加到 `PATH` 的选项。

可以在命令提示符中使用以下命令确认安装：

```bat
python --version
```

### 2. 安装 FFmpeg

FFmpeg 不包含在本仓库中。

请下载至少包含以下内容的 Windows 版 FFmpeg：

- `ffmpeg.exe`
- `ffprobe.exe`
- `libvpx-vp9`
- `libopus`
- `libx264`

如果要使用 GPU 加速绿幕 MP4 编码，FFmpeg 版本还应包含对应 GPU 的编码器：

- NVIDIA: `h264_nvenc`
- AMD: `h264_amf`
- Intel: `h264_qsv`

最简单的设置方式是将：

```text
ffmpeg.exe
ffprobe.exe
```

放在与：

```text
r800zz_rvm_video.py
```

以及 BAT 文件相同的文件夹中。

使用这种方式时，**不需要**为 FFmpeg 设置 Windows 的 `PATH` 环境变量。

也可以把 FFmpeg 安装到其他位置，只要将它的 `bin` 目录添加到 `PATH` 即可。

可以使用以下命令检查可用的硬件编码器：

```bat
ffmpeg -encoders
```

### 3. 根据硬件安装 PyTorch

PyTorch 不随本仓库一起提供。

设置用 BAT 文件会从官方软件源下载所需的 Python 软件包。

请选择与您的硬件对应的设置方式。

#### NVIDIA GPU

运行：

```text
install_python_packages.bat
```

它会安装或更新普通 NVIDIA/CPU BAT 文件所使用的 CUDA 版 PyTorch 环境。

安装的软件包会被放入 `python` 命令所使用的 Python 环境中，通常位于该 Python 安装目录下的：

```text
Lib\site-packages
```

NVIDIA GPU 路径是 R800ZZ 实际测试过的 GPU 配置。

#### AMD GPU

运行：

```text
install_python_packages_AMD.bat
```

它会在 R800ZZ RVM Tools 文件夹中创建一个独立的 Python 虚拟环境：

```text
.venv_amd
```

并在其中安装 `torch-directml`。

转换时请使用文件名以：

```text
_AMD.bat
```

结尾的 BAT 文件。

AMD GPU 支持通过 DirectML 实现。R800ZZ 尚未在真实 AMD GPU 硬件上进行测试。

#### Intel GPU / Intel 核显

运行：

```text
install_python_packages_Intel.bat
```

它会在 R800ZZ RVM Tools 文件夹中创建一个独立的 Python 虚拟环境：

```text
.venv_intel
```

并在其中安装 `torch-directml`。

转换时请使用文件名以：

```text
_Intel.bat
```

结尾的 BAT 文件。

Intel GPU 支持通过 DirectML 实现；在可用时，绿幕 MP4 会使用 Intel Quick Sync Video（`h264_qsv`）。

R800ZZ 尚未在真实 Intel GPU 硬件上进行测试。

#### 仅 CPU

不需要 GPU。

对于仅使用 CPU 的环境，请安装 CPU 版 PyTorch：

```bat
python -m pip install --upgrade pip
python -m pip install numpy
python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

标准转换 BAT 文件会在 CUDA 不可用时自动使用 CPU 处理。

CPU 转换通常会比 GPU 加速的 RVM 推理更慢。

## PyTorch 和 RVM 会下载到哪里？

### PyTorch

对于普通 NVIDIA/CPU 环境，PyTorch 会安装到 `python` 命令所使用的 Python 环境中。

例如，常见的 Python 安装可能会将软件包保存在：

```text
C:\Users\<username>\AppData\Local\Programs\Python\Python3xx\Lib\site-packages
```

具体位置取决于 Python 的安装方式。

对于 AMD 和 Intel，附带的设置脚本会使用本地虚拟环境：

```text
R800ZZ_RVM_Tools\.venv_amd
R800ZZ_RVM_Tools\.venv_intel
```

### RVM

RVM 通过 PyTorch Torch Hub 加载。

第一次转换时，Torch Hub 会自动下载 RVM 仓库以及预训练的 MobileNetV3 模型。

Windows 上 Torch Hub 的默认缓存通常位于：

```text
C:\Users\<username>\.cache\torch\hub
```

RVM 仓库缓存通常会出现在该目录下。

下载的模型权重通常保存在：

```text
C:\Users\<username>\.cache\torch\hub\checkpoints
```

具体缓存位置可以通过 `TORCH_HOME` 等 PyTorch 环境设置进行更改。

文件缓存后，后续转换会继续复用这些文件。

## 使用方法

转换操作通过**在 Windows 文件资源管理器中，将视频文件拖放到对应的 `.bat` 文件上**完成。

例如，如果您有：

```text
aaa.mp4
```

并希望使用 NVIDIA GPU 或 CPU 创建绿幕 MP4，请拖动：

```text
aaa.mp4
```

然后直接放到：

```text
R800ZZ_Make_Green_MP4.bat
```

BAT 文件会接收拖入的视频文件并自动开始转换。

同样，如果要创建 WebM VP9 Alpha 视频，请拖动：

```text
aaa.mp4
```

并放到：

```text
R800ZZ_Make_WebM_Alpha.bat
```

不需要打开命令提示符并手动输入视频文件名。

### 创建绿幕 MP4

使用 NVIDIA GPU 或 CPU 时，将视频文件拖放到：

```text
R800ZZ_Make_Green_MP4.bat
```

使用 AMD GPU 时：

```text
R800ZZ_Make_Green_MP4_AMD.bat
```

使用 Intel GPU 时：

```text
R800ZZ_Make_Green_MP4_Intel.bat
```

示例：

```text
aaa.mp4
    ↓ 拖放
R800ZZ_Make_Green_MP4.bat
```

输出：

```text
aaa_RVM_Green.mp4
```

### 创建 WebM VP9 Alpha

使用 NVIDIA GPU 或 CPU 时，将视频文件拖放到：

```text
R800ZZ_Make_WebM_Alpha.bat
```

使用 AMD GPU 时：

```text
R800ZZ_Make_WebM_Alpha_AMD.bat
```

使用 Intel GPU 时：

```text
R800ZZ_Make_WebM_Alpha_Intel.bat
```

示例：

```text
aaa.mp4
    ↓ 拖放
R800ZZ_Make_WebM_Alpha.bat
```

输出：

```text
aaa_RVM_Alpha.webm
```

默认情况下，BAT 文件会把转换后的视频保存在 R800ZZ RVM Tools 文件夹中。

## 性能说明

GPU 加速不是必需的。

当前处理流程包含多个不同阶段，并非所有阶段都使用 GPU 加速。

### NVIDIA

- RVM 推理：CUDA GPU
- 绿幕 MP4 H.264 编码：NVENC
- WebM VP9 Alpha 编码：CPU（`libvpx-vp9`）
- FFmpeg 输入视频解码：当前实现中使用 CPU

### AMD

- RVM 推理：DirectML
- 绿幕 MP4 H.264 编码：AMF
- WebM VP9 Alpha 编码：CPU（`libvpx-vp9`）
- FFmpeg 输入视频解码：当前实现中使用 CPU

### Intel

- RVM 推理：DirectML
- 绿幕 MP4 H.264 编码：Quick Sync Video
- WebM VP9 Alpha 编码：CPU（`libvpx-vp9`）
- FFmpeg 输入视频解码：当前实现中使用 CPU

由于 WebM VP9 Alpha 编码使用 CPU，因此即使 GPU 非常快，也不会让整个 Alpha 转换过程获得同等幅度的加速。

绿幕 MP4 转换能够更充分地受益于 GPU 加速，因为 RVM 推理和 H.264 编码都可以使用 GPU 硬件。

## 关于抠图质量

RVM 并不是通过判断某种特定背景颜色来去除背景。

它使用神经网络估算人物前景和 Alpha matte。

因此，输入视频并不需要使用绿色背景。

绿幕 MP4 模式会先使用 RVM 完成人像抠图，然后把提取出的前景放到新生成的绿色背景上。

WebM VP9 Alpha 模式会直接使用 RVM 的 Alpha matte 作为输出视频的透明度信息。

结果可能会受到源视频、运动、头发细节、遮挡、照明以及 RVM 精度等因素影响。

## 硬件测试状态

R800ZZ 已测试 NVIDIA GPU 路径。

工具中包含 AMD GPU 和 Intel GPU 加速支持，但 R800ZZ 尚未亲自在真实 AMD 或 Intel GPU 系统上测试这些路径。

仅使用 CPU 时不需要独立显卡。

## 第三方软件

R800ZZ RVM Tools 使用或配合以下项目工作：

- Robust Video Matting
- PyTorch
- Torch-DirectML
- FFmpeg

RVM 是独立于 R800ZZ RVM Tools 开发的项目。

本仓库不包含 RVM 源代码或预训练模型文件。

## 免责声明

R800ZZ RVM Tools 是独立的实用工具。

输出文件的兼容性取决于用于播放的视频播放器的功能。

绿幕 MP4 需要支持 chroma key 的播放器。

WebM VP9 Alpha 需要播放器真正解码并使用 WebM 的 Alpha 通道。播放器支持普通 WebM VP9 视频，并不一定意味着它支持 VP9 Alpha 透明。
