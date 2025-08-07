# ascii-img-render

A command-line utility to convert raster images into ASCII art rendered as PNG images, with support for custom resolutions, fonts, and color schemes.

---

## Table of Contents

* [Features](#features)
* [Requirements](#requirements)
* [Installation](#installation)
* [Usage](#usage)
* [Options](#options)
* [Examples](#examples)
* [License](#license)

---

## Features

* Convert any input image to ASCII art and save as a PNG
* Fit output to preset resolutions (`1080p`, `720p`, `4k`) or custom dimensions (`WIDTHxHEIGHT`)
* Customize font (TrueType), size, text and background colors
* Optional Braille rendering with dithering for increased detail

---

## Requirements

Tested on Arch Linux. Ensure you have the following packages installed:

```bash
# Core dependencies
sudo pacman -S --needed python python-pillow imagemagick

# ASCII conversion tool
# (from AUR)
yay -S ascii-image-converter

# Terminus TTF font
# (provides a clean monospace font for ASCII art)
yay -S terminus-font-ttf
```

> **Note:** If you use a different font, install its TTF package or provide the path to a custom `.ttf` file.

---

## Installation

1. Clone the repository:

   ```bash
    git clone https://github.com/ashi0-a/ascii-img-renderer.git
    cd ascii-img-render
   ```

2. Make the script executable:

    ```bash
    chmod +x ascii-img-render.py
    ```

3. Verify dependencies are installed (see [Requirements](#requirements)).

---

## Usage

```bash
./ascii-img-render.py -i <input.png> (-p <preset> | -r <WIDTHxHEIGHT>) [options] -o <output.png>
```

To display full help:

```bash
./ascii-img-render.py --help
```

---

## Options

| Flag               | Description                                                                 | Default           |
| ------------------ | --------------------------------------------------------------------------- | ----------------- |
| `-i, --input`      | Path to the input image (PNG, JPEG, etc.) (required)                        | —                 |
| `-p, --preset`     | Resolution preset: `1080p` (1920×1080), `720p` (1280×720), `4k` (3840×2160) | —                 |
| `-r, --resolution` | Custom resolution: `WIDTHxHEIGHT` (e.g., `1920x1080`)                       | —                 |
| `-f, --font`       | Path to TrueType font file (`.ttf`)                                         | `TerminusTTF.ttf` |
| `-s, --size`       | Font size in points                                                         | `12`              |
| `-c, --color`      | Text color in hex (`RRGGBB` or `RGB`, without `#`)                          | `ffffff` (white)  |
| `-B, --bg`         | Background color in hex (`RRGGBB` or `RGB`, without `#`)                    | `000000` (black)  |
| `-b, --braille`    | Enable Braille font rendering and dithering                                 | Off               |
| `-o, --output`     | Path to save the output PNG file (required)                                 | —                 |

---

## Examples

1. **Convert to 1080p using default Terminus font**

   ```bash
   ./ascii-img-render.py -i photo.jpg -p 1080p -o ascii_photo.png
   ```

2. **Custom 1280×720 resolution with red text on black background**

   ```bash
   ./ascii-img-render.py -i photo.jpg -r 1280x720 -s 24 -c ff0000 -B 000000 -o red_ascii.png
   ```

3. **Braille rendering with dithering at 720p**

   ```bash
   ./ascii-img-render.py -i photo.jpg -p 720p -b -o braille_ascii.png
   ```

---
