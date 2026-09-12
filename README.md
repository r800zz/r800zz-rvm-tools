# R800ZZ RVM Tools

R800ZZ RVM Tools converts ordinary video files into videos suitable for background transparency.

It uses **Robust Video Matting (RVM)** for human foreground extraction and **FFmpeg** for video decoding and encoding.

Two output modes are supported:

- **Green-screen MP4** — creates an H.264 MP4 with the extracted person composited over a pure green background.
- **WebM VP9 Alpha** — creates a WebM VP9 video with a real alpha channel.

A high-performance GPU is not required. The tool can run on CPU only, although GPU acceleration can make RVM processing much faster.

## What is RVM?

RVM stands for **Robust Video Matting**.

RVM is a neural-network-based human video matting model designed to separate people from the background while preserving temporal information between video frames.

This tool uses the upstream RVM project through PyTorch Torch Hub.

The RVM source code and pretrained model are **not included in this repository**. They are downloaded from the upstream project when required.

## Output modes

### Green-screen MP4

The person extracted by RVM is composited over a pure green background and encoded as H.264 MP4.

Example output:

```text
aaa_RVM_Green.mp4
```

This mode is intended for VR video players that support chroma key transparency.

Examples:

- R800ZZbrowser
- r800zzvrplayer

Green-screen conversion is usually much faster than WebM VP9 Alpha conversion.

When supported, the tool uses hardware H.264 encoding:

| Hardware | RVM inference | H.264 encoder |
| --- | --- | --- |
| NVIDIA GPU | PyTorch CUDA | `h264_nvenc` |
| AMD GPU | PyTorch DirectML | `h264_amf` |
| Intel GPU / Intel integrated GPU | PyTorch DirectML | `h264_qsv` |
| CPU only | PyTorch CPU | `libx264` |

### WebM VP9 Alpha

This mode creates a WebM video using VP9 with a real alpha channel.

Example output:

```text
aaa_RVM_Alpha.webm
```

This is **not an R800ZZ-specific alpha-video format**.

VP9 is an open video codec from the WebM Project, and WebM supports alpha-channel video. Alpha data is stored using the WebM alpha mechanism rather than by placing a custom mask image in an unused area of the video frame.

The WebM VP9 Alpha output created by this tool is currently encoded with FFmpeg `libvpx-vp9`. The VP9 alpha encoding stage is CPU-based, even when RVM inference uses a GPU. For this reason, WebM VP9 Alpha conversion can be significantly slower than Green-screen MP4 conversion.

### VR players supporting the output

For Green-screen MP4, examples of VR players with chroma-key functionality include:

- R800ZZbrowser
- r800zzvrplayer

For WebM VP9 Alpha, the VR player I have confirmed is:

- **r800zzvrplayer 0.4 or later**

At the time of writing, I have not been able to confirm another VR video player that directly plays WebM VP9 video with its alpha channel as VR transparency.

This is not a claim that no other compatible VR player exists. If you know of another one, please let me know.

## Requirements

- Windows 10 or Windows 11
- Python
- FFmpeg
- Internet access during initial setup and the first RVM run
- CPU, or a supported NVIDIA / AMD / Intel GPU

For the widest compatibility with the provided NVIDIA, AMD, and Intel setup scripts, **Python 3.10 to 3.12 is recommended**.

## Installation

### 1. Install Python

Install Python for Windows.

Python itself is **not automatically installed by R800ZZ RVM Tools**.

During Python installation, enabling the option to add Python to `PATH` is recommended.

You can verify the installation from Command Prompt:

```bat
python --version
```

### 2. Install FFmpeg

FFmpeg is not included in this repository.

Download a Windows build of FFmpeg containing at least:

- `ffmpeg.exe`
- `ffprobe.exe`
- `libvpx-vp9`
- `libopus`
- `libx264`

For GPU-accelerated Green-screen MP4 output, the FFmpeg build should also contain the encoder for your GPU:

- NVIDIA: `h264_nvenc`
- AMD: `h264_amf`
- Intel: `h264_qsv`

The easiest setup is to place:

```text
ffmpeg.exe
ffprobe.exe
```

in the same folder as:

```text
r800zz_rvm_video.py
```

and the BAT files.

In this configuration, you do **not** need to configure the Windows `PATH` environment variable for FFmpeg.

Alternatively, FFmpeg may be installed elsewhere if its `bin` directory is added to `PATH`.

You can check available hardware encoders with:

```bat
ffmpeg -encoders
```

### 3. Install PyTorch for your hardware

PyTorch is not bundled with this repository.

The setup BAT files download the required Python packages from their official package sources.

Choose the setup method matching your hardware.

#### NVIDIA GPU

Run:

```text
install_python_packages.bat
```

This installs or updates the CUDA-enabled PyTorch environment used by the normal NVIDIA/CPU BAT files.

The installed packages are placed in the Python environment selected by the `python` command, normally under that Python installation's:

```text
Lib\site-packages
```

The NVIDIA GPU path is the GPU configuration tested by R800ZZ.

#### AMD GPU

Run:

```text
install_python_packages_AMD.bat
```

This creates an isolated Python virtual environment:

```text
.venv_amd
```

inside the R800ZZ RVM Tools folder and installs `torch-directml` there.

Use the BAT files ending in:

```text
_AMD.bat
```

for conversion.

AMD GPU support is provided through DirectML. It has not been tested on physical AMD hardware by R800ZZ.

#### Intel GPU / Intel integrated GPU

Run:

```text
install_python_packages_Intel.bat
```

This creates an isolated Python virtual environment:

```text
.venv_intel
```

inside the R800ZZ RVM Tools folder and installs `torch-directml` there.

Use the BAT files ending in:

```text
_Intel.bat
```

for conversion.

Intel GPU support is provided through DirectML, and Green-screen MP4 uses Intel Quick Sync Video (`h264_qsv`) when available.

It has not been tested on physical Intel GPU hardware by R800ZZ.

#### CPU only

A GPU is not required.

For a CPU-only environment, install the CPU version of PyTorch:

```bat
python -m pip install --upgrade pip
python -m pip install numpy
python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

The standard conversion BAT files automatically use CPU processing when CUDA is not available.

CPU conversion will normally be slower than GPU-accelerated RVM inference.

## Where are PyTorch and RVM downloaded?

### PyTorch

For the normal NVIDIA/CPU environment, PyTorch is installed into the Python environment used by the `python` command.

For example, a normal Python installation may store packages under:

```text
C:\Users\<username>\AppData\Local\Programs\Python\Python3xx\Lib\site-packages
```

The exact location depends on how Python was installed.

For AMD and Intel, the provided setup scripts use local virtual environments:

```text
R800ZZ_RVM_Tools\.venv_amd
R800ZZ_RVM_Tools\.venv_intel
```

### RVM

RVM is loaded with PyTorch Torch Hub.

On the first conversion, Torch Hub automatically downloads the RVM repository and pretrained MobileNetV3 model.

The default Torch Hub cache on Windows is normally under:

```text
C:\Users\<username>\.cache\torch\hub
```

The RVM repository cache will normally appear below that directory.

Downloaded model weights are normally stored below:

```text
C:\Users\<username>\.cache\torch\hub\checkpoints
```

The exact cache location can be changed by PyTorch environment settings such as `TORCH_HOME`.

After the files have been cached, they are reused on later conversions.

## How to use

Conversion is performed by **dragging and dropping a video file onto the appropriate `.bat` file in Windows Explorer**.

For example, if you have:

```text
aaa.mp4
```

and want to create a Green-screen MP4 using an NVIDIA GPU or CPU, drag:

```text
aaa.mp4
```

and drop it directly onto:

```text
R800ZZ_Make_Green_MP4.bat
```

The BAT file receives the dropped video file and starts the conversion automatically.

Similarly, to create a WebM VP9 Alpha video, drag:

```text
aaa.mp4
```

and drop it onto:

```text
R800ZZ_Make_WebM_Alpha.bat
```

You do not need to open a Command Prompt and manually type the video file name.

### Create Green-screen MP4

For NVIDIA GPU or CPU, drag and drop the video file onto:

```text
R800ZZ_Make_Green_MP4.bat
```

For AMD GPU:

```text
R800ZZ_Make_Green_MP4_AMD.bat
```

For Intel GPU:

```text
R800ZZ_Make_Green_MP4_Intel.bat
```

Example:

```text
aaa.mp4
    ↓ drag and drop
R800ZZ_Make_Green_MP4.bat
```

Output:

```text
aaa_RVM_Green.mp4
```

### Create WebM VP9 Alpha

For NVIDIA GPU or CPU, drag and drop the video file onto:

```text
R800ZZ_Make_WebM_Alpha.bat
```

For AMD GPU:

```text
R800ZZ_Make_WebM_Alpha_AMD.bat
```

For Intel GPU:

```text
R800ZZ_Make_WebM_Alpha_Intel.bat
```

Example:

```text
aaa.mp4
    ↓ drag and drop
R800ZZ_Make_WebM_Alpha.bat
```

Output:

```text
aaa_RVM_Alpha.webm
```

By default, the BAT files place the converted video in the R800ZZ RVM Tools folder.

## Performance notes

GPU acceleration is optional.

The current processing pipeline contains several different stages, and not every stage is GPU accelerated.

### NVIDIA

- RVM inference: CUDA GPU
- Green MP4 H.264 encoding: NVENC
- WebM VP9 Alpha encoding: CPU (`libvpx-vp9`)
- FFmpeg input video decoding: CPU in the current implementation

### AMD

- RVM inference: DirectML
- Green MP4 H.264 encoding: AMF
- WebM VP9 Alpha encoding: CPU (`libvpx-vp9`)
- FFmpeg input video decoding: CPU in the current implementation

### Intel

- RVM inference: DirectML
- Green MP4 H.264 encoding: Quick Sync Video
- WebM VP9 Alpha encoding: CPU (`libvpx-vp9`)
- FFmpeg input video decoding: CPU in the current implementation

Because WebM VP9 Alpha encoding uses the CPU, a very fast GPU does not make the entire Alpha conversion process equally fast.

Green-screen MP4 conversion can benefit much more from GPU acceleration because both RVM inference and H.264 encoding can use GPU hardware.

## Notes about matting quality

RVM does not remove the background by checking for a specific background color.

It estimates the human foreground and alpha matte using a neural network.

Therefore, the input video does not need to have a green background.

The Green-screen MP4 mode first performs RVM human matting and then places the extracted foreground over a newly generated green background.

The WebM VP9 Alpha mode uses the RVM alpha matte directly as the output video's transparency information.

Results can still vary depending on the source video, motion, hair detail, occlusion, lighting, and the accuracy of RVM.

## Hardware testing status

R800ZZ has tested the NVIDIA GPU path.

AMD GPU acceleration and Intel GPU acceleration are included, but R800ZZ has not personally tested those paths on physical AMD or Intel GPU systems.

CPU operation does not require a discrete GPU.

## Third-party software

R800ZZ RVM Tools uses or works with the following projects:

- Robust Video Matting
- PyTorch
- Torch-DirectML
- FFmpeg

RVM is developed separately from R800ZZ RVM Tools.

This repository does not include the RVM source code or pretrained model files.

## Disclaimer

R800ZZ RVM Tools is an independent utility.

Output compatibility depends on the capabilities of the video player used for playback.

Green-screen MP4 requires a player with chroma-key support.

WebM VP9 Alpha requires a player that actually decodes and uses the WebM alpha channel. A player supporting ordinary WebM VP9 video does not necessarily support VP9 alpha transparency.
