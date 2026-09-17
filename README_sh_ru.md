[English](README_sh_en.md) | [Русский](README_sh_ru.md) | [Español](README_sh_es.md) | [ภาษาไทย](README_sh_th.md) | [中文](README_sh_zh.md) | [한국어](README_sh_ko.md) | [日本語](README_sh_ja.md)

## UNIX-подобные операционные системы (Linux, WSL, macOS)

R800ZZ RVM Tools также можно использовать в Linux и macOS.

Работа в Linux была протестирована R800ZZ с использованием **Ubuntu в WSL2 на Windows 11**.

В протестированной среде WSL2 **NVIDIA GPU** успешно использовался для инференса RVM через CUDA, и были успешно созданы как Green-screen MP4, так и WebM VP9 Alpha видео.

macOS в этом тесте не использовалась.

## Краткое руководство

Сначала установите Python, FFmpeg и необходимые пакеты Python.

Для создания Green-screen MP4:

```bash
bash green.sh "input.mp4"
```

Пример:

```bash
bash green.sh "aaa.mp4"
```

Выходной файл:

```text
aaa_RVM_Green.mp4
```

Для создания WebM VP9 Alpha видео:

```bash
bash alphavp9.sh "input.mp4"
```

Пример:

```bash
bash alphavp9.sh "aaa.mp4"
```

Выходной файл:

```text
aaa_RVM_Alpha.webm
```

Для видеофайла также можно указать абсолютный путь.

Например:

```bash
bash green.sh "/home/user/Videos/aaa.mp4"
```

В WSL2 видео, сохранённое на диске Windows C:, можно указать через путь WSL, например:

```bash
bash green.sh "/mnt/c/Videos/aaa.mp4"
```

## Требования Linux

Установите Python, FFmpeg, Git и поддержку виртуальных окружений Python.

В Ubuntu / WSL2:

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv ffmpeg git
```

Проверьте установку:

```bash
python3 --version
ffmpeg -version
```

## Среда Python

Создайте виртуальное окружение Python:

```bash
python3 -m venv .venv_linux
source .venv_linux/bin/activate
```

Обновите pip:

```bash
python -m pip install --upgrade pip
```

## NVIDIA GPU в Linux / WSL2

При использовании NVIDIA GPU с поддержкой CUDA установите версию PyTorch с поддержкой CUDA.

Конкретный пакет PyTorch CUDA должен соответствовать текущей поддерживаемой среде PyTorch.

После установки можно проверить, может ли PyTorch использовать NVIDIA GPU:

```bash
python -c "import torch; print(torch.__version__); print(torch.version.cuda); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
```

Если для доступности CUDA отображается:

```text
True
```

RVM может использовать NVIDIA GPU.

## FFmpeg

В Linux используется системный FFmpeg, установленный через менеджер пакетов.

Следующие команды должны быть доступны из терминала:

```bash
ffmpeg
ffprobe
```

В отличие от версии для Windows, файлы `ffmpeg.exe` и `ffprobe.exe` не нужно помещать в каталог R800ZZ RVM Tools.

## Поддержка NVIDIA GPU в WSL2

При использовании WSL2 доступ к NVIDIA GPU уже должен работать внутри WSL.

Это можно проверить командой:

```bash
nvidia-smi
```

Если NVIDIA GPU отображается, PyTorch с поддержкой CUDA сможет использовать GPU после установки подходящего пакета PyTorch.

## Green-screen MP4

Для преобразования обычного видео в Green-screen MP4:

```bash
bash green.sh "input.mp4"
```

RVM извлекает передний план с человеком и совмещает его с чистым зелёным фоном.

Пример:

```text
Input:
aaa.mp4

Output:
aaa_RVM_Green.mp4
```

Если доступно ускорение NVIDIA GPU, инференс RVM может использовать CUDA.

Преобразование Green-screen MP4 также может использовать аппаратное H.264-кодирование NVIDIA, если оно поддерживается установленной сборкой FFmpeg.

## WebM VP9 Alpha

Для создания WebM VP9 видео с настоящим альфа-каналом:

```bash
bash alphavp9.sh "input.mp4"
```

Пример:

```text
Input:
aaa.mp4

Output:
aaa_RVM_Alpha.webm
```

RVM создаёт альфа-маску человека, которая сохраняется как информация о прозрачности в выходном WebM VP9.

При доступности CUDA инференс RVM может использовать NVIDIA GPU.

Этап кодирования WebM VP9 Alpha использует FFmpeg `libvpx-vp9` и выполняется на CPU, поэтому это преобразование обычно медленнее, чем преобразование Green-screen MP4.

## macOS

Версия shell-скриптов для Linux/macOS также предназначена для поддержки macOS.

Однако текущая версия Linux/macOS была протестирована R800ZZ на **Ubuntu в WSL2**, а не на физическом оборудовании macOS.

Поэтому работа GPU-ускорения в macOS не была проверена R800ZZ.

Для работы на CPU NVIDIA GPU не требуется.
