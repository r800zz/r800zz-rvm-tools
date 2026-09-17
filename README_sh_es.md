[English](README_sh_en.md) | [Русский](README_sh_ru.md) | [Español](README_sh_es.md) | [ภาษาไทย](README_sh_th.md) | [中文](README_sh_zh.md) | [한국어](README_sh_ko.md) | [日本語](README_sh_ja.md)

## Sistemas operativos tipo UNIX (Linux, WSL, macOS)

R800ZZ RVM Tools también puede utilizarse en Linux y macOS.

El funcionamiento en Linux ha sido probado por R800ZZ usando **Ubuntu bajo WSL2 en Windows 11**.

En el entorno WSL2 probado se utilizó correctamente una **GPU NVIDIA** para la inferencia de RVM mediante CUDA y se generaron correctamente vídeos Green-screen MP4 y WebM VP9 Alpha.

macOS no se utilizó para esta prueba.

## Guía rápida de uso

Instale primero Python, FFmpeg y los paquetes de Python necesarios.

Para crear un Green-screen MP4:

```bash
bash green.sh "input.mp4"
```

Ejemplo:

```bash
bash green.sh "aaa.mp4"
```

Salida:

```text
aaa_RVM_Green.mp4
```

Para crear un vídeo WebM VP9 Alpha:

```bash
bash alphavp9.sh "input.mp4"
```

Ejemplo:

```bash
bash alphavp9.sh "aaa.mp4"
```

Salida:

```text
aaa_RVM_Alpha.webm
```

La ruta del archivo de vídeo también puede ser una ruta absoluta.

Por ejemplo:

```bash
bash green.sh "/home/user/Videos/aaa.mp4"
```

En WSL2, un vídeo almacenado en la unidad C: de Windows puede especificarse mediante una ruta de WSL como:

```bash
bash green.sh "/mnt/c/Videos/aaa.mp4"
```

## Requisitos de Linux

Instale Python, FFmpeg, Git y el soporte para entornos virtuales de Python.

En Ubuntu / WSL2:

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv ffmpeg git
```

Compruebe las instalaciones:

```bash
python3 --version
ffmpeg -version
```

## Entorno de Python

Cree un entorno virtual de Python:

```bash
python3 -m venv .venv_linux
source .venv_linux/bin/activate
```

Actualice pip:

```bash
python -m pip install --upgrade pip
```

## GPU NVIDIA en Linux / WSL2

Cuando utilice una GPU NVIDIA compatible con CUDA, instale la versión de PyTorch compatible con CUDA.

El paquete CUDA exacto de PyTorch debe coincidir con el entorno de PyTorch compatible actualmente.

Después de la instalación, puede comprobar si PyTorch puede utilizar la GPU NVIDIA con:

```bash
python -c "import torch; print(torch.__version__); print(torch.version.cuda); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
```

Si se muestra:

```text
True
```

para la disponibilidad de CUDA, RVM puede utilizar la GPU NVIDIA.

## FFmpeg

En Linux se utiliza el FFmpeg del sistema instalado mediante el gestor de paquetes.

Los siguientes comandos deben estar disponibles desde la terminal:

```bash
ffmpeg
ffprobe
```

A diferencia de la versión para Windows, no es necesario colocar `ffmpeg.exe` ni `ffprobe.exe` en el directorio de R800ZZ RVM Tools.

## Compatibilidad con GPU NVIDIA en WSL2

Al utilizar WSL2, el acceso a la GPU NVIDIA debe estar disponible previamente dentro de WSL.

Puede comprobarlo con:

```bash
nvidia-smi
```

Si se muestra la GPU NVIDIA, PyTorch con soporte CUDA podrá utilizarla después de instalar el paquete de PyTorch adecuado.

## Green-screen MP4

Para convertir un vídeo normal en un Green-screen MP4:

```bash
bash green.sh "input.mp4"
```

RVM extrae el primer plano de la persona y lo compone sobre un fondo verde puro.

Ejemplo:

```text
Input:
aaa.mp4

Output:
aaa_RVM_Green.mp4
```

Cuando la aceleración por GPU NVIDIA está disponible, la inferencia de RVM puede utilizar CUDA.

La conversión a Green-screen MP4 también puede utilizar codificación H.264 por hardware de NVIDIA cuando la compilación instalada de FFmpeg lo admite.

## WebM VP9 Alpha

Para crear un vídeo WebM VP9 con un canal alfa real:

```bash
bash alphavp9.sh "input.mp4"
```

Ejemplo:

```text
Input:
aaa.mp4

Output:
aaa_RVM_Alpha.webm
```

RVM genera la máscara alfa de la persona, que se almacena como información de transparencia en la salida WebM VP9.

La inferencia de RVM puede utilizar la GPU NVIDIA cuando CUDA está disponible.

La etapa de codificación WebM VP9 Alpha utiliza FFmpeg `libvpx-vp9` y se ejecuta en la CPU, por lo que esta conversión suele ser más lenta que la conversión a Green-screen MP4.

## macOS

La versión de scripts de shell para Linux/macOS también está destinada a ser compatible con macOS.

Sin embargo, la versión actual para Linux/macOS ha sido probada por R800ZZ en **Ubuntu bajo WSL2**, no en hardware físico con macOS.

Por lo tanto, R800ZZ no ha verificado el comportamiento de la aceleración por GPU en macOS.

El funcionamiento mediante CPU no requiere una GPU NVIDIA.
