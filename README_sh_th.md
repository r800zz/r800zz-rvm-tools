[English](README_sh_en.md) | [Русский](README_sh_ru.md) | [Español](README_sh_es.md) | [ภาษาไทย](README_sh_th.md) | [中文](README_sh_zh.md) | [한국어](README_sh_ko.md) | [日本語](README_sh_ja.md)

## ระบบปฏิบัติการแบบ UNIX (Linux, WSL, macOS)

R800ZZ RVM Tools สามารถใช้งานบน Linux และ macOS ได้เช่นกัน

R800ZZ ได้ทดสอบการทำงานบน Linux โดยใช้ **Ubuntu ภายใต้ WSL2 บน Windows 11**

ในสภาพแวดล้อม WSL2 ที่ทดสอบ สามารถใช้ **NVIDIA GPU** สำหรับการอนุมานของ RVM ผ่าน CUDA ได้สำเร็จ และสามารถสร้างวิดีโอทั้ง Green-screen MP4 และ WebM VP9 Alpha ได้สำเร็จ

ไม่ได้ใช้ macOS ในการทดสอบนี้

## คู่มือการใช้งานแบบรวดเร็ว

ติดตั้ง Python, FFmpeg และแพ็กเกจ Python ที่จำเป็นก่อน

ในการสร้าง Green-screen MP4:

```bash
bash green.sh "input.mp4"
```

ตัวอย่าง:

```bash
bash green.sh "aaa.mp4"
```

ไฟล์ผลลัพธ์:

```text
aaa_RVM_Green.mp4
```

ในการสร้างวิดีโอ WebM VP9 Alpha:

```bash
bash alphavp9.sh "input.mp4"
```

ตัวอย่าง:

```bash
bash alphavp9.sh "aaa.mp4"
```

ไฟล์ผลลัพธ์:

```text
aaa_RVM_Alpha.webm
```

สามารถระบุพาธของไฟล์วิดีโอเป็นพาธแบบสัมบูรณ์ได้เช่นกัน

ตัวอย่าง:

```bash
bash green.sh "/home/user/Videos/aaa.mp4"
```

ภายใต้ WSL2 วิดีโอที่เก็บอยู่ในไดรฟ์ C: ของ Windows สามารถระบุด้วยพาธของ WSL เช่น:

```bash
bash green.sh "/mnt/c/Videos/aaa.mp4"
```

## ข้อกำหนดสำหรับ Linux

ติดตั้ง Python, FFmpeg, Git และการรองรับ virtual environment ของ Python

บน Ubuntu / WSL2:

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv ffmpeg git
```

ตรวจสอบการติดตั้ง:

```bash
python3 --version
ffmpeg -version
```

## สภาพแวดล้อม Python

สร้าง virtual environment ของ Python:

```bash
python3 -m venv .venv_linux
source .venv_linux/bin/activate
```

อัปเกรด pip:

```bash
python -m pip install --upgrade pip
```

## NVIDIA GPU บน Linux / WSL2

เมื่อใช้ NVIDIA GPU ที่รองรับ CUDA ให้ติดตั้ง PyTorch รุ่นที่รองรับ CUDA

แพ็กเกจ PyTorch CUDA ที่ใช้ควรตรงกับสภาพแวดล้อม PyTorch ที่รองรับในปัจจุบัน

หลังจากติดตั้งแล้ว สามารถตรวจสอบว่า PyTorch ใช้ NVIDIA GPU ได้หรือไม่ด้วย:

```bash
python -c "import torch; print(torch.__version__); print(torch.version.cuda); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
```

หากการตรวจสอบความพร้อมใช้งานของ CUDA แสดง:

```text
True
```

RVM สามารถใช้ NVIDIA GPU ได้

## FFmpeg

บน Linux จะใช้ FFmpeg ของระบบที่ติดตั้งผ่าน package manager

คำสั่งต่อไปนี้ต้องสามารถเรียกใช้ได้จากเทอร์มินัล:

```bash
ffmpeg
ffprobe
```

ต่างจากเวอร์ชัน Windows ตรงที่ไม่จำเป็นต้องวาง `ffmpeg.exe` หรือ `ffprobe.exe` ไว้ในไดเรกทอรี R800ZZ RVM Tools

## การรองรับ NVIDIA GPU บน WSL2

เมื่อใช้ WSL2 ต้องสามารถเข้าถึง NVIDIA GPU จากภายใน WSL ได้อยู่แล้ว

สามารถตรวจสอบได้ด้วย:

```bash
nvidia-smi
```

หากแสดง NVIDIA GPU อยู่ PyTorch ที่รองรับ CUDA จะสามารถใช้ GPU ได้หลังจากติดตั้งแพ็กเกจ PyTorch ที่เหมาะสม

## Green-screen MP4

ในการแปลงวิดีโอทั่วไปเป็น Green-screen MP4:

```bash
bash green.sh "input.mp4"
```

RVM จะแยกส่วนหน้าที่เป็นบุคคลออกมาและนำไปประกอบบนพื้นหลังสีเขียวล้วน

ตัวอย่าง:

```text
Input:
aaa.mp4

Output:
aaa_RVM_Green.mp4
```

เมื่อสามารถใช้การเร่งด้วย NVIDIA GPU ได้ การอนุมานของ RVM สามารถใช้ CUDA ได้

การแปลง Green-screen MP4 สามารถใช้การเข้ารหัส H.264 ด้วยฮาร์ดแวร์ NVIDIA ได้เช่นกัน หาก FFmpeg ที่ติดตั้งรองรับ

## WebM VP9 Alpha

ในการสร้างวิดีโอ WebM VP9 ที่มี alpha channel จริง:

```bash
bash alphavp9.sh "input.mp4"
```

ตัวอย่าง:

```text
Input:
aaa.mp4

Output:
aaa_RVM_Alpha.webm
```

RVM จะสร้าง alpha matte ของบุคคล ซึ่งจะถูกเก็บเป็นข้อมูลความโปร่งใสในไฟล์ WebM VP9 ที่ส่งออก

การอนุมานของ RVM สามารถใช้ NVIDIA GPU ได้เมื่อ CUDA พร้อมใช้งาน

ขั้นตอนการเข้ารหัส WebM VP9 Alpha ใช้ FFmpeg `libvpx-vp9` และทำงานด้วย CPU ดังนั้นโดยปกติการแปลงนี้จะช้ากว่าการแปลง Green-screen MP4

## macOS

เวอร์ชัน shell script สำหรับ Linux/macOS มีจุดประสงค์ให้รองรับ macOS ด้วย

อย่างไรก็ตาม เวอร์ชัน Linux/macOS ปัจจุบันได้รับการทดสอบโดย R800ZZ บน **Ubuntu ภายใต้ WSL2** ไม่ใช่บนฮาร์ดแวร์ macOS จริง

ดังนั้น R800ZZ จึงยังไม่ได้ตรวจสอบพฤติกรรมของการเร่งด้วย GPU บน macOS

การทำงานด้วย CPU ไม่จำเป็นต้องมี NVIDIA GPU
