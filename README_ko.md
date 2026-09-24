# R800ZZ RVM Tools

[English](README.md) | [Русский](README_ru.md) | [Español](README_es.md) | [ภาษาไทย](README_th.md) | [中文](README_zh.md) | [한국어](README_ko.md) | [日本語](README_ja.md)

Windows와 NVIDIA GPU를 사용한다면 [r800zzXRdlnaServer for Windows+NVIDIA GPU](https://github.com/r800zz/r800zzxrdlnaserver/blob/main/README_ko.md)를 사용하는 것이 더 좋습니다.

R800ZZ RVM Tools는 일반 동영상 파일을 배경 투명 처리에 적합한 동영상으로 변환하는 도구입니다.

사람 전경 추출에는 **Robust Video Matting (RVM)**을 사용하고, 동영상 디코딩과 인코딩에는 **FFmpeg**를 사용합니다.

두 가지 출력 모드를 지원합니다.

- **그린 배경 MP4** — 추출한 사람을 순수한 녹색 배경 위에 합성한 H.264 MP4를 생성합니다.
- **WebM VP9 Alpha** — 실제 알파 채널을 가진 WebM VP9 동영상을 생성합니다.

고성능 GPU는 필수가 아닙니다. CPU만으로도 실행할 수 있지만, GPU 가속을 사용하면 RVM 처리를 크게 빠르게 할 수 있습니다.

[README , Unix 계열 운영 체제(Linux , WSL , macOS)](README_sh_ko.md)

## 업데이트 기록

### 2026년 9월 17일

* 알파 모드의 배경 렌더링 문제를 수정했습니다.
* Unix 계열 운영 체제(Linux, WSL, macOS)용 Bash 스크립트를 추가했습니다.


## 빠른 사용 안내 (Windows)

- 사전 준비: Python과 FFmpeg를 설치합니다.

- 처음 사용할 때 `install_python_packages_NVIDIA.bat`를 실행합니다.

- 그린 배경 동영상으로 변환하려면 동영상 파일을 `R800ZZ_Make_Green_MP4_NVIDIA.bat`에 드래그 앤 드롭합니다.

- Alpha 투명(WebM VP9) 동영상으로 변환하려면 동영상 파일을 `R800ZZ_Make_WebM_Alpha_NVIDIA.bat`에 드래그 앤 드롭합니다.

## RVM이란?

RVM은 **Robust Video Matting**의 약자입니다.

RVM은 동영상 프레임 사이의 시간 정보를 유지하면서 사람과 배경을 분리하도록 설계된 신경망 기반 사람 동영상 매팅 모델입니다.

이 도구는 PyTorch Torch Hub를 통해 원본 RVM 프로젝트를 사용합니다.

RVM 소스 코드와 사전 학습 모델은 **이 저장소에 포함되어 있지 않습니다**. 필요할 때 원본 프로젝트에서 다운로드합니다.

## 출력 모드

### 그린 배경 MP4

RVM으로 추출한 사람을 순수한 녹색 배경 위에 합성하고 H.264 MP4로 인코딩합니다.

출력 예:

```text
aaa_RVM_Green.mp4
```

이 모드는 크로마키 투명을 지원하는 VR 동영상 플레이어용입니다.

예:

- [PICO/Meta용 R800ZZbrowser](https://vr180g.com/browser/browser.php?l=kr)
- [PICO/Meta용 r800zzvrplayer](https://vr180g.com/pico/vrplayer.php?l=kr)

그린 배경 변환은 일반적으로 WebM VP9 Alpha 변환보다 훨씬 빠릅니다.

지원되는 환경에서는 하드웨어 H.264 인코딩을 사용합니다.

| 하드웨어 | RVM 추론 | H.264 인코더 |
| --- | --- | --- |
| NVIDIA GPU | PyTorch CUDA | `h264_nvenc` |
| AMD GPU | PyTorch DirectML | `h264_amf` |
| Intel GPU / Intel 내장 GPU | PyTorch DirectML | `h264_qsv` |
| CPU만 사용 | PyTorch CPU | `libx264` |

### WebM VP9 Alpha

이 모드는 실제 알파 채널을 가진 VP9 WebM 동영상을 생성합니다.

출력 예:

```text
aaa_RVM_Alpha.webm
```

이 형식은 **R800ZZ 전용 Alpha 동영상 형식이 아닙니다**.

VP9은 WebM Project의 오픈 비디오 코덱이며 WebM은 알파 채널 동영상을 지원합니다. Alpha 데이터는 동영상 프레임의 사용하지 않는 영역에 별도의 마스크 이미지를 넣는 방식이 아니라 WebM의 Alpha 메커니즘을 사용해 저장됩니다.

이 도구가 생성하는 WebM VP9 Alpha는 현재 FFmpeg `libvpx-vp9`으로 인코딩됩니다. RVM 추론에서 GPU를 사용하더라도 VP9 Alpha 인코딩 단계는 CPU에서 처리됩니다. 따라서 WebM VP9 Alpha 변환은 그린 배경 MP4 변환보다 상당히 느릴 수 있습니다.

### 출력 형식을 지원하는 VR 플레이어

그린 배경 MP4의 경우, 크로마키 기능을 지원하는 VR 플레이어의 예는 다음과 같습니다.

- [PICO/Meta용 R800ZZbrowser](https://vr180g.com/browser/browser.php?l=kr)
- [PICO/Meta용 r800zzvrplayer](https://vr180g.com/pico/vrplayer.php?l=kr)

WebM VP9 Alpha의 경우, 제가 동작을 확인한 VR 플레이어는 다음과 같습니다.

- **[r800zzvrplayer 0.6 이상](https://vr180g.com/pico/vrplayer.php?l=kr)**

이 문서를 작성하는 시점에서는 WebM VP9 동영상의 알파 채널을 VR 투명도로 직접 사용하는 다른 VR 동영상 플레이어를 확인하지 못했습니다.

이는 다른 호환 플레이어가 존재하지 않는다고 단정하는 의미는 아닙니다. 다른 플레이어를 알고 있다면 알려 주세요.

## 요구 사항

- Windows 10 또는 Windows 11
- Python
- FFmpeg
- 초기 설정 및 첫 RVM 실행 시 인터넷 연결
- CPU 또는 지원되는 NVIDIA / AMD / Intel GPU

제공되는 NVIDIA, AMD, Intel 설정 스크립트와의 호환성을 최대한 확보하려면 **Python 3.10~3.12를 권장**합니다.

## 설치

### 1. Python 설치

Windows용 Python을 설치합니다.

Python 자체는 **R800ZZ RVM Tools가 자동으로 설치하지 않습니다**.

Python 설치 시 Python을 `PATH`에 추가하는 옵션을 활성화하는 것을 권장합니다.

명령 프롬프트에서 다음 명령으로 설치 여부를 확인할 수 있습니다.

```bat
python --version
```

### 2. FFmpeg 설치

FFmpeg는 이 저장소에 포함되어 있지 않습니다.

최소한 다음 항목을 포함하는 Windows용 FFmpeg 빌드를 다운로드합니다.

- `ffmpeg.exe`
- `ffprobe.exe`
- `libvpx-vp9`
- `libopus`
- `libx264`

GPU 가속 그린 배경 MP4 출력을 사용하려면 FFmpeg 빌드에 사용하는 GPU용 인코더도 포함되어 있어야 합니다.

- NVIDIA: `h264_nvenc`
- AMD: `h264_amf`
- Intel: `h264_qsv`

가장 간단한 설정 방법은 다음 파일을:

```text
ffmpeg.exe
ffprobe.exe
```

다음 파일과 같은 폴더에 두는 것입니다.

```text
r800zz_rvm_video.py
```

그리고 BAT 파일들도 같은 폴더에 둡니다.

이 구성에서는 FFmpeg를 위해 Windows `PATH` 환경 변수를 설정할 필요가 **없습니다**.

또는 FFmpeg를 다른 위치에 설치하고 해당 `bin` 디렉터리를 `PATH`에 추가할 수도 있습니다.

사용 가능한 하드웨어 인코더는 다음 명령으로 확인할 수 있습니다.

```bat
ffmpeg -encoders
```

### 3. 하드웨어에 맞는 PyTorch 설치

PyTorch는 이 저장소에 포함되어 있지 않습니다.

설정용 BAT 파일이 필요한 Python 패키지를 공식 배포처에서 다운로드합니다.

사용하는 하드웨어에 맞는 설정 방법을 선택하세요.

#### NVIDIA GPU

다음을 실행합니다.

```text
install_python_packages.bat
```

일반 NVIDIA/CPU BAT 파일에서 사용하는 CUDA 지원 PyTorch 환경을 설치하거나 업데이트합니다.

설치되는 패키지는 `python` 명령이 가리키는 Python 환경에 설치되며, 일반적으로 해당 Python 설치 폴더 아래의:

```text
Lib\site-packages
```

에 위치합니다.

NVIDIA GPU 경로는 R800ZZ가 실제로 테스트한 GPU 구성입니다.

#### AMD GPU

다음을 실행합니다.

```text
install_python_packages_AMD.bat
```

R800ZZ RVM Tools 폴더 안에 별도의 Python 가상 환경을 생성합니다.

```text
.venv_amd
```

그리고 그 안에 `torch-directml`을 설치합니다.

변환에는 파일명이 다음으로 끝나는 BAT 파일을 사용합니다.

```text
_AMD.bat
```

AMD GPU 지원은 DirectML을 사용합니다. R800ZZ는 실제 AMD GPU 하드웨어에서 테스트하지 않았습니다.

#### Intel GPU / Intel 내장 GPU

다음을 실행합니다.

```text
install_python_packages_Intel.bat
```

R800ZZ RVM Tools 폴더 안에 별도의 Python 가상 환경을 생성합니다.

```text
.venv_intel
```

그리고 그 안에 `torch-directml`을 설치합니다.

변환에는 파일명이 다음으로 끝나는 BAT 파일을 사용합니다.

```text
_Intel.bat
```

Intel GPU 지원은 DirectML을 사용하며, 사용 가능한 경우 그린 배경 MP4는 Intel Quick Sync Video(`h264_qsv`)를 사용합니다.

R800ZZ는 실제 Intel GPU 하드웨어에서 테스트하지 않았습니다.

#### CPU만 사용

GPU는 필요하지 않습니다.

CPU만 사용하는 환경에서는 CPU 버전 PyTorch를 설치합니다.

```bat
python -m pip install --upgrade pip
python -m pip install numpy
python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

표준 변환 BAT 파일은 CUDA를 사용할 수 없을 때 자동으로 CPU 처리를 사용합니다.

CPU 변환은 일반적으로 GPU 가속 RVM 추론보다 느립니다.

## PyTorch와 RVM은 어디에 다운로드됩니까?

### PyTorch

일반 NVIDIA/CPU 환경에서는 PyTorch가 `python` 명령이 사용하는 Python 환경에 설치됩니다.

예를 들어 일반적인 Python 설치에서는 패키지가 다음 위치에 저장될 수 있습니다.

```text
C:\Users\<username>\AppData\Local\Programs\Python\Python3xx\Lib\site-packages
```

정확한 위치는 Python 설치 방식에 따라 달라집니다.

AMD 및 Intel의 경우 제공된 설정 스크립트가 로컬 가상 환경을 사용합니다.

```text
R800ZZ_RVM_Tools\.venv_amd
R800ZZ_RVM_Tools\.venv_intel
```

### RVM

RVM은 PyTorch Torch Hub를 통해 로드됩니다.

첫 변환 시 Torch Hub가 RVM 저장소와 사전 학습된 MobileNetV3 모델을 자동으로 다운로드합니다.

Windows에서 Torch Hub의 기본 캐시 위치는 일반적으로 다음과 같습니다.

```text
C:\Users\<username>\.cache\torch\hub
```

RVM 저장소 캐시는 일반적으로 이 디렉터리 아래에 생성됩니다.

다운로드한 모델 가중치는 일반적으로 다음 위치에 저장됩니다.

```text
C:\Users\<username>\.cache\torch\hub\checkpoints
```

정확한 캐시 위치는 `TORCH_HOME` 등의 PyTorch 환경 설정으로 변경할 수 있습니다.

한 번 캐시된 파일은 이후 변환에서 다시 사용됩니다.

## 사용 방법

변환은 **Windows 탐색기에서 동영상 파일을 적절한 `.bat` 파일에 드래그 앤 드롭**하여 수행합니다.

예를 들어 다음 파일이 있다고 가정합니다.

```text
aaa.mp4
```

NVIDIA GPU 또는 CPU를 사용하여 그린 배경 MP4를 만들려면:

```text
aaa.mp4
```

파일을 다음 BAT 파일에 직접 드래그 앤 드롭합니다.

```text
R800ZZ_Make_Green_MP4.bat
```

BAT 파일이 드롭된 동영상 파일을 받아 자동으로 변환을 시작합니다.

마찬가지로 WebM VP9 Alpha 동영상을 만들려면:

```text
aaa.mp4
```

파일을 다음 BAT 파일에 드래그 앤 드롭합니다.

```text
R800ZZ_Make_WebM_Alpha.bat
```

명령 프롬프트를 열고 동영상 파일명을 직접 입력할 필요는 없습니다.

### 그린 배경 MP4 만들기

NVIDIA GPU 또는 CPU의 경우 동영상 파일을 다음 파일에 드래그 앤 드롭합니다.

```text
R800ZZ_Make_Green_MP4.bat
```

AMD GPU의 경우:

```text
R800ZZ_Make_Green_MP4_AMD.bat
```

Intel GPU의 경우:

```text
R800ZZ_Make_Green_MP4_Intel.bat
```

예:

```text
aaa.mp4
    ↓ 드래그 앤 드롭
R800ZZ_Make_Green_MP4.bat
```

출력:

```text
aaa_RVM_Green.mp4
```

### WebM VP9 Alpha 만들기

NVIDIA GPU 또는 CPU의 경우 동영상 파일을 다음 파일에 드래그 앤 드롭합니다.

```text
R800ZZ_Make_WebM_Alpha.bat
```

AMD GPU의 경우:

```text
R800ZZ_Make_WebM_Alpha_AMD.bat
```

Intel GPU의 경우:

```text
R800ZZ_Make_WebM_Alpha_Intel.bat
```

예:

```text
aaa.mp4
    ↓ 드래그 앤 드롭
R800ZZ_Make_WebM_Alpha.bat
```

출력:

```text
aaa_RVM_Alpha.webm
```

기본적으로 BAT 파일은 변환된 동영상을 R800ZZ RVM Tools 폴더에 저장합니다.

## 성능 관련 참고 사항

GPU 가속은 선택 사항입니다.

현재 처리 파이프라인은 여러 단계로 구성되어 있으며 모든 단계가 GPU로 가속되는 것은 아닙니다.

### NVIDIA

- RVM 추론: CUDA GPU
- 그린 배경 MP4 H.264 인코딩: NVENC
- WebM VP9 Alpha 인코딩: CPU (`libvpx-vp9`)
- FFmpeg 입력 동영상 디코딩: 현재 구현에서는 CPU

### AMD

- RVM 추론: DirectML
- 그린 배경 MP4 H.264 인코딩: AMF
- WebM VP9 Alpha 인코딩: CPU (`libvpx-vp9`)
- FFmpeg 입력 동영상 디코딩: 현재 구현에서는 CPU

### Intel

- RVM 추론: DirectML
- 그린 배경 MP4 H.264 인코딩: Quick Sync Video
- WebM VP9 Alpha 인코딩: CPU (`libvpx-vp9`)
- FFmpeg 입력 동영상 디코딩: 현재 구현에서는 CPU

WebM VP9 Alpha 인코딩은 CPU를 사용하므로 매우 빠른 GPU를 사용하더라도 Alpha 변환 전체가 같은 비율로 빨라지는 것은 아닙니다.

그린 배경 MP4는 RVM 추론과 H.264 인코딩 모두 GPU 하드웨어를 사용할 수 있으므로 GPU 가속의 효과를 더 크게 받을 수 있습니다.

## 매팅 품질에 대한 참고 사항

RVM은 특정 배경색을 검사해서 배경을 제거하는 방식이 아닙니다.

신경망을 사용해 사람 전경과 Alpha matte를 추정합니다.

따라서 입력 동영상의 배경이 녹색일 필요는 없습니다.

그린 배경 MP4 모드는 먼저 RVM으로 사람 매팅을 수행한 뒤, 추출된 전경을 새로 생성한 녹색 배경 위에 배치합니다.

WebM VP9 Alpha 모드는 RVM의 Alpha matte를 출력 동영상의 투명도 정보로 직접 사용합니다.

결과는 원본 동영상, 움직임, 머리카락 디테일, 가림, 조명, RVM의 정확도 등에 따라 달라질 수 있습니다.

## 하드웨어 테스트 상태

R800ZZ는 NVIDIA GPU 경로를 테스트했습니다.

AMD GPU 가속 및 Intel GPU 가속도 포함되어 있지만, R800ZZ가 실제 AMD 또는 Intel GPU 시스템에서 직접 테스트하지는 않았습니다.

CPU만 사용할 경우 별도의 외장 GPU는 필요하지 않습니다.

## 서드파티 소프트웨어

R800ZZ RVM Tools는 다음 프로젝트를 사용하거나 함께 동작합니다.

- Robust Video Matting
- PyTorch
- Torch-DirectML
- FFmpeg

RVM은 R800ZZ RVM Tools와 별도로 개발됩니다.

이 저장소에는 RVM 소스 코드나 사전 학습 모델 파일이 포함되어 있지 않습니다.

## 면책 조항

R800ZZ RVM Tools는 독립적인 유틸리티입니다.

출력 파일의 호환성은 재생에 사용하는 동영상 플레이어의 기능에 따라 달라집니다.

그린 배경 MP4에는 크로마키를 지원하는 플레이어가 필요합니다.

WebM VP9 Alpha에는 WebM의 알파 채널을 실제로 디코딩하고 사용하는 플레이어가 필요합니다. 일반 WebM VP9 동영상을 지원한다고 해서 VP9 Alpha 투명도까지 지원하는 것은 아닙니다.
