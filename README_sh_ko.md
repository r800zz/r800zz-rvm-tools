[English](README_sh_en.md) | [Русский](README_sh_ru.md) | [Español](README_sh_es.md) | [ภาษาไทย](README_sh_th.md) | [中文](README_sh_zh.md) | [한국어](README_sh_ko.md) | [日本語](README_sh_ja.md)

## UNIX 유사 운영 체제 (Linux, WSL, macOS)

R800ZZ RVM Tools는 Linux와 macOS에서도 사용할 수 있습니다.

Linux 동작은 R800ZZ가 **Windows 11의 WSL2에서 Ubuntu**를 사용하여 테스트했습니다.

테스트한 WSL2 환경에서는 CUDA를 통해 **NVIDIA GPU**를 RVM 추론에 성공적으로 사용했으며, Green-screen MP4와 WebM VP9 Alpha 동영상을 모두 성공적으로 생성했습니다.

이 테스트에는 macOS를 사용하지 않았습니다.

## 빠른 사용 가이드

먼저 Python, FFmpeg 및 필요한 Python 패키지를 설치하십시오.

Green-screen MP4를 생성하려면:

```bash
bash green.sh "input.mp4"
```

예:

```bash
bash green.sh "aaa.mp4"
```

출력:

```text
aaa_RVM_Green.mp4
```

WebM VP9 Alpha 동영상을 생성하려면:

```bash
bash alphavp9.sh "input.mp4"
```

예:

```bash
bash alphavp9.sh "aaa.mp4"
```

출력:

```text
aaa_RVM_Alpha.webm
```

동영상 파일 경로에는 절대 경로도 사용할 수 있습니다.

예:

```bash
bash green.sh "/home/user/Videos/aaa.mp4"
```

WSL2에서는 Windows C: 드라이브에 저장된 동영상을 다음과 같은 WSL 경로로 지정할 수 있습니다:

```bash
bash green.sh "/mnt/c/Videos/aaa.mp4"
```

## Linux 요구 사항

Python, FFmpeg, Git 및 Python 가상 환경 지원을 설치합니다.

Ubuntu / WSL2:

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv ffmpeg git
```

설치를 확인합니다:

```bash
python3 --version
ffmpeg -version
```

## Python 환경

Python 가상 환경을 생성합니다:

```bash
python3 -m venv .venv_linux
source .venv_linux/bin/activate
```

pip를 업그레이드합니다:

```bash
python -m pip install --upgrade pip
```

## Linux / WSL2의 NVIDIA GPU

CUDA를 지원하는 NVIDIA GPU를 사용하는 경우 CUDA 지원 버전의 PyTorch를 설치하십시오.

정확한 PyTorch CUDA 패키지는 현재 지원되는 PyTorch 환경과 일치해야 합니다.

설치 후 다음 명령으로 PyTorch가 NVIDIA GPU를 사용할 수 있는지 확인할 수 있습니다:

```bash
python -c "import torch; print(torch.__version__); print(torch.version.cuda); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
```

CUDA 사용 가능 여부에 다음이 표시되면:

```text
True
```

RVM은 NVIDIA GPU를 사용할 수 있습니다.

## FFmpeg

Linux에서는 패키지 관리자를 통해 설치된 시스템 FFmpeg를 사용합니다.

다음 명령을 터미널에서 사용할 수 있어야 합니다:

```bash
ffmpeg
ffprobe
```

Windows 버전과 달리 `ffmpeg.exe` 또는 `ffprobe.exe`를 R800ZZ RVM Tools 디렉터리에 둘 필요가 없습니다.

## WSL2 NVIDIA GPU 지원

WSL2를 사용할 때는 WSL 내부에서 NVIDIA GPU에 이미 접근할 수 있어야 합니다.

다음 명령으로 확인할 수 있습니다:

```bash
nvidia-smi
```

NVIDIA GPU가 표시되면 적절한 PyTorch 패키지를 설치한 후 CUDA 지원 PyTorch에서 GPU를 사용할 수 있습니다.

## Green-screen MP4

일반 동영상을 Green-screen MP4로 변환하려면:

```bash
bash green.sh "input.mp4"
```

RVM은 사람 전경을 추출하여 순수한 녹색 배경 위에 합성합니다.

예:

```text
Input:
aaa.mp4

Output:
aaa_RVM_Green.mp4
```

NVIDIA GPU 가속을 사용할 수 있는 경우 RVM 추론에 CUDA를 사용할 수 있습니다.

설치된 FFmpeg 빌드가 지원하는 경우 Green-screen MP4 변환에서 NVIDIA 하드웨어 H.264 인코딩도 사용할 수 있습니다.

## WebM VP9 Alpha

실제 알파 채널이 있는 WebM VP9 동영상을 생성하려면:

```bash
bash alphavp9.sh "input.mp4"
```

예:

```text
Input:
aaa.mp4

Output:
aaa_RVM_Alpha.webm
```

RVM은 사람 알파 매트를 생성하며, 이 정보는 WebM VP9 출력의 투명도 정보로 저장됩니다.

CUDA를 사용할 수 있는 경우 RVM 추론에 NVIDIA GPU를 사용할 수 있습니다.

WebM VP9 Alpha 인코딩 단계는 FFmpeg `libvpx-vp9`를 사용하며 CPU 기반으로 동작하므로 일반적으로 Green-screen MP4 변환보다 느립니다.

## macOS

Linux/macOS용 shell script 버전은 macOS도 지원하도록 되어 있습니다.

하지만 현재 Linux/macOS 버전은 실제 macOS 하드웨어가 아니라 R800ZZ가 **WSL2의 Ubuntu**에서 테스트했습니다.

따라서 macOS에서의 GPU 가속 동작은 R800ZZ가 확인하지 않았습니다.

CPU 동작에는 NVIDIA GPU가 필요하지 않습니다.
