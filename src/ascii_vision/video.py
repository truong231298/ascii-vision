"""Frame-by-frame video to ASCII video conversion (requires OpenCV)."""

from __future__ import annotations

from pathlib import Path
import argparse

from .converter import DEFAULT_CHARSET, image_to_ascii


def video_to_ascii_video(
    input_path: str | Path,
    output_path: str | Path,
    *,
    width: int = 100,
    charset: str = DEFAULT_CHARSET,
) -> Path:
    """Convert a video to an MP4 video containing rendered ASCII frames."""
    try:
        import cv2
        import numpy as np
        from PIL import Image, ImageDraw, ImageFont
    except ImportError as exc:
        raise RuntimeError("Video conversion requires OpenCV and NumPy. Install with: pip install ascii-vision[video]") from exc

    capture = cv2.VideoCapture(str(input_path))
    if not capture.isOpened():
        raise ValueError(f"Could not open video: {input_path}")
    fps = capture.get(cv2.CAP_PROP_FPS) or 24.0
    destination = Path(output_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    writer = None
    font_size = 12
    font = ImageFont.load_default(size=font_size)
    try:
        while True:
            ok, frame = capture.read()
            if not ok:
                break
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            art = image_to_ascii(Image.fromarray(rgb), width=width, charset=charset)
            lines = art.splitlines()
            probe = Image.new("RGB", (1, 1))
            draw = ImageDraw.Draw(probe)
            bbox = draw.textbbox((0, 0), "M", font=font)
            char_width = max(1, round(draw.textlength("M", font=font)))
            line_height = max(1, bbox[3] - bbox[1] + 1)
            size = (max(1, width * char_width), max(1, len(lines) * line_height))
            canvas = Image.new("RGB", size, "black")
            canvas_draw = ImageDraw.Draw(canvas)
            for row, line in enumerate(lines):
                canvas_draw.text((0, row * line_height), line, fill="white", font=font)
            rgb_frame = np.asarray(canvas)
            if writer is None:
                writer = cv2.VideoWriter(str(destination), cv2.VideoWriter_fourcc(*"mp4v"), fps, size)
                if not writer.isOpened():
                    raise RuntimeError(f"Could not create output video: {destination}")
            writer.write(cv2.cvtColor(rgb_frame, cv2.COLOR_RGB2BGR))
    finally:
        capture.release()
        if writer is not None:
            writer.release()
    if writer is None:
        raise ValueError(f"Video contains no readable frames: {input_path}")
    return destination


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Convert a video into ASCII-rendered MP4 frames.")
    parser.add_argument("input", type=Path, help="source video path")
    parser.add_argument("--output", type=Path, default=Path("outputs/ascii_video.mp4"))
    parser.add_argument("--width", type=int, default=100)
    parser.add_argument("--charset", default=DEFAULT_CHARSET)
    args = parser.parse_args(argv)
    if args.width < 1:
        parser.error("--width must be at least 1")
    try:
        result = video_to_ascii_video(args.input, args.output, width=args.width, charset=args.charset)
    except (OSError, ValueError, RuntimeError) as exc:
        parser.error(str(exc))
    print(f"ASCII video saved to: {result}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
