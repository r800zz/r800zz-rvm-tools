import argparse
import json
import shutil
import subprocess
import sys
from fractions import Fraction
from pathlib import Path


def find_tool(name: str) -> str:
    base = Path(__file__).resolve().parent
    local = base / f"{name}.exe"
    if local.is_file():
        return str(local)
    found = shutil.which(name) or shutil.which(f"{name}.exe")
    if found:
        return found
    raise FileNotFoundError(
        f"{name} was not found. Put {name}.exe next to this script or add it to PATH."
    )


def probe_video(ffprobe: str, input_path: Path):
    cmd = [
        ffprobe,
        "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,avg_frame_rate,r_frame_rate,nb_frames,duration",
        "-of", "json",
        str(input_path),
    ]
    data = json.loads(subprocess.check_output(cmd, text=True, encoding="utf-8"))
    streams = data.get("streams", [])
    if not streams:
        raise RuntimeError("No video stream found.")

    stream = streams[0]
    width = int(stream["width"])
    height = int(stream["height"])

    fps_text = stream.get("avg_frame_rate") or stream.get("r_frame_rate") or "30/1"
    if fps_text == "0/0":
        fps_text = stream.get("r_frame_rate") or "30/1"
    fps = Fraction(fps_text)

    total = None
    nb_frames = stream.get("nb_frames")
    if nb_frames and nb_frames != "N/A":
        try:
            total = int(nb_frames)
        except ValueError:
            pass
    if total is None:
        duration = stream.get("duration")
        if duration and duration != "N/A":
            try:
                total = round(float(duration) * float(fps))
            except ValueError:
                pass

    return width, height, fps, total


def read_frames(pipe, frame_size: int, max_frames: int):
    wanted = frame_size * max_frames
    data = bytearray()
    while len(data) < wanted:
        chunk = pipe.read(wanted - len(data))
        if not chunk:
            break
        data.extend(chunk)
    complete = len(data) // frame_size
    if complete == 0:
        return None, 0
    if len(data) != complete * frame_size:
        del data[complete * frame_size:]
    return data, complete


def load_rvm(device):
    import torch

    print("Loading Robust Video Matting (first run may download it)...")
    model = torch.hub.load(
        "PeterL1n/RobustVideoMatting",
        "mobilenetv3",
        pretrained=True,
        trust_repo=True,
    )
    model = model.eval().to(device)
    return model


def make_decoder(ffmpeg: str, input_path: Path):
    return subprocess.Popen(
        [
            ffmpeg,
            "-v", "error",
            "-i", str(input_path),
            "-map", "0:v:0",
            "-f", "rawvideo",
            "-pix_fmt", "rgb24",
            "pipe:1",
        ],
        stdout=subprocess.PIPE,
    )


def make_encoder(ffmpeg: str, input_path: Path, output_path: Path,
                 width: int, height: int, fps: Fraction,
                 mode: str, crf: int, green_encoder: str):
    fps_text = f"{fps.numerator}/{fps.denominator}"
    in_pix_fmt = "rgba" if mode == "alpha" else "rgb24"

    cmd = [
        ffmpeg,
        "-y",
        "-v", "error",
        "-f", "rawvideo",
        "-pix_fmt", in_pix_fmt,
        "-s", f"{width}x{height}",
        "-r", fps_text,
        "-i", "pipe:0",
        "-i", str(input_path),
        "-map", "0:v:0",
        "-map", "1:a:0?",
    ]

    if mode == "alpha":
        cmd += [
            "-c:v", "libvpx-vp9",
            "-pix_fmt", "yuva420p",
            "-crf", str(crf),
            "-b:v", "0",
            "-c:a", "libopus",
            "-shortest",
            str(output_path),
        ]
    else:
        if green_encoder == "nvenc":
            cmd += [
                "-c:v", "h264_nvenc",
                "-preset", "p4",
                "-cq", str(crf),
                "-b:v", "0",
                "-pix_fmt", "yuv420p",
            ]
        elif green_encoder == "amf":
            cmd += [
                "-c:v", "h264_amf",
                "-quality", "quality",
                "-rc", "cqp",
                "-qp_i", str(crf),
                "-qp_p", str(crf),
                "-qp_b", str(crf),
                "-pix_fmt", "yuv420p",
            ]
        elif green_encoder == "qsv":
            cmd += [
                "-c:v", "h264_qsv",
                "-global_quality", str(crf),
                "-pix_fmt", "nv12",
            ]
        else:
            cmd += [
                "-c:v", "libx264",
                "-crf", str(crf),
                "-pix_fmt", "yuv420p",
            ]

        cmd += [
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            str(output_path),
        ]

    return subprocess.Popen(cmd, stdin=subprocess.PIPE)



def get_directml_device(vendor: str | None = None):
    try:
        import torch_directml
    except ImportError as e:
        raise RuntimeError(
            "torch-directml is not installed. Run the AMD or Intel setup BAT first."
        ) from e

    if vendor is None:
        return torch_directml.device(), "DirectML default"

    vendor = vendor.lower()
    matches = []
    for i in range(torch_directml.device_count()):
        try:
            name = torch_directml.device_name(i)
        except Exception:
            name = ""
        low = name.lower()

        if vendor == "amd" and ("amd" in low or "radeon" in low):
            matches.append((i, name))
        elif vendor == "intel" and "intel" in low:
            matches.append((i, name))

    if not matches:
        raise RuntimeError(f"No {vendor.upper()} DirectML GPU was found.")

    index, name = matches[0]
    return torch_directml.device(index), name

def convert(args):
    try:
        import torch
    except ImportError as e:
        raise RuntimeError("PyTorch is not installed. Run install_python_packages.bat first.") from e

    input_path = Path(args.input).resolve()
    if not input_path.is_file():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    ffmpeg = find_tool("ffmpeg")
    ffprobe = find_tool("ffprobe")
    width, height, fps, total_frames = probe_video(ffprobe, input_path)

    if args.output:
        output_path = Path(args.output).resolve()
    else:
        out_dir = Path(args.output_dir).resolve() if args.output_dir else input_path.parent
        suffix = "_RVM_Alpha.webm" if args.mode == "alpha" else "_RVM_Green.mp4"
        output_path = out_dir / f"{input_path.stem}{suffix}"

    output_path.parent.mkdir(parents=True, exist_ok=True)

    device_name = None

    if args.device == "auto":
        if torch.cuda.is_available():
            device = torch.device("cuda")
            green_encoder = "nvenc"
            device_name = torch.cuda.get_device_name(0)
        else:
            device = torch.device("cpu")
            green_encoder = "x264"
            device_name = "CPU"
    elif args.device in ("directml", "amd"):
        device, device_name = get_directml_device(
            None if args.device == "directml" else "amd"
        )
        green_encoder = "amf"
    elif args.device == "intel":
        device, device_name = get_directml_device("intel")
        green_encoder = "qsv"
    else:
        device = torch.device(args.device)
        green_encoder = "nvenc" if device.type == "cuda" else "x264"
        device_name = str(device)

    print(f"Input : {input_path}")
    print(f"Output: {output_path}")
    print(f"Video : {width}x{height}  {float(fps):.3f} fps")
    print(f"Device: {device}")
    if device_name:
        print(f"GPU   : {device_name}")
    if args.mode == "green":
        encoder_name = {
            "nvenc": "h264_nvenc",
            "amf": "h264_amf",
            "qsv": "h264_qsv",
            "x264": "libx264",
        }[green_encoder]
        print(f"Encoder: {encoder_name}")

    model = load_rvm(device)
    downsample_ratio = args.downsample
    if downsample_ratio is None:
        downsample_ratio = min(512 / max(width, height), 1.0)

    decoder = make_decoder(ffmpeg, input_path)
    encoder = make_encoder(
        ffmpeg, input_path, output_path,
        width, height, fps,
        args.mode, args.crf, green_encoder,
    )

    frame_size = width * height * 3
    rec = [None, None, None, None]
    processed = 0

    try:
        with torch.inference_mode():
            while True:
                raw, count = read_frames(decoder.stdout, frame_size, args.chunk)
                if count == 0:
                    break

                src = torch.frombuffer(raw, dtype=torch.uint8)
                src = src.reshape(count, height, width, 3)
                src = src.permute(0, 3, 1, 2).unsqueeze(0)
                src = src.to(device=device, dtype=torch.float32).div_(255.0)

                fgr, pha, *rec = model(src, *rec, downsample_ratio)
                fgr = fgr.clamp_(0.0, 1.0)
                pha = pha.clamp_(0.0, 1.0)

                if args.mode == "alpha":
                    out = torch.cat((src, pha), dim=2) #bugfix September 17, 2026 Fixed incorrect background rendering.
                else:
                    green = torch.tensor(
                        [0.0, 1.0, 0.0],
                        device=device,
                        dtype=fgr.dtype,
                    ).view(1, 1, 3, 1, 1)
                    out = fgr * pha + green * (1.0 - pha)

                out = out[0].permute(0, 2, 3, 1)
                out = out.mul(255.0).round_().to(torch.uint8).cpu().contiguous()
                encoder.stdin.write(out.numpy().tobytes())

                processed += count
                if total_frames:
                    print(f"\rFrames: {processed}/{total_frames}", end="", flush=True)
                else:
                    print(f"\rFrames: {processed}", end="", flush=True)
    finally:
        print()
        if decoder.stdout:
            decoder.stdout.close()
        decoder.wait()
        if encoder.stdin:
            encoder.stdin.close()
        enc_rc = encoder.wait()

    if enc_rc != 0:
        raise RuntimeError(f"FFmpeg encoder failed with exit code {enc_rc}.")

    print("Done.")


def main():
    parser = argparse.ArgumentParser(
        description="Create RVM-matted WebM alpha video or green-screen MP4."
    )
    parser.add_argument("input", help="Input video file")
    parser.add_argument("--mode", choices=("alpha", "green"), required=True)
    parser.add_argument("--output-dir", help="Output directory")
    parser.add_argument("--output", help="Exact output file path")
    parser.add_argument("--device", default="auto", help="auto, cpu, cuda, cuda:0, directml, amd, intel, ...")
    parser.add_argument("--chunk", type=int, default=1, help="Frames processed at once")
    parser.add_argument("--downsample", type=float, default=None,
                        help="RVM downsample ratio. Default: auto")
    parser.add_argument("--crf", type=int, default=20, help="FFmpeg CRF")
    args = parser.parse_args()

    if args.chunk < 1:
        parser.error("--chunk must be 1 or greater")
    if args.downsample is not None and not (0.0 < args.downsample <= 1.0):
        parser.error("--downsample must be greater than 0 and at most 1")

    try:
        convert(args)
    except KeyboardInterrupt:
        print("\nCancelled.")
        sys.exit(130)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
