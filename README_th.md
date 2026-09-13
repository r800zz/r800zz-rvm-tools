# R800ZZ RVM Tools

[English](README.md) | [Русский](README_ru.md) | [Español](README_es.md) | [ภาษาไทย](README_th.md) | [中文](README_zh.md) | [한국어](README_ko.md) | [日本語](README_ja.md)

R800ZZ RVM Tools ใช้แปลงไฟล์วิดีโอทั่วไปให้เป็นวิดีโอที่เหมาะสำหรับการทำพื้นหลังโปร่งใส

เครื่องมือนี้ใช้ **Robust Video Matting (RVM)** สำหรับแยกบุคคลออกจากพื้นหลัง และใช้ **FFmpeg** สำหรับถอดรหัสและเข้ารหัสวิดีโอ

รองรับรูปแบบเอาต์พุต 2 แบบ:

- **MP4 พื้นหลังสีเขียว** — สร้างไฟล์ H.264 MP4 โดยนำบุคคลที่แยกออกมาไปวางบนพื้นหลังสีเขียวล้วน
- **WebM VP9 Alpha** — สร้างวิดีโอ WebM VP9 ที่มีช่องอัลฟาจริง

ไม่จำเป็นต้องมี GPU ประสิทธิภาพสูง เครื่องมือนี้สามารถทำงานด้วย CPU เพียงอย่างเดียวได้ แต่การใช้ GPU จะช่วยให้การประมวลผล RVM เร็วขึ้นมาก

## คู่มือใช้งานแบบย่อ

- สิ่งที่ต้องมี: ติดตั้ง Python และ FFmpeg

- ในการใช้งานครั้งแรก ให้รัน `install_python_packages_NVIDIA.bat`

- หากต้องการแปลงวิดีโอเป็นพื้นหลังสีเขียว ให้ลากไฟล์วิดีโอไปวางบน `R800ZZ_Make_Green_MP4_NVIDIA.bat`

- หากต้องการแปลงเป็นความโปร่งใส Alpha (WebM VP9) ให้ลากไฟล์วิดีโอไปวางบน `R800ZZ_Make_WebM_Alpha_NVIDIA.bat`

## RVM คืออะไร?

RVM ย่อมาจาก **Robust Video Matting**

RVM เป็นโมเดล neural network สำหรับ video matting ของบุคคล ซึ่งออกแบบมาเพื่อแยกบุคคลออกจากพื้นหลังพร้อมรักษาข้อมูลเชิงเวลาระหว่างเฟรมวิดีโอ

เครื่องมือนี้ใช้โปรเจกต์ RVM ต้นฉบับผ่าน PyTorch Torch Hub

ซอร์สโค้ด RVM และโมเดลที่ฝึกไว้ล่วงหน้า **ไม่ได้รวมอยู่ใน repository นี้** โดยจะดาวน์โหลดจากโปรเจกต์ต้นฉบับเมื่อจำเป็น

## รูปแบบเอาต์พุต

### MP4 พื้นหลังสีเขียว

บุคคลที่แยกออกมาด้วย RVM จะถูกนำไปวางบนพื้นหลังสีเขียวล้วน และเข้ารหัสเป็น H.264 MP4

ตัวอย่างไฟล์ผลลัพธ์:

```text
aaa_RVM_Green.mp4
```

โหมดนี้เหมาะสำหรับโปรแกรมเล่นวิดีโอ VR ที่รองรับความโปร่งใสแบบ chroma key

ตัวอย่าง:

- [R800ZZbrowser สำหรับ PICO/Meta](https://vr180g.com/browser/browser.php?l=th)
- [r800zzvrplayer สำหรับ PICO 4 Ultra/PICO4](https://vr180g.com/pico/vrplayer.php?l=th)

โดยทั่วไป การแปลงเป็นพื้นหลังสีเขียวจะเร็วกว่าการแปลงเป็น WebM VP9 Alpha มาก

หากฮาร์ดแวร์รองรับ เครื่องมือจะใช้การเข้ารหัส H.264 ด้วยฮาร์ดแวร์:

| ฮาร์ดแวร์ | การประมวลผล RVM | ตัวเข้ารหัส H.264 |
| --- | --- | --- |
| NVIDIA GPU | PyTorch CUDA | `h264_nvenc` |
| AMD GPU | PyTorch DirectML | `h264_amf` |
| Intel GPU / Intel integrated GPU | PyTorch DirectML | `h264_qsv` |
| CPU เท่านั้น | PyTorch CPU | `libx264` |

### WebM VP9 Alpha

โหมดนี้สร้างวิดีโอ WebM ที่ใช้ VP9 พร้อมช่องอัลฟาจริง

ตัวอย่างไฟล์ผลลัพธ์:

```text
aaa_RVM_Alpha.webm
```

นี่ **ไม่ใช่รูปแบบวิดีโอ Alpha เฉพาะของ R800ZZ**

VP9 เป็นวิดีโอโคเดกแบบเปิดจาก WebM Project และ WebM รองรับวิดีโอที่มีช่องอัลฟา ข้อมูล Alpha จะถูกเก็บด้วยกลไก Alpha ของ WebM แทนการนำภาพ mask แบบกำหนดเองไปวางไว้ในพื้นที่ว่างของเฟรมวิดีโอ

ปัจจุบันเอาต์พุต WebM VP9 Alpha ของเครื่องมือนี้เข้ารหัสด้วย FFmpeg `libvpx-vp9` ขั้นตอนการเข้ารหัส VP9 Alpha ใช้ CPU แม้ว่าการประมวลผล RVM จะใช้ GPU ก็ตาม ดังนั้นการแปลง WebM VP9 Alpha อาจช้ากว่าการแปลง MP4 พื้นหลังสีเขียวอย่างมาก

### โปรแกรมเล่น VR ที่รองรับเอาต์พุต

สำหรับ MP4 พื้นหลังสีเขียว ตัวอย่างโปรแกรมเล่น VR ที่มีฟังก์ชัน chroma key ได้แก่:

- [R800ZZbrowser สำหรับ PICO/Meta](https://vr180g.com/browser/browser.php?l=th)
- [r800zzvrplayer สำหรับ PICO 4 Ultra/PICO4](https://vr180g.com/pico/vrplayer.php?l=th)

สำหรับ WebM VP9 Alpha โปรแกรมเล่น VR ที่ผมยืนยันการทำงานแล้วคือ:

- **[r800zzvrplayer 0.4 หรือใหม่กว่า](https://vr180g.com/pico/vrplayer.php?l=th)**

ณ เวลาที่เขียนเอกสารนี้ ผมยังไม่พบโปรแกรมเล่นวิดีโอ VR อื่นที่เล่นวิดีโอ WebM VP9 และใช้ช่องอัลฟาโดยตรงเป็นความโปร่งใสใน VR

ข้อความนี้ไม่ได้หมายความว่าไม่มีโปรแกรมเล่นอื่นที่รองรับ หากคุณทราบว่ามีโปรแกรมอื่น กรุณาแจ้งให้ผมทราบ

## ความต้องการของระบบ

- Windows 10 หรือ Windows 11
- Python
- FFmpeg
- การเชื่อมต่ออินเทอร์เน็ตระหว่างการตั้งค่าครั้งแรกและการใช้งาน RVM ครั้งแรก
- CPU หรือ NVIDIA / AMD / Intel GPU ที่รองรับ

เพื่อให้เข้ากันได้ดีที่สุดกับสคริปต์ตั้งค่า NVIDIA, AMD และ Intel ที่ให้มา แนะนำให้ใช้ **Python 3.10 ถึง 3.12**

## การติดตั้ง

### 1. ติดตั้ง Python

ติดตั้ง Python สำหรับ Windows

ตัว Python เอง **จะไม่ถูกติดตั้งโดยอัตโนมัติจาก R800ZZ RVM Tools**

ระหว่างติดตั้ง Python แนะนำให้เปิดตัวเลือกเพิ่ม Python ลงใน `PATH`

คุณสามารถตรวจสอบการติดตั้งจาก Command Prompt ได้ด้วย:

```bat
python --version
```

### 2. ติดตั้ง FFmpeg

FFmpeg ไม่ได้รวมอยู่ใน repository นี้

ดาวน์โหลด FFmpeg สำหรับ Windows ที่มีอย่างน้อย:

- `ffmpeg.exe`
- `ffprobe.exe`
- `libvpx-vp9`
- `libopus`
- `libx264`

สำหรับการสร้าง MP4 พื้นหลังสีเขียวด้วย GPU, FFmpeg ที่ใช้ควรมีตัวเข้ารหัสสำหรับ GPU ของคุณด้วย:

- NVIDIA: `h264_nvenc`
- AMD: `h264_amf`
- Intel: `h264_qsv`

วิธีตั้งค่าที่ง่ายที่สุดคือวาง:

```text
ffmpeg.exe
ffprobe.exe
```

ไว้ในโฟลเดอร์เดียวกับ:

```text
r800zz_rvm_video.py
```

และไฟล์ BAT

ในรูปแบบนี้ คุณ **ไม่จำเป็นต้อง** ตั้งค่าตัวแปรสภาพแวดล้อม `PATH` ของ Windows สำหรับ FFmpeg

อีกทางหนึ่ง สามารถติดตั้ง FFmpeg ไว้ที่อื่นได้ หากเพิ่มโฟลเดอร์ `bin` ของ FFmpeg ลงใน `PATH`

สามารถตรวจสอบตัวเข้ารหัสฮาร์ดแวร์ที่ใช้ได้ด้วย:

```bat
ffmpeg -encoders
```

### 3. ติดตั้ง PyTorch ให้ตรงกับฮาร์ดแวร์ของคุณ

PyTorch ไม่ได้รวมอยู่ใน repository นี้

ไฟล์ BAT สำหรับตั้งค่าจะดาวน์โหลดแพ็กเกจ Python ที่จำเป็นจากแหล่งแจกจ่ายอย่างเป็นทางการ

เลือกวิธีติดตั้งตามฮาร์ดแวร์ที่ใช้

#### NVIDIA GPU

รัน:

```text
install_python_packages.bat
```

คำสั่งนี้จะติดตั้งหรืออัปเดต PyTorch ที่รองรับ CUDA ซึ่งใช้โดยไฟล์ BAT ปกติสำหรับ NVIDIA/CPU

แพ็กเกจที่ติดตั้งจะอยู่ใน Python environment ที่คำสั่ง `python` อ้างถึง โดยปกติจะอยู่ใต้:

```text
Lib\site-packages
```

ภายในโฟลเดอร์ติดตั้ง Python นั้น

เส้นทาง NVIDIA GPU เป็นการตั้งค่า GPU ที่ R800ZZ ได้ทดสอบแล้ว

#### AMD GPU

รัน:

```text
install_python_packages_AMD.bat
```

คำสั่งนี้จะสร้าง Python virtual environment แยกต่างหาก:

```text
.venv_amd
```

ภายในโฟลเดอร์ R800ZZ RVM Tools และติดตั้ง `torch-directml` ลงไป

สำหรับการแปลง ให้ใช้ไฟล์ BAT ที่ลงท้ายด้วย:

```text
_AMD.bat
```

การรองรับ AMD GPU ใช้ DirectML และ R800ZZ ยังไม่ได้ทดสอบกับฮาร์ดแวร์ AMD จริง

#### Intel GPU / Intel integrated GPU

รัน:

```text
install_python_packages_Intel.bat
```

คำสั่งนี้จะสร้าง Python virtual environment แยกต่างหาก:

```text
.venv_intel
```

ภายในโฟลเดอร์ R800ZZ RVM Tools และติดตั้ง `torch-directml` ลงไป

สำหรับการแปลง ให้ใช้ไฟล์ BAT ที่ลงท้ายด้วย:

```text
_Intel.bat
```

การรองรับ Intel GPU ใช้ DirectML และ MP4 พื้นหลังสีเขียวจะใช้ Intel Quick Sync Video (`h264_qsv`) เมื่อสามารถใช้งานได้

R800ZZ ยังไม่ได้ทดสอบกับฮาร์ดแวร์ Intel GPU จริง

#### CPU เท่านั้น

ไม่จำเป็นต้องมี GPU

สำหรับระบบที่ใช้ CPU เท่านั้น ให้ติดตั้ง PyTorch เวอร์ชัน CPU:

```bat
python -m pip install --upgrade pip
python -m pip install numpy
python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

ไฟล์ BAT สำหรับแปลงแบบมาตรฐานจะใช้ CPU โดยอัตโนมัติเมื่อ CUDA ไม่พร้อมใช้งาน

โดยทั่วไป การแปลงด้วย CPU จะช้ากว่าการประมวลผล RVM ที่เร่งด้วย GPU

## PyTorch และ RVM ถูกดาวน์โหลดไปที่ไหน?

### PyTorch

สำหรับสภาพแวดล้อม NVIDIA/CPU ปกติ PyTorch จะถูกติดตั้งใน Python environment ที่ใช้โดยคำสั่ง `python`

ตัวอย่างเช่น การติดตั้ง Python ทั่วไปอาจเก็บแพ็กเกจไว้ที่:

```text
C:\Users\<username>\AppData\Local\Programs\Python\Python3xx\Lib\site-packages
```

ตำแหน่งจริงขึ้นอยู่กับวิธีติดตั้ง Python

สำหรับ AMD และ Intel สคริปต์ตั้งค่าที่ให้มาจะใช้ virtual environment ภายในเครื่อง:

```text
R800ZZ_RVM_Tools\.venv_amd
R800ZZ_RVM_Tools\.venv_intel
```

### RVM

RVM ถูกโหลดผ่าน PyTorch Torch Hub

ในการแปลงครั้งแรก Torch Hub จะดาวน์โหลด repository ของ RVM และโมเดล MobileNetV3 ที่ฝึกไว้ล่วงหน้าโดยอัตโนมัติ

ตำแหน่ง cache เริ่มต้นของ Torch Hub บน Windows โดยทั่วไปคือ:

```text
C:\Users\<username>\.cache\torch\hub
```

cache ของ repository RVM โดยทั่วไปจะอยู่ภายใต้ไดเรกทอรีนี้

ไฟล์น้ำหนักโมเดลที่ดาวน์โหลดมักจะถูกเก็บไว้ที่:

```text
C:\Users\<username>\.cache\torch\hub\checkpoints
```

ตำแหน่ง cache สามารถเปลี่ยนได้ด้วยการตั้งค่าสภาพแวดล้อม PyTorch เช่น `TORCH_HOME`

หลังจาก cache แล้ว ไฟล์เหล่านี้จะถูกนำมาใช้ซ้ำในการแปลงครั้งต่อไป

## วิธีใช้งาน

การแปลงทำได้โดย **ลากไฟล์วิดีโอไปวางบนไฟล์ `.bat` ที่เหมาะสมใน Windows Explorer**

ตัวอย่าง หากคุณมี:

```text
aaa.mp4
```

และต้องการสร้าง MP4 พื้นหลังสีเขียวโดยใช้ NVIDIA GPU หรือ CPU ให้ลาก:

```text
aaa.mp4
```

แล้ววางลงบน:

```text
R800ZZ_Make_Green_MP4.bat
```

ไฟล์ BAT จะรับไฟล์วิดีโอที่ถูกวางและเริ่มการแปลงโดยอัตโนมัติ

ในทำนองเดียวกัน หากต้องการสร้างวิดีโอ WebM VP9 Alpha ให้ลาก:

```text
aaa.mp4
```

แล้ววางลงบน:

```text
R800ZZ_Make_WebM_Alpha.bat
```

ไม่จำเป็นต้องเปิด Command Prompt และพิมพ์ชื่อไฟล์วิดีโอด้วยตนเอง

### สร้าง MP4 พื้นหลังสีเขียว

สำหรับ NVIDIA GPU หรือ CPU ให้ลากไฟล์วิดีโอไปวางบน:

```text
R800ZZ_Make_Green_MP4.bat
```

สำหรับ AMD GPU:

```text
R800ZZ_Make_Green_MP4_AMD.bat
```

สำหรับ Intel GPU:

```text
R800ZZ_Make_Green_MP4_Intel.bat
```

ตัวอย่าง:

```text
aaa.mp4
    ↓ ลากและวาง
R800ZZ_Make_Green_MP4.bat
```

ผลลัพธ์:

```text
aaa_RVM_Green.mp4
```

### สร้าง WebM VP9 Alpha

สำหรับ NVIDIA GPU หรือ CPU ให้ลากไฟล์วิดีโอไปวางบน:

```text
R800ZZ_Make_WebM_Alpha.bat
```

สำหรับ AMD GPU:

```text
R800ZZ_Make_WebM_Alpha_AMD.bat
```

สำหรับ Intel GPU:

```text
R800ZZ_Make_WebM_Alpha_Intel.bat
```

ตัวอย่าง:

```text
aaa.mp4
    ↓ ลากและวาง
R800ZZ_Make_WebM_Alpha.bat
```

ผลลัพธ์:

```text
aaa_RVM_Alpha.webm
```

โดยค่าเริ่มต้น ไฟล์ BAT จะบันทึกวิดีโอที่แปลงแล้วไว้ในโฟลเดอร์ R800ZZ RVM Tools

## หมายเหตุเกี่ยวกับประสิทธิภาพ

การเร่งด้วย GPU เป็นตัวเลือก ไม่ใช่ข้อบังคับ

กระบวนการปัจจุบันประกอบด้วยหลายขั้นตอน และไม่ใช่ทุกขั้นตอนที่จะเร่งด้วย GPU

### NVIDIA

- การประมวลผล RVM: CUDA GPU
- การเข้ารหัส H.264 ของ MP4 พื้นหลังสีเขียว: NVENC
- การเข้ารหัส WebM VP9 Alpha: CPU (`libvpx-vp9`)
- การถอดรหัสวิดีโออินพุตด้วย FFmpeg: CPU ในการใช้งานปัจจุบัน

### AMD

- การประมวลผล RVM: DirectML
- การเข้ารหัส H.264 ของ MP4 พื้นหลังสีเขียว: AMF
- การเข้ารหัส WebM VP9 Alpha: CPU (`libvpx-vp9`)
- การถอดรหัสวิดีโออินพุตด้วย FFmpeg: CPU ในการใช้งานปัจจุบัน

### Intel

- การประมวลผล RVM: DirectML
- การเข้ารหัส H.264 ของ MP4 พื้นหลังสีเขียว: Quick Sync Video
- การเข้ารหัส WebM VP9 Alpha: CPU (`libvpx-vp9`)
- การถอดรหัสวิดีโออินพุตด้วย FFmpeg: CPU ในการใช้งานปัจจุบัน

เนื่องจากการเข้ารหัส WebM VP9 Alpha ใช้ CPU การใช้ GPU ที่เร็วมากจึงไม่ได้ทำให้กระบวนการแปลง Alpha ทั้งหมดเร็วขึ้นในสัดส่วนเดียวกัน

การแปลง MP4 พื้นหลังสีเขียวสามารถได้ประโยชน์จาก GPU มากกว่า เพราะทั้งการประมวลผล RVM และการเข้ารหัส H.264 สามารถใช้ฮาร์ดแวร์ GPU ได้

## หมายเหตุเกี่ยวกับคุณภาพของ matting

RVM ไม่ได้ลบพื้นหลังด้วยการตรวจสอบสีพื้นหลังที่กำหนดไว้

RVM ประเมินบุคคลในส่วนหน้าและ alpha matte ด้วย neural network

ดังนั้นวิดีโออินพุตจึงไม่จำเป็นต้องมีพื้นหลังสีเขียว

โหมด MP4 พื้นหลังสีเขียวจะทำ human matting ด้วย RVM ก่อน จากนั้นจึงนำส่วนหน้าที่แยกออกมาไปวางบนพื้นหลังสีเขียวที่สร้างขึ้นใหม่

โหมด WebM VP9 Alpha ใช้ alpha matte จาก RVM โดยตรงเป็นข้อมูลความโปร่งใสของวิดีโอเอาต์พุต

ผลลัพธ์อาจแตกต่างกันตามวิดีโอต้นฉบับ การเคลื่อนไหว รายละเอียดเส้นผม การบังกัน แสง และความแม่นยำของ RVM

## สถานะการทดสอบฮาร์ดแวร์

R800ZZ ได้ทดสอบเส้นทาง NVIDIA GPU แล้ว

มีการรองรับการเร่งด้วย AMD GPU และ Intel GPU แต่ R800ZZ ยังไม่ได้ทดสอบเส้นทางเหล่านี้ด้วยระบบ AMD หรือ Intel GPU จริง

การทำงานด้วย CPU อย่างเดียวไม่จำเป็นต้องมี discrete GPU

## ซอฟต์แวร์ของบุคคลที่สาม

R800ZZ RVM Tools ใช้หรือทำงานร่วมกับโปรเจกต์ต่อไปนี้:

- Robust Video Matting
- PyTorch
- Torch-DirectML
- FFmpeg

RVM พัฒนาแยกต่างหากจาก R800ZZ RVM Tools

repository นี้ไม่มีซอร์สโค้ด RVM หรือไฟล์โมเดลที่ฝึกไว้ล่วงหน้า

## ข้อจำกัดความรับผิดชอบ

R800ZZ RVM Tools เป็นยูทิลิตีอิสระ

ความเข้ากันได้ของไฟล์เอาต์พุตขึ้นอยู่กับความสามารถของโปรแกรมเล่นวิดีโอที่ใช้เล่น

MP4 พื้นหลังสีเขียวต้องใช้โปรแกรมเล่นที่รองรับ chroma key

WebM VP9 Alpha ต้องใช้โปรแกรมเล่นที่สามารถถอดรหัสและใช้งานช่องอัลฟาของ WebM ได้จริง การรองรับวิดีโอ WebM VP9 ปกติไม่ได้หมายความว่าจะรองรับความโปร่งใส VP9 Alpha เสมอไป
