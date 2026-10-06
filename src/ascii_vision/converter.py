"""Convert images into character-based art."""

from __future__ import annotations

from pathlib import Path
from typing import TypeAlias

from PIL import Image, ImageOps

ImageSource: TypeAlias = Image.Image | str | Path
DEFAULT_CHARSET = "@%#*+=-:. "


def image_to_ascii(
    image: ImageSource,
    width: int = 100,
    charset: str = DEFAULT_CHARSET,
    *,
    aspect_ratio: float = 0.5,
    mode: str = "grayscale",
) -> str:
    """Convert an image or image path to ASCII text.

    ``aspect_ratio`` compensates for terminal characters being taller than
    they are wide. ``mode`` can be ``grayscale`` or ``color``; color output
    is represented by ANSI true-color escape sequences.
    """
    if width < 1:
        raise ValueError("width must be at least 1")
    if not charset:
        raise ValueError("charset must contain at least one character")
    if aspect_ratio <= 0:
        raise ValueError("aspect_ratio must be greater than 0")
    if mode not in {"grayscale", "color"}:
        raise ValueError("mode must be 'grayscale' or 'color'")

    if isinstance(image, (str, Path)):
        with Image.open(image) as opened:
            return image_to_ascii(opened, width, charset, aspect_ratio=aspect_ratio, mode=mode)

    source = ImageOps.exif_transpose(image)
    if source.width < 1 or source.height < 1:
        raise ValueError("image must have non-zero dimensions")
    height = max(1, round(source.height / source.width * width * aspect_ratio))
    resized = source.resize((width, height), Image.Resampling.LANCZOS)
    grayscale = resized.convert("L")
    pixels = list(grayscale.getdata())
    colors = list(resized.convert("RGB").getdata()) if mode == "color" else None
    lines: list[str] = []

    for y in range(height):
        row: list[str] = []
        for x in range(width):
            index = y * width + x
            shade = pixels[index]
            char = charset[round((255 - shade) / 255 * (len(charset) - 1))]
            if colors is not None:
                red, green, blue = colors[index]
                row.append(f"\033[38;2;{red};{green};{blue}m{char}\033[0m")
            else:
                row.append(char)
        lines.append("".join(row))
    return "\n".join(lines)

