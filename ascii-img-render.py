#!/usr/bin/env python3
"""
ascii-img-render.py

Usage:
  # With 1080p preset and default font:
  python3 ascii-img-render.py -i art.txt -p 1080p -o ascii_bg.png

  # Custom resolution and TTF font:
  python3 ascii-img-render.py -i art.txt -r 1280x720 -f /path/Terminus32.ttf -s 24 -c ff0000 -B 000000 -o ascii_bg.png

Options:
  -i, --input       ASCII art text file (required)
  -p, --preset      Resolution preset: 1080p, 720p, 4k
  -r, --resolution  Custom resolution: WIDTHxHEIGHT (e.g., 1920x1080)
  -f, --font        Path to TTF font file (defaults to Terminus32 if not specified)
  -s, --size        Font size in pts (default: 12)
  -c, --color       Text color in RRGGBB or RGB format (without "#", default: ffffff)
  -B, --bg          Background color in RRGGBB or RGB format (without "#", default: 000000)
  -b, --braille     Use braille font rendering for ASCII art
  -o, --output      Output PNG file path (required)
"""
import sys
import subprocess
import argparse
import tempfile
import os
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

PRESETS = {
    '1080p': (1920, 1080),
    '720p': (1280, 720),
    '4k':   (3840, 2160),
}

def parse_resolution(res_str):
    try:
        w, h = map(int, res_str.lower().split('x'))
        return w, h
    except Exception:
        raise argparse.ArgumentTypeError(
            "Resolution must be in format WIDTHxHEIGHT, e.g. 1920x1080"
        )

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    if len(hex_str) == 3:
        hex_str = ''.join([c*2 for c in hex_str])
    if len(hex_str) != 6:
        raise argparse.ArgumentTypeError(f"Invalid color format: {hex_str}")
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Render ASCII art to PNG with fixed resolution or preset'
    )
    parser.add_argument('-i', '--input', type=str, required=True, help='Input ASCII art text file')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-p', '--preset', choices=PRESETS.keys(), help='Resolution preset')
    group.add_argument('-r', '--resolution', type=parse_resolution, help='Custom resolution WIDTHxHEIGHT')
    parser.add_argument('-f', '--font', default='TerminusTTF.ttf', help='Path to TTF font file')
    parser.add_argument('-s', '--size', type=int, default=12, help='Font size in pts (default: 12)')
    parser.add_argument('-c', '--color', type=hex_to_rgb, default='ffffff', help='Text color RRGGBB or RGB (without "#")')
    parser.add_argument('-B', '--bg', dest='bg', type=hex_to_rgb, default='000000', help='Background color RRGGBB or RGB (without "#")')
    parser.add_argument('-b', '--braille', action='store_true', help='Use braille font rendering for ASCII art')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output PNG file path')
    args = parser.parse_args()

    # Check input file
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Input ASCII art file {input_path} not found", file=sys.stderr)
        sys.exit(1)
    if not input_path.is_file():
        print(f"{input_path} is not a file", file=sys.stderr)
        sys.exit(1)

    # Canvas size
    canvas_w, canvas_h = PRESETS[args.preset] if args.preset else args.resolution

    output_path = Path(args.output)
    parent = output_path.parent or Path('.')
    # Check output directory and write permission
    if not parent.exists():
        print(f"Output directory {parent} does not exist", file=sys.stderr)
        sys.exit(1)
    if not os.access(parent, os.W_OK):
        fallback = Path.cwd() / output_path.name
        print(f"No write permission in {parent}, saving to current directory instead: {fallback}", file=sys.stderr)
        output_path = fallback
    # Should not point to an existing directory
    if output_path.exists() and output_path.is_dir():
        print(f"Invalid path: {output_path} is a directory", file=sys.stderr)
        sys.exit(1)

    # Load font
    try:
        font = ImageFont.truetype(args.font, size=args.size)
    except Exception as e:
        print(f"Failed to load font {args.font}: {e}", file=sys.stderr)
        sys.exit(1)

    fg = args.color
    bg_color = args.bg

    img = Image.new('RGB', (canvas_w, canvas_h), color=bg_color)
    draw = ImageDraw.Draw(img)

    bbox = draw.textbbox((0, 0), 'A', font=font)
    char_w, char_h = bbox[2] - bbox[0], bbox[3] - bbox[1]

    with tempfile.TemporaryDirectory() as tmpdir:
        cropped = Path(tmpdir) / 'cropped'
        resize_cmd = ['magick', args.input, '-resize', f'{canvas_w}x{canvas_h}^', '-gravity', 'center', '-extent', f'{canvas_w}x{canvas_h}', str(cropped)]
        ascii_cmd = ['ascii-image-converter', '--only-save', '--dimensions', f'{canvas_w // char_w},{canvas_h // char_h}', '--save-txt', tmpdir, str(cropped)]
        if args.braille:
            ascii_cmd += ['--braille', '--dither']

        try:
            subprocess.run(resize_cmd, check=True)
            subprocess.run(ascii_cmd, check=True, stdout=subprocess.DEVNULL)
        except subprocess.CalledProcessError as e:
            print(f"Command execution error: {e}", file=sys.stderr)
            sys.exit(1)

        txt_path = Path(tmpdir) / 'cropped-ascii-art.txt'
        lines = txt_path.read_text().rstrip('\n').split('\n')

    # Draw ASCII art
    for i, line in enumerate(lines):
        draw.text((0, i * char_h), line, font=font, fill=fg)

    # Save image
    try:
        img.save(output_path)
        print(f"Successfully saved at {output_path}")
    except PermissionError as e:
        print(f"Save error: {e}\nMake sure you have write permissions for {output_path}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"File format error: {e}. Make sure the filename ends with .png", file=sys.stderr)
        sys.exit(1)
    except OSError as e:
        print(f"Error saving file {output_path}: {e}", file=sys.stderr)
        sys.exit(1)
