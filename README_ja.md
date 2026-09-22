# R800ZZ RVM Tools

[English](README.md) | [Русский](README_ru.md) | [Español](README_es.md) | [ภาษาไทย](README_th.md) | [中文](README_zh.md) | [한국어](README_ko.md) | [日本語](README_ja.md)

WindowsとNVIDIA GPUを使用している場合は、[r800zzXRdlnaServer for Windows+NVIDIA GPU](https://github.com/r800zz/r800zzxrdlnaserver/blob/main/README_ja.md)のほうがおすすめです。

R800ZZ RVM Tools は、通常の動画ファイルを背景透過に適した動画へ変換するツールです。

人物の前景抽出には **Robust Video Matting (RVM)**、動画のデコードとエンコードには **FFmpeg** を使用します。

2種類の出力モードに対応しています。

- **緑背景 MP4** — 抽出した人物を純緑色の背景に合成した H.264 MP4 を作成します。
- **WebM VP9 Alpha** — 実際のアルファチャンネルを持つ WebM VP9 動画を作成します。

高性能GPUは必須ではありません。CPUだけでも実行できますが、GPUアクセラレーションを使用するとRVM処理を大幅に高速化できます。

[README , UnixライクOS(Linux , WSL , macOS)](README_sh_ja.md)

## 更新履歴

### 2026年9月17日

* アルファモードの背景描画を修正。
* Unix系OS（Linux、WSL、macOS）向けのBashスクリプトを追加。


## 実行方法の簡易説明 (Windows)

- 前提として Python と FFmpeg をインストールしてください。

- 初回は `install_python_packages_NVIDIA.bat` を実行してください。

- 緑背景に変換する場合は、動画ファイルを `R800ZZ_Make_Green_MP4_NVIDIA.bat` にドラッグ＆ドロップしてください。

- Alpha透過（WebM VP9）に変換する場合は、動画ファイルを `R800ZZ_Make_WebM_Alpha_NVIDIA.bat` にドラッグ＆ドロップしてください。

## RVMとは？

RVMは **Robust Video Matting** の略です。

RVMは、動画フレーム間の時間的な情報を保ちながら、人物と背景を分離するために設計されたニューラルネットワークベースの人物動画マッティングモデルです。

このツールは PyTorch Torch Hub を通して上流のRVMプロジェクトを使用します。

RVMのソースコードと学習済みモデルは**このリポジトリには含まれていません**。必要になった時に上流プロジェクトからダウンロードされます。

## 出力モード

### 緑背景 MP4

RVMで抽出した人物を純緑色の背景に合成し、H.264 MP4としてエンコードします。

出力例：

```text
aaa_RVM_Green.mp4
```

このモードは、クロマキー透過に対応したVR動画プレイヤー向けです。

例：

- [PICO/Meta向け R800ZZbrowser](https://vr180g.com/browser/browser.php?l=jp)
- [PICO 4 Ultra/PICO4向け r800zzvrplayer](https://vr180g.com/pico/vrplayer.php?l=jp)

緑背景への変換は通常、WebM VP9 Alphaへの変換よりかなり高速です。

対応環境では、H.264のハードウェアエンコードを使用します。

| ハードウェア | RVM推論 | H.264エンコーダ |
| --- | --- | --- |
| NVIDIA GPU | PyTorch CUDA | `h264_nvenc` |
| AMD GPU | PyTorch DirectML | `h264_amf` |
| Intel GPU / Intel内蔵GPU | PyTorch DirectML | `h264_qsv` |
| CPUのみ | PyTorch CPU | `libx264` |

### WebM VP9 Alpha

このモードでは、実際のアルファチャンネルを持つVP9のWebM動画を作成します。

出力例：

```text
aaa_RVM_Alpha.webm
```

これは **R800ZZ独自のAlpha動画形式ではありません**。

VP9はWebM Projectのオープンな動画コーデックで、WebMはアルファチャンネル付き動画に対応しています。Alphaデータは、動画フレームの未使用領域に独自のマスク画像を配置するのではなく、WebMのAlpha機構を使って保存されます。

このツールが作成するWebM VP9 Alphaは、現在FFmpegの `libvpx-vp9` でエンコードしています。RVM推論にGPUを使用していても、VP9 Alphaのエンコード処理はCPUで行われます。そのため、WebM VP9 Alphaへの変換は緑背景MP4への変換より大幅に遅くなる場合があります。

### 出力に対応するVRプレイヤー

緑背景MP4について、クロマキー機能を持つVRプレイヤーの例：

- [PICO/Meta向け R800ZZbrowser](https://vr180g.com/browser/browser.php?l=jp)
- [PICO 4 Ultra/PICO4向け r800zzvrplayer](https://vr180g.com/pico/vrplayer.php?l=jp)

WebM VP9 Alphaについて、私が動作を確認しているVRプレイヤーは次のものです。

- **[r800zzvrplayer 0.5以降](https://vr180g.com/pico/vrplayer.php?l=jp)**

執筆時点では、WebM VP9動画のアルファチャンネルをVR透過として直接再生する別のVR動画プレイヤーを確認できていません。

これは、他に対応プレイヤーが存在しないと断言するものではありません。ご存じの場合は教えてください。

## 必要環境

- Windows 10 または Windows 11
- Python
- FFmpeg
- 初期セットアップ時およびRVM初回実行時のインターネット接続
- CPU、または対応する NVIDIA / AMD / Intel GPU

付属するNVIDIA、AMD、Intel用セットアップスクリプトとの互換性を広く確保するため、**Python 3.10～3.12を推奨**します。

## インストール

### 1. Pythonをインストール

Windows版Pythonをインストールしてください。

Python自体は **R800ZZ RVM Toolsによって自動インストールされません**。

Pythonのインストール時に、Pythonを `PATH` に追加するオプションを有効にすることを推奨します。

コマンドプロンプトで次のように確認できます。

```bat
python --version
```

### 2. FFmpegをインストール

FFmpegはこのリポジトリには含まれていません。

少なくとも次を含むWindows版FFmpegをダウンロードしてください。

- `ffmpeg.exe`
- `ffprobe.exe`
- `libvpx-vp9`
- `libopus`
- `libx264`

GPUで緑背景MP4のエンコードを高速化する場合、使用するGPUに対応した次のエンコーダもFFmpegに含まれている必要があります。

- NVIDIA: `h264_nvenc`
- AMD: `h264_amf`
- Intel: `h264_qsv`

もっとも簡単な方法は、

```text
ffmpeg.exe
ffprobe.exe
```

を、

```text
r800zz_rvm_video.py
```

およびBATファイルと同じフォルダに置くことです。

この構成なら、FFmpeg用にWindowsの `PATH` 環境変数を設定する必要は**ありません**。

別の場所にFFmpegをインストールし、その `bin` フォルダを `PATH` に追加して使用することもできます。

利用可能なハードウェアエンコーダは次のコマンドで確認できます。

```bat
ffmpeg -encoders
```

### 3. ハードウェアに合ったPyTorchをインストール

PyTorchはこのリポジトリには同梱されていません。

セットアップ用BATファイルが、必要なPythonパッケージを公式の配布元からダウンロードします。

使用するハードウェアに合ったセットアップ方法を選んでください。

#### NVIDIA GPU

次を実行します。

```text
install_python_packages.bat
```

通常のNVIDIA/CPU用BATファイルで使用する、CUDA対応PyTorch環境をインストールまたは更新します。

インストールされるパッケージは、`python` コマンドが指しているPython環境に入り、通常はそのPythonインストール先の次の場所にあります。

```text
Lib\site-packages
```

NVIDIA GPUの経路は、R800ZZが動作確認したGPU構成です。

#### AMD GPU

次を実行します。

```text
install_python_packages_AMD.bat
```

R800ZZ RVM Toolsフォルダ内に、独立したPython仮想環境を作成します。

```text
.venv_amd
```

そして、その中に `torch-directml` をインストールします。

変換には末尾が次のBATファイルを使用します。

```text
_AMD.bat
```

AMD GPU対応はDirectMLを使用します。R800ZZは実機のAMD GPUでは動作確認していません。

#### Intel GPU / Intel内蔵GPU

次を実行します。

```text
install_python_packages_Intel.bat
```

R800ZZ RVM Toolsフォルダ内に、独立したPython仮想環境を作成します。

```text
.venv_intel
```

そして、その中に `torch-directml` をインストールします。

変換には末尾が次のBATファイルを使用します。

```text
_Intel.bat
```

Intel GPU対応はDirectMLを使用し、利用可能な場合、緑背景MP4にはIntel Quick Sync Video（`h264_qsv`）を使用します。

R800ZZは実機のIntel GPUでは動作確認していません。

#### CPUのみ

GPUは必須ではありません。

CPUのみの環境では、CPU版PyTorchをインストールしてください。

```bat
python -m pip install --upgrade pip
python -m pip install numpy
python -m pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

標準の変換用BATファイルは、CUDAが利用できない場合、自動的にCPU処理を使用します。

CPUでの変換は通常、GPUで高速化したRVM推論より遅くなります。

## PyTorchとRVMはどこにダウンロードされますか？

### PyTorch

通常のNVIDIA/CPU環境では、PyTorchは `python` コマンドで使用されるPython環境にインストールされます。

一般的なPythonインストールでは、例えば次の場所にパッケージが保存されます。

```text
C:\Users\<username>\AppData\Local\Programs\Python\Python3xx\Lib\site-packages
```

正確な場所はPythonのインストール方法によって異なります。

AMDとIntelでは、付属のセットアップスクリプトがローカルの仮想環境を使用します。

```text
R800ZZ_RVM_Tools\.venv_amd
R800ZZ_RVM_Tools\.venv_intel
```

### RVM

RVMはPyTorch Torch Hubを通して読み込まれます。

初回の変換時に、Torch HubがRVMリポジトリと学習済みMobileNetV3モデルを自動的にダウンロードします。

WindowsでのTorch Hubの標準キャッシュは通常、次の場所です。

```text
C:\Users\<username>\.cache\torch\hub
```

RVMリポジトリのキャッシュは通常、このディレクトリ以下に作られます。

ダウンロードされたモデルの重みは通常、次の場所に保存されます。

```text
C:\Users\<username>\.cache\torch\hub\checkpoints
```

正確なキャッシュ場所は `TORCH_HOME` などのPyTorch環境設定によって変更できます。

一度キャッシュされたファイルは、以降の変換で再利用されます。

## 使用方法

変換は、**Windows Explorerで動画ファイルを目的の `.bat` ファイルへドラッグ＆ドロップ**して行います。

例えば、

```text
aaa.mp4
```

があり、NVIDIA GPUまたはCPUで緑背景MP4を作成する場合、

```text
aaa.mp4
```

を、

```text
R800ZZ_Make_Green_MP4.bat
```

へ直接ドラッグ＆ドロップします。

BATファイルがドロップされた動画ファイルを受け取り、自動的に変換を開始します。

同様に、WebM VP9 Alpha動画を作成する場合は、

```text
aaa.mp4
```

を、

```text
R800ZZ_Make_WebM_Alpha.bat
```

へドラッグ＆ドロップします。

コマンドプロンプトを開いて動画ファイル名を手入力する必要はありません。

### 緑背景MP4を作成

NVIDIA GPUまたはCPUでは、動画ファイルを次へドラッグ＆ドロップします。

```text
R800ZZ_Make_Green_MP4.bat
```

AMD GPUでは：

```text
R800ZZ_Make_Green_MP4_AMD.bat
```

Intel GPUでは：

```text
R800ZZ_Make_Green_MP4_Intel.bat
```

例：

```text
aaa.mp4
    ↓ ドラッグ＆ドロップ
R800ZZ_Make_Green_MP4.bat
```

出力：

```text
aaa_RVM_Green.mp4
```

### WebM VP9 Alphaを作成

NVIDIA GPUまたはCPUでは、動画ファイルを次へドラッグ＆ドロップします。

```text
R800ZZ_Make_WebM_Alpha.bat
```

AMD GPUでは：

```text
R800ZZ_Make_WebM_Alpha_AMD.bat
```

Intel GPUでは：

```text
R800ZZ_Make_WebM_Alpha_Intel.bat
```

例：

```text
aaa.mp4
    ↓ ドラッグ＆ドロップ
R800ZZ_Make_WebM_Alpha.bat
```

出力：

```text
aaa_RVM_Alpha.webm
```

標準では、BATファイルは変換後の動画をR800ZZ RVM Toolsフォルダに保存します。

## パフォーマンスについて

GPUアクセラレーションは任意です。

現在の処理パイプラインはいくつかの異なる処理段階から構成されており、すべての処理がGPUで高速化されるわけではありません。

### NVIDIA

- RVM推論：CUDA GPU
- 緑背景MP4のH.264エンコード：NVENC
- WebM VP9 Alphaエンコード：CPU（`libvpx-vp9`）
- FFmpegによる入力動画のデコード：現在の実装ではCPU

### AMD

- RVM推論：DirectML
- 緑背景MP4のH.264エンコード：AMF
- WebM VP9 Alphaエンコード：CPU（`libvpx-vp9`）
- FFmpegによる入力動画のデコード：現在の実装ではCPU

### Intel

- RVM推論：DirectML
- 緑背景MP4のH.264エンコード：Quick Sync Video
- WebM VP9 Alphaエンコード：CPU（`libvpx-vp9`）
- FFmpegによる入力動画のデコード：現在の実装ではCPU

WebM VP9 AlphaのエンコードはCPUを使用するため、非常に高速なGPUを使用してもAlpha変換処理全体が同じように高速になるわけではありません。

緑背景MP4は、RVM推論とH.264エンコードの両方でGPUを利用できるため、GPUアクセラレーションの効果をより大きく受けられます。

## マッティング品質について

RVMは、特定の背景色を判定して背景を削除するものではありません。

ニューラルネットワークを使用して人物の前景とAlphaマットを推定します。

そのため、入力動画の背景が緑色である必要はありません。

緑背景MP4モードでは、まずRVMで人物を抽出し、その後、新しく生成した緑背景の上に前景を配置します。

WebM VP9 Alphaモードでは、RVMのAlphaマットをそのまま出力動画の透明度情報として使用します。

結果は、元動画、動き、髪の細部、遮蔽、照明、RVMの推定精度などによって変わる場合があります。

## ハードウェア動作確認状況

R800ZZはNVIDIA GPU経路で動作確認しています。

AMD GPUアクセラレーションとIntel GPUアクセラレーションも含まれていますが、R800ZZ自身は実機のAMD GPUまたはIntel GPU環境では動作確認していません。

CPU動作にはディスクリートGPUは必要ありません。

## サードパーティソフトウェア

R800ZZ RVM Toolsは、次のプロジェクトを使用、または連携して動作します。

- Robust Video Matting
- PyTorch
- Torch-DirectML
- FFmpeg

RVMはR800ZZ RVM Toolsとは別に開発されています。

このリポジトリには、RVMのソースコードおよび学習済みモデルファイルは含まれていません。

## 免責事項

R800ZZ RVM Toolsは独立したユーティリティです。

出力動画の互換性は、再生に使用する動画プレイヤーの機能に依存します。

緑背景MP4にはクロマキーに対応したプレイヤーが必要です。

WebM VP9 Alphaには、WebMのアルファチャンネルを実際にデコードして利用するプレイヤーが必要です。通常のWebM VP9動画に対応しているだけでは、VP9 Alpha透過に対応しているとは限りません。
