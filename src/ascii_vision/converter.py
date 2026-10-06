from PIL import Image

DEFAULT_CHARSET = "@%#*+=-:. "

def resize_image(image: Image.Image, width: int) -> Image.Image:
    "Resize image while preserving aspect ratio. Terminal characters are usually taller than they are wide, therefore the height is caled by approximately 0.5"
    original_width, original_height = image.size

    aspect_ratio = original_height / original_width
    height = max(1, int(width * aspect_ratio * 0.5))

    return image.resize((width, height))

def pixel_to_character(pixel_value: int, charset: str = DEFAULT_CHARSET) -> str:
    """Map grayscale pixel intensity to an ASCII character."""
    index = int(pixel_value / 255 * (len(charset) - 1))
    return charset[index]

def image_to_ascii(image: Image.Image, width: int = 100, charset: str = DEFAULT_CHARSET) -> str:
    "Convert an image into ASCII art."
    image = image.convert("L")
    image = resize_image(image, width)

    pixels = image.load()
    image_width, image_height = image.size

    lines = []

    for y in range(image_height):
        line = []

        for x in range(image_width):
            pixel = pixels[x, y]
            character = pixel_to_character(pixel, charset)
            line.append(character)

        lines.append("".join(line))

def convert_image(input_path: str, output_path: str, width: int = 100, charset: str = DEFAULT_CHARSET) -> None:
    """Convert an image file to an ASCII text file."""
    image = Image.open(input_path)

    ascii_art = image_to_ascii(image, width, charset)