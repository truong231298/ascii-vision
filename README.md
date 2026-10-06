# ASCII-Vision

ASCII-Vision is a lightweight image processing project that converts images into ASCII art. It resizes an image, accounts for the proportions of terminal characters, converts pixel brightness into a configurable character set, and can save the result as text or a rendered image. An optional video module converts video frames into an MP4 of ASCII art.

## Features

- Grayscale and ANSI true-color terminal output
- Configurable output width and character set
- Save text as `.txt`, or render it to `.png` / `.jpg`
- Optional frame-by-frame MP4 conversion
- Python API and command-line interface
- Pillow-based processing; video support uses OpenCV

## How the conversion works

```text
Input image → resize and aspect correction → grayscale intensity
           → map intensity to a character → text or rendered image
```

Dark pixels map to dense characters and bright pixels map to lighter characters. The default character set, ordered from darkest to brightest, is `@%#*+=-:. `.

## Install

Python 3.10 or newer is required.

```bash
git clone https://github.com/YOUR_USERNAME/ascii-vision.git
cd ascii-vision
python -m venv .venv
```

Activate the environment (`.venv\Scripts\activate` on Windows, or `source .venv/bin/activate` on macOS/Linux), then install:

```bash
pip install -e .
```

For video conversion, install the optional dependencies:

```bash
pip install -e ".[video]"
```

## Image conversion

Run from the repository root:

```bash
python -m ascii_vision.main examples/input.jpg
```

By default, the program writes `outputs/output.txt`. Increase the width for more detail or select another character set:

```bash
python -m ascii_vision.main examples/input.jpg --width 120
python -m ascii_vision.main examples/input.jpg --charset "@#*:. " --output outputs/portrait.txt
```

Render the characters to an image:

```bash
python -m ascii_vision.main examples/input.jpg --output outputs/ascii.png
```

Print colored characters in a terminal that supports ANSI true color:

```bash
python -m ascii_vision.main examples/input.jpg --mode color
```

The `ascii-vision` command is also available after installation:

```bash
ascii-vision examples/input.jpg --width 120 --output outputs/result.txt
```

## Video conversion

After installing the `[video]` extra, convert frames while preserving the source FPS:

```bash
python -m ascii_vision.video examples/sample_video.mp4 --output outputs/ascii_video.mp4
```

Video processing uses OpenCV's MP4V codec; codec availability depends on the local OpenCV build.

## Python API

```python
from PIL import Image
from ascii_vision import image_to_ascii

with Image.open("examples/input.jpg") as image:
    art = image_to_ascii(image, width=100)
print(art)
```

`image_to_ascii` accepts a Pillow image or an image path. It supports `width`, `charset`, `aspect_ratio` (default `0.5`), and `mode` (`"grayscale"` or `"color"`). Color mode returns ANSI escape sequences for terminal display.

## Project layout

```text
src/ascii_vision/   Conversion library, renderers, CLI, and video module
examples/           Example input media
outputs/            Generated output (ignored by Git)
tests/              Reserved for automated tests
```

## Current scope

The image converter, text/image exports, terminal color mode, and video conversion module are implemented. The video module requires the optional dependencies above. Automated tests, image color rendering, benchmarks, demos, and AI-based processing are future work. No trained model or external service is used.

## License

Apache License 2.0. See [LICENSE](LICENSE).
