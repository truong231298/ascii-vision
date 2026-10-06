import argparse
from converter import convert_image

def main():
    parser = argparse.ArgumentParser(
        description='Convert an image to ASCII art.'
    )

    parser.add_argument(
        'input',
        help="Path to input image"
    )

    parser.add_argument(
        "-o",
        "--output",
        default="outputs/output.txt",
        help="Path to output ASCII file"
    )

    parser.add_argument(
        "-w",
        "--width",
        type=int,
        default=100,
        help="Output ASCII width."
    )

    parser.add_argument(
        "--charset",
        default="@%#*+=-:. ",
        help="Character used for ASCII rendering."
    )

    args = parser.parse_args()

    convert_image(args.input, args.output, args.width, args.charset)

    print(f"ASCII image saved to {args.output}")
