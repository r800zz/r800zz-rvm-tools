# R800ZZ RVM Tools

[English](README.md) | [Русский](README_ru.md) | [Español](README_es.md) | [ภาษาไทย](README_th.md) | [中文](README_zh.md) | [한국어](README_ko.md) | [日本語](README_ja.md)

R800ZZ RVM Tools convierte archivos de vídeo normales en vídeos adecuados para usar transparencia de fondo.

Utiliza **Robust Video Matting (RVM)** para extraer el primer plano de personas y **FFmpeg** para decodificar y codificar vídeo.

Se admiten dos modos de salida:

- **MP4 con fondo verde** — crea un MP4 H.264 con la persona extraída compuesta sobre un fondo verde puro.
- **WebM VP9 Alpha** — crea un vídeo WebM VP9 con un canal alfa real.

No es obligatoria una GPU de alto rendimiento. La herramienta puede funcionar solo con CPU, aunque la aceleración por GPU puede hacer que el procesamiento con RVM sea mucho más rápido.

## Guía rápida de uso

- Requisitos previos: instale Python y FFmpeg.

- La primera vez, ejecute `install_python_packages_NVIDIA.bat`.

- Para convertir un vídeo a fondo verde, arrastre y suelte el archivo de vídeo sobre `R800ZZ_Make_Green_MP4_NVIDIA.bat`.

- Para convertir un vídeo a transparencia Alpha (WebM VP9), arrastre y suelte el archivo de vídeo sobre `R800ZZ_Make_WebM_Alpha_NVIDIA.bat`.

## ¿Qué es RVM?

RVM significa **Robust Video Matting**.

RVM es un modelo de matting de vídeo para personas basado en redes neuronales, diseñado para separar a las personas del fondo conservando la información temporal entre los fotogramas del vídeo.

Esta herramienta utiliza el proyecto RVM original mediante PyTorch Torch Hub.

El código fuente de RVM y el modelo preentrenado **no están incluidos en este repositorio**. Se descargan desde el proyecto original cuando son necesarios.

## Modos de salida

### MP4 con fondo verde

La persona extraída por RVM se compone sobre un fondo verde puro y se codifica como MP4 H.264.

Ejemplo de salida:

```text
aaa_RVM_Green.mp4
```

Este modo está pensado para reproductores de vídeo VR compatibles con transparencia por chroma key.

Ejemplos:

- [R800ZZbrowser para PICO/Meta](https://vr180g.com/browser/browser.php?l=es)
- [r800zzvrplayer para PICO 4 Ultra/PICO4](https://vr180g.com/pico/vrplayer.php?l=es)

La conversión a fondo verde suele ser mucho más rápida que la conversión a WebM VP9 Alpha.

Cuando es compatible, la herramienta utiliza codificación H.264 por hardware:

| Hardware | Inferencia RVM | Codificador H.264 |
| --- | --- | --- |
| GPU NVIDIA | PyTorch CUDA | `h264_nvenc` |
| GPU AMD | PyTorch DirectML | `h264_amf` |
| GPU Intel / GPU Intel integrada | PyTorch DirectML | `h264_qsv` |
| Solo CPU | PyTorch CPU | `libx264` |

### WebM VP9 Alpha

Este modo crea un vídeo WebM que utiliza VP9 con un canal alfa real.

Ejemplo de salida:

```text
aaa_RVM_Alpha.webm
```

Este **no es un formato de vídeo alfa específico de R800ZZ**.

VP9 es un códec de vídeo abierto del WebM Project, y WebM admite vídeo con canal alfa. Los datos alfa se almacenan mediante el mecanismo alfa de WebM, en lugar de colocar una imagen de máscara personalizada en una zona no utilizada del fotograma.

Actualmente, la salida WebM VP9 Alpha creada por esta herramienta se codifica con FFmpeg `libvpx-vp9`. La etapa de codificación VP9 Alpha se realiza en la CPU, incluso cuando la inferencia RVM utiliza la GPU. Por este motivo, la conversión a WebM VP9 Alpha puede ser considerablemente más lenta que la conversión a MP4 con fondo verde.

### Reproductores VR compatibles con la salida

Para MP4 con fondo verde, algunos ejemplos de reproductores VR con función de chroma key son:

- [R800ZZbrowser para PICO/Meta](https://vr180g.com/browser/browser.php?l=es)
- [r800zzvrplayer para PICO 4 Ultra/PICO4](https://vr180g.com/pico/vrplayer.php?l=es)

Para WebM VP9 Alpha, el reproductor VR que he confirmado es:

- **[r800zzvrplayer 4.0 o posterior](https://vr180g.com/pico/vrplayer.php?l=es)**

En el momento de escribir esto, no he podido confirmar ningún otro reproductor de vídeo VR que reproduzca directamente vídeo WebM VP9 utilizando su canal alfa como transparencia VR.

Esto no pretende afirmar que no exista ningún otro reproductor compatible. Si conoce alguno, por favor comuníquemelo.

## Requisitos

- Windows 10 o Windows 11
- Python
- FFmpeg
- Conexión a Internet durante la configuración inicial y la primera ejecución de RVM
- CPU, o una GPU NVIDIA / AMD / Intel compatible

Para obtener la mayor compatibilidad con los scripts de configuración incluidos para NVIDIA, AMD e Intel, se recomienda **Python 3.10 a 3.12**.

## Instalación

### 1. Instalar Python

Instale Python para Windows.

Python **no se instala automáticamente mediante R800ZZ RVM Tools**.

Durante la instalación de Python se recomienda activar la opción para añadir Python a `PATH`.

Puede comprobar la instalación desde el Símbolo del sistema:

```bat
python --version
```

### 2. Instalar FFmpeg

FFmpeg no está incluido en este repositorio.

Descargue una compilación de FFmpeg para Windows que incluya al menos:

- `ffmpeg.exe`
- `ffprobe.exe`
- `libvpx-vp9`
- `libopus`
- `libx264`

Para generar MP4 con fondo verde acelerados por GPU, la compilación de FFmpeg también debe incluir el codificador correspondiente a su GPU:

- NVIDIA: `h264_nvenc`
- AMD: `h264_amf`
- Intel: `h264_qsv`

La configuración más sencilla es colocar:

```text
ffmpeg.exe
ffprobe.exe
```

en la misma carpeta que:

```text
r800zz_rvm_video.py
```

y los archivos BAT.

Con esta configuración, **no es necesario** configurar la variable de entorno `PATH` de Windows para FFmpeg.

Como alternativa, puede instalar FFmpeg en otra ubicación si añade su directorio `bin` a `PATH`.

Puede comprobar los codificadores por hardware disponibles con:

```bat
ffmpeg -encoders
```

### 3. Instalar PyTorch para su hardware

PyTorch no se incluye con este repositorio.

Los archivos BAT de configuración descargan los paquetes de Python necesarios desde sus fuentes oficiales.

Elija el método de configuración correspondiente a su hardware.

#### GPU NVIDIA

Ejecute:

```text
install_python_packages.bat
```

Esto instala o actualiza el entorno PyTorch con CUDA utilizado por los archivos BAT normales para NVIDIA/CPU.

Los paquetes instalados se colocan en el entorno de Python seleccionado por el comando `python`, normalmente bajo:

```text
Lib\site-packages
```

dentro de esa instalación de Python.

La ruta de GPU NVIDIA es la configuración de GPU probada por R800ZZ.

#### GPU AMD

Ejecute:

```text
install_python_packages_AMD.bat
```

Esto crea un entorno virtual de Python aislado:

```text
.venv_amd
```

dentro de la carpeta R800ZZ RVM Tools e instala allí `torch-directml`.

Para la conversión, utilice los archivos BAT cuyo nombre termina en:

```text
_AMD.bat
```

La compatibilidad con GPU AMD se proporciona mediante DirectML. R800ZZ no la ha probado en hardware AMD físico.

#### GPU Intel / GPU Intel integrada

Ejecute:

```text
install_python_packages_Intel.bat
```

Esto crea un entorno virtual de Python aislado:

```text
.venv_intel
```

dentro de la carpeta R800ZZ RVM Tools e instala allí `torch-directml`.

Para la conversión, utilice los archivos BAT cuyo nombre termina en:

```text
_Intel.bat
```

La compatibilidad con GPU Intel se proporciona mediante DirectML, y el MP4 con fondo verde utiliza Intel Quick Sync Video (`h264_qsv`) cuando está disponible.

R800ZZ no lo ha probado en hardware Intel físico.

#### Solo CPU

No se necesita una GPU.

Para un entorno de solo CPU, instale la versión de CPU de PyTorch:

```bat
python -m pip install --upgrade pip
python -m pip install numpy
python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

Los archivos BAT de conversión estándar utilizan automáticamente procesamiento por CPU cuando CUDA no está disponible.

La conversión por CPU normalmente será más lenta que la inferencia RVM acelerada por GPU.

## ¿Dónde se descargan PyTorch y RVM?

### PyTorch

Para el entorno normal NVIDIA/CPU, PyTorch se instala en el entorno de Python utilizado por el comando `python`.

Por ejemplo, una instalación normal de Python puede guardar los paquetes en:

```text
C:\Users\<username>\AppData\Local\Programs\Python\Python3xx\Lib\site-packages
```

La ubicación exacta depende de cómo se haya instalado Python.

Para AMD e Intel, los scripts de configuración incluidos utilizan entornos virtuales locales:

```text
R800ZZ_RVM_Tools\.venv_amd
R800ZZ_RVM_Tools\.venv_intel
```

### RVM

RVM se carga mediante PyTorch Torch Hub.

En la primera conversión, Torch Hub descarga automáticamente el repositorio de RVM y el modelo MobileNetV3 preentrenado.

La caché predeterminada de Torch Hub en Windows normalmente se encuentra en:

```text
C:\Users\<username>\.cache\torch\hub
```

La caché del repositorio de RVM aparecerá normalmente debajo de ese directorio.

Los pesos descargados del modelo normalmente se guardan en:

```text
C:\Users\<username>\.cache\torch\hub\checkpoints
```

La ubicación exacta de la caché puede cambiarse mediante ajustes de entorno de PyTorch como `TORCH_HOME`.

Una vez almacenados en caché, los archivos se reutilizan en conversiones posteriores.

## Cómo usarlo

La conversión se realiza **arrastrando y soltando un archivo de vídeo sobre el archivo `.bat` correspondiente en el Explorador de Windows**.

Por ejemplo, si tiene:

```text
aaa.mp4
```

y desea crear un MP4 con fondo verde utilizando una GPU NVIDIA o la CPU, arrastre:

```text
aaa.mp4
```

y suéltelo directamente sobre:

```text
R800ZZ_Make_Green_MP4.bat
```

El archivo BAT recibe el vídeo soltado e inicia automáticamente la conversión.

De forma similar, para crear un vídeo WebM VP9 Alpha, arrastre:

```text
aaa.mp4
```

y suéltelo sobre:

```text
R800ZZ_Make_WebM_Alpha.bat
```

No es necesario abrir un Símbolo del sistema ni escribir manualmente el nombre del archivo de vídeo.

### Crear MP4 con fondo verde

Para GPU NVIDIA o CPU, arrastre y suelte el archivo de vídeo sobre:

```text
R800ZZ_Make_Green_MP4.bat
```

Para GPU AMD:

```text
R800ZZ_Make_Green_MP4_AMD.bat
```

Para GPU Intel:

```text
R800ZZ_Make_Green_MP4_Intel.bat
```

Ejemplo:

```text
aaa.mp4
    ↓ arrastrar y soltar
R800ZZ_Make_Green_MP4.bat
```

Salida:

```text
aaa_RVM_Green.mp4
```

### Crear WebM VP9 Alpha

Para GPU NVIDIA o CPU, arrastre y suelte el archivo de vídeo sobre:

```text
R800ZZ_Make_WebM_Alpha.bat
```

Para GPU AMD:

```text
R800ZZ_Make_WebM_Alpha_AMD.bat
```

Para GPU Intel:

```text
R800ZZ_Make_WebM_Alpha_Intel.bat
```

Ejemplo:

```text
aaa.mp4
    ↓ arrastrar y soltar
R800ZZ_Make_WebM_Alpha.bat
```

Salida:

```text
aaa_RVM_Alpha.webm
```

De forma predeterminada, los archivos BAT guardan el vídeo convertido en la carpeta R800ZZ RVM Tools.

## Notas sobre el rendimiento

La aceleración por GPU es opcional.

La canalización de procesamiento actual contiene varias etapas distintas y no todas están aceleradas por GPU.

### NVIDIA

- Inferencia RVM: GPU CUDA
- Codificación H.264 del MP4 con fondo verde: NVENC
- Codificación WebM VP9 Alpha: CPU (`libvpx-vp9`)
- Decodificación del vídeo de entrada con FFmpeg: CPU en la implementación actual

### AMD

- Inferencia RVM: DirectML
- Codificación H.264 del MP4 con fondo verde: AMF
- Codificación WebM VP9 Alpha: CPU (`libvpx-vp9`)
- Decodificación del vídeo de entrada con FFmpeg: CPU en la implementación actual

### Intel

- Inferencia RVM: DirectML
- Codificación H.264 del MP4 con fondo verde: Quick Sync Video
- Codificación WebM VP9 Alpha: CPU (`libvpx-vp9`)
- Decodificación del vídeo de entrada con FFmpeg: CPU en la implementación actual

Como la codificación WebM VP9 Alpha utiliza la CPU, una GPU muy rápida no hace que todo el proceso de conversión Alpha sea igualmente rápido.

La conversión a MP4 con fondo verde puede beneficiarse mucho más de la aceleración por GPU, ya que tanto la inferencia RVM como la codificación H.264 pueden utilizar hardware de GPU.

## Notas sobre la calidad del matting

RVM no elimina el fondo comprobando un color de fondo concreto.

Estima el primer plano humano y la máscara alfa mediante una red neuronal.

Por lo tanto, el vídeo de entrada no necesita tener un fondo verde.

El modo MP4 con fondo verde primero realiza el matting de la persona con RVM y después coloca el primer plano extraído sobre un fondo verde recién generado.

El modo WebM VP9 Alpha utiliza directamente la máscara alfa de RVM como información de transparencia del vídeo de salida.

Los resultados pueden variar según el vídeo de origen, el movimiento, el detalle del cabello, las oclusiones, la iluminación y la precisión de RVM.

## Estado de las pruebas de hardware

R800ZZ ha probado la ruta de GPU NVIDIA.

Se incluyen aceleración para GPU AMD y GPU Intel, pero R800ZZ no ha probado personalmente esas rutas en sistemas físicos con GPU AMD o Intel.

El funcionamiento solo con CPU no requiere una GPU dedicada.

## Software de terceros

R800ZZ RVM Tools utiliza o funciona junto con los siguientes proyectos:

- Robust Video Matting
- PyTorch
- Torch-DirectML
- FFmpeg

RVM se desarrolla por separado de R800ZZ RVM Tools.

Este repositorio no incluye el código fuente de RVM ni los archivos del modelo preentrenado.

## Descargo de responsabilidad

R800ZZ RVM Tools es una utilidad independiente.

La compatibilidad de la salida depende de las capacidades del reproductor de vídeo utilizado para la reproducción.

El MP4 con fondo verde requiere un reproductor compatible con chroma key.

WebM VP9 Alpha requiere un reproductor que realmente decodifique y utilice el canal alfa de WebM. Que un reproductor admita vídeo WebM VP9 normal no significa necesariamente que admita transparencia VP9 Alpha.
