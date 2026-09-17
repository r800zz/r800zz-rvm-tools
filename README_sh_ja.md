[English](README_sh_en.md) | [Русский](README_sh_ru.md) | [Español](README_sh_es.md) | [ภาษาไทย](README_sh_th.md) | [中文](README_sh_zh.md) | [한국어](README_sh_ko.md) | [日本語](README_sh_ja.md)

## UNIXライクOS（Linux、WSL、macOS）

R800ZZ RVM Tools は Linux および macOS でも使用できます。

Linux での動作は、R800ZZ が **Windows 11 上の WSL2 の Ubuntu** を使用してテストしました。

テストした WSL2 環境では、CUDA を通じて **NVIDIA GPU** を RVM 推論に使用でき、Green-screen MP4 と WebM VP9 Alpha の両方の動画を正常に生成できました。

このテストでは macOS は使用していません。

## クイック使用ガイド

最初に Python、FFmpeg、および必要な Python パッケージをインストールしてください。

Green-screen MP4 を作成するには:

```bash
bash green.sh "input.mp4"
```

例:

```bash
bash green.sh "aaa.mp4"
```

出力:

```text
aaa_RVM_Green.mp4
```

WebM VP9 Alpha 動画を作成するには:

```bash
bash alphavp9.sh "input.mp4"
```

例:

```bash
bash alphavp9.sh "aaa.mp4"
```

出力:

```text
aaa_RVM_Alpha.webm
```

動画ファイルのパスには絶対パスも指定できます。

例:

```bash
bash green.sh "/home/user/Videos/aaa.mp4"
```

WSL2 では、Windows の C: ドライブに保存された動画を、次のような WSL パスで指定できます:

```bash
bash green.sh "/mnt/c/Videos/aaa.mp4"
```

## Linux の要件

Python、FFmpeg、Git、および Python の仮想環境サポートをインストールします。

Ubuntu / WSL2 の場合:

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv ffmpeg git
```

インストールを確認します:

```bash
python3 --version
ffmpeg -version
```

## Python 環境

Python 仮想環境を作成します:

```bash
python3 -m venv .venv_linux
source .venv_linux/bin/activate
```

pip を更新します:

```bash
python -m pip install --upgrade pip
```

## Linux / WSL2 で NVIDIA GPU を使用する場合

CUDA 対応の NVIDIA GPU を使用する場合は、CUDA 対応版の PyTorch をインストールしてください。

使用する PyTorch CUDA パッケージは、現在サポートされている PyTorch 環境に合わせる必要があります。

インストール後、PyTorch が NVIDIA GPU を使用できるか次のコマンドで確認できます:

```bash
python -c "import torch; print(torch.__version__); print(torch.version.cuda); print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')"
```

CUDA の利用可否として:

```text
True
```

と表示されれば、RVM は NVIDIA GPU を使用できます。

## FFmpeg

Linux では、パッケージマネージャーからインストールされたシステムの FFmpeg を使用します。

次のコマンドをターミナルから実行できる必要があります:

```bash
ffmpeg
ffprobe
```

Windows 版とは異なり、`ffmpeg.exe` や `ffprobe.exe` を R800ZZ RVM Tools のディレクトリに置く必要はありません。

## WSL2 の NVIDIA GPU サポート

WSL2 を使用する場合、WSL 内から NVIDIA GPU にアクセスできる状態になっている必要があります。

次のコマンドで確認できます:

```bash
nvidia-smi
```

NVIDIA GPU が表示されれば、適切な PyTorch パッケージをインストールした後、CUDA 対応 PyTorch から GPU を使用できます。

## Green-screen MP4

通常の動画を Green-screen MP4 に変換するには:

```bash
bash green.sh "input.mp4"
```

RVM が人物の前景を抽出し、純粋な緑色の背景上に合成します。

例:

```text
Input:
aaa.mp4

Output:
aaa_RVM_Green.mp4
```

NVIDIA GPU アクセラレーションが利用できる場合、RVM 推論に CUDA を使用できます。

インストールされている FFmpeg ビルドが対応している場合、Green-screen MP4 の変換では NVIDIA ハードウェア H.264 エンコードも使用できます。

## WebM VP9 Alpha

実際のアルファチャンネルを持つ WebM VP9 動画を作成するには:

```bash
bash alphavp9.sh "input.mp4"
```

例:

```text
Input:
aaa.mp4

Output:
aaa_RVM_Alpha.webm
```

RVM が人物のアルファマットを生成し、それが WebM VP9 出力の透明度情報として保存されます。

CUDA が利用できる場合、RVM 推論に NVIDIA GPU を使用できます。

WebM VP9 Alpha のエンコード処理では FFmpeg の `libvpx-vp9` を使用し、CPU ベースで処理されるため、この変換は通常 Green-screen MP4 の変換より遅くなります。

## macOS

Linux/macOS 用シェルスクリプト版は macOS にも対応することを想定しています。

ただし、現在の Linux/macOS 版は、物理 macOS ハードウェアではなく、R800ZZ が **WSL2 上の Ubuntu** でテストしています。

そのため、macOS での GPU アクセラレーションの動作は R800ZZ では確認していません。

CPU での動作には NVIDIA GPU は必要ありません。
