"""Command-line interface for ASCII-Vision."""

from __future__ import annotations

import argparse
from pathlib import Path

from .converter import DEFAULT_CHARSET, image_to_ascii
from .renderer import render_ascii_image


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Convert an image into ASCII art.")
    parser.add_argument("input", type=Path, help="path to the source image")
    parser.add_argument("--width", type=int, default=100, help="output character width (default: 100)")
    parser.add_argument("--charset", default=DEFAULT_CHARSET, help="characters from darkest to brightest")
    parser.add_argument("--mode", choices=("grayscale", "color"), default="grayscale", help="terminal output mode")
    parser.add_argument("--output", type=Path, help="output .txt, .png, or .jpg path")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.width < 1:
        parser.error("--width must be at least 1")
    if not args.charset:
        parser.error("--charset must not be empty")
    if not args.input.is_file():
        parser.error(f"input file does not exist: {args.input}")
    output = args.output or Path("outputs/output.txt")
    try:
        art = image_to_ascii(args.input, width=args.width, charset=args.charset, mode=args.mode)
        if output.suffix.lower() in {".png", ".jpg", ".jpeg"}:
            if args.mode == "color":
                parser.error("color mode is supported for terminal output; image export is grayscale")
            render_ascii_image(art, output)
        elif output.suffix.lower() == ".txt":
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(art + "\n", encoding="utf-8")
        else:
            parser.error("--output must end in .txt, .png, or .jpg")
    except (OSError, ValueError) as exc:
        parser.error(str(exc))
    print(f"ASCII art saved to: {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

