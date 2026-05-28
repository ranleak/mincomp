# MinComp

**A minimal, lightweight video compressor powered by a custom FFmpeg build.**

MinComp is a Python-based command-line utility designed to compress video files efficiently, especially on lower-end computers with 2 to 4 CPU cores. Instead of relying on a bloated, generic installation of FFmpeg, MinComp compiles its own highly stripped-down version of FFmpeg under the hood. This custom binary is optimized for speed and only includes the essential components needed to convert standard videos into highly compatible H.264/AAC MP4 files.

## Features

- **Custom FFmpeg Engine:** Uses a custom-compiled static binary that strips out unused features for maximum efficiency.
- **Low-End CPU Optimized:** Automatically detects your system's core count and adjusts processing threads to keep your computer responsive during compression.
- **Simple CLI** A straightforward Python interface makes it easy to compress videos without memorizing complex FFmpeg arguments.

## Install MinComp

To install MinComp, you can install via the Github repo with `pip install git+https://github.com/ranleak/mincomp` **OR** you can install via the wheels provided with each release. When you install from Github or via the wheels, a pre-compiled FFmpeg binary is already included with the package.

## Prerequisites

To build the custom FFmpeg binary, you will need some standard build tools installed on your system.

For Ubuntu/Debian-based systems, you can install them via:

```
sudo apt-get update
sudo apt-get install build-essential yasm nasm pkg-config wget git
```

## Local Build & Installation

1. **Clone or download this repository.**
2. **Build the minimal FFmpeg binary.** Run the included shell script from the root of the project:
   ```
   chmod +x build_ffmpeg.sh
   ./build_ffmpeg.sh
   ```
   (_This step will download the source code for x264 and FFmpeg, configure them for minimal size/high speed, compile them, and place the final binary in `mincomp/bin`._)
3. **Install the Python package.** Once the binary is built, install the CLI tool locally:
   ```
   pip install -e .
   ```

## Usage

After installation, the `mincomp` command will be available anywhere in your terminal.

**Basic Compression:**

```
mincomp my_video.mkv compressed_video.mp4
```

**Advanced Compression:**
You can tweak the compression settings using the available flags:

```
mincomp my_video.mkv compressed_video.mp4 --preset fast --crf 26 --audio-bitrate 96k
```

### Options

- `input`: Path to your input video file.
- `output`: Path where the converted MP4 file should be saved.
- `--crf`: Constant Rate Factor (18-51). Lower numbers mean better quality but larger file sizes. Default is `28` (great for high compression).
- `preset`: Encoding speed preset (`ultrafast`, `superfast`, `veryfast`, `faster`, `fast`, `medium`, `slow`). Default is faster.
- `--audio-bitrate`: Set the audio quality (e.g., `96k`, `128k`, `192k`.)

## Development & Code Quality

We use [Ruff](https://github.com/astral-sh/ruff) to format and lint our Python code to keep everything clean, organized, and standardized.

### Setup Development Environment

To install development dependencies (including Ruff):

```
pip install -e ".[dev]"
```

### Run Linter (Checking for errors)

```
ruff check .
```

### Run Formatter (Automatically clean up formatting/imports)

```
ruff format .
```

Made with ❤️ by Ranleak & Alex Scott
