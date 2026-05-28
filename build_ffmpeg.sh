# Compiles a minimal, static FFmpeg binary optimized for speed and low-end CPUs.
# Requires: build-essential, yasm, nasm, wget, git, pkg-config

set -e

# Set up directories
ROOT_DIR=$(pwd)
BUILD_DIR="$ROOT_DIR/build_tmp"
BIN_DIR="$ROOT_DIR/mincomp/bin"
PREFIX="$BUILD_DIR/workspace"

mkdir -p "$BUILD_DIR"
mkdir -p "$BIN_DIR"
mkdir -p "$PREFIX"

export PATH="$PREFIX/bin:$PATH"
export PKG_CONFIG_PATH="$PREFIX/lib/pkgconfig"

echo "=== Building static libx264 ==="
cd "$BUILD_DIR"
if [ ! -d "x264" ]; then
    git clone --depth 1 https://code.videolan.org/videolan/x264.git
fi
cd x264
./configure --prefix="$PREFIX" --enable-static --disable-opencl --disable-cli --disable-shared
make -j$(nproc)
make install

echo "=== Downloading FFmpeg ==="
cd "$BUILD_DIR"
FFMPEG_VERSION="6.1.1"
if [ ! -f "ffmpeg-${FFMPEG_VERSION}.tar.bz2" ]; then
    wget "https://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.bz2"
    tar -xf "ffmpeg-${FFMPEG_VERSION}.tar.bz2"
fi
cd "ffmpeg-${FFMPEG_VERSION}"

echo "=== Configuring Minimal FFmpeg ==="
# We disable EVERYTHING, then selectively enable ONLY what we need for standard MP4 video compression.
# CFLAGS are optimized for speed on low-end hardware (-O3, loop vectorization).
./configure \
    --prefix="$PREFIX" \
    --pkg-config-flags="--static" \
    --extra-cflags="-I$PREFIX/include -O3 -fno-math-errno -fno-signed-zeros -ftree-vectorize" \
    --extra-ldflags="-L$PREFIX/lib -static" \
    --extra-libs="-lpthread -lm" \
    --disable-debug \
    --disable-doc \
    --disable-ffplay \
    --disable-ffprobe \
    --disable-network \
    --disable-everything \
    --enable-gpl \
    --enable-nonfree \
    --enable-libx264 \
    --enable-pthreads \
    --enable-small \
    --enable-protocol=file \
    --enable-demuxer=mov,mp4,m4a,3gp,3g2,mj2,avi,matroska,webm,m4v \
    --enable-muxer=mp4 \
    --enable-parser=h264,aac,hevc \
    --enable-decoder=h264,hevc,aac,mp3,mpeg4 \
    --enable-encoder=libx264,aac \
    --enable-filter=scale,aresample,crop,format

echo "=== Compiling FFmpeg ==="
make -j$(nproc)

echo "=== Copying binary to package ==="
cp ffmpeg "$BIN_DIR/ffmpeg"
chmod +x "$BIN_DIR/ffmpeg"

echo "Success! Minimal FFmpeg binary placed in $BIN_DIR/ffmpeg"
echo "You can safely delete the build_tmp directory."