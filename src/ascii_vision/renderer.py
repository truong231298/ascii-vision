"""Render ASCII art to raster images using Pillow."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def render_ascii_image(
    ascii_art: str,
    output_path: str | Path,
    *,
    font_size: int = 12,
    foreground: str = "white",
    background: str = "black",
) -> Path:
    """Render plain ASCII text as a PNG or JPEG image."""
    destination = Path(output_path)
    extension = destination.suffix.lower()
    if extension not in {".png", ".jpg", ".jpeg"}:
        raise ValueError("image output must use .png, .jpg, or .jpeg")
    if font_size < 1:
        raise ValueError("font_size must be at least 1")

    font = ImageFont.load_default(size=font_size)
    lines = ascii_art.splitlines() or [""]
    probe = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(probe)
    bbox = draw.textbbox((0, 0), "M", font=font)
    char_width = max(1, draw.textlength("M", font=font))
    line_height = max(1, bbox[3] - bbox[1] + 1)
    width = max(1, round(max(map(len, lines), default=0) * char_width))
    height = max(1, len(lines) * line_height)
    image = Image.new("RGB", (width, height), background)
    draw = ImageDraw.Draw(image)
    for row, line in enumerate(lines):
        draw.text((0, row * line_height), line, fill=foreground, font=font)

    destination.parent.mkdir(parents=True, exist_ok=True)
    if extension in {".jpg", ".jpeg"}:
        image.save(destination, quality=95)
    else:
        image.save(destination)
    return destination

