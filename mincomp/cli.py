import argparse
import subprocess
import os
import sys
import multiprocessing
from pathlib import Path

def get_ffmpeg_path():
    """Locates the bundled minimal FFmpeg binary."""
    base_dir = Path(__file__).parent
    binary_name = "ffmpeg.exe" if os.name == 'nt' else "ffmpeg"
    binary_path = base_dir / "bin" / binary_name
    return binary_path

def calculate_optimal_threads():
    """
    Calculates the optimal number of threads for low-end CPUs (2-4 cores).
    Leaves 1 core free for system stability if >2 cores exist.
    """
    try:
        cores = multiprocessing.cpu_count()
    except NotImplementedError:
        cores = 2

    if cores <= 2:
        return cores # On dual-core or less, use everything available
    else:
        return cores - 1 # On 3-4+ cores, leave one core free for OS background tasks

def compress_video(input_path, output_path, crf=28, preset="faster", audio_bitrate="128k"):
    """
    Executes the compression using the bundled FFmpeg binary.
    """
    ffmpeg_path = get_ffmpeg_path()
    
    if not ffmpeg_path.exists():
        print(f"[!] Error: Custom FFmpeg binary not found at {ffmpeg_path}")
        print("[!] Please run 'bash build_ffmpeg.sh' first to compile the binary.")
        sys.exit(1)

    threads = calculate_optimal_threads()
    
    # FFmpeg command strictly tailored to the encoders we enabled in the build script
    cmd = [
        str(ffmpeg_path),
        "-y",                  # Overwrite output file
        "-i", str(input_path), # Input file
        "-c:v", "libx264",     # Use x264 encoder
        "-crf", str(crf),      # Constant Rate Factor (lower is better quality, 28 is good for small size)
        "-preset", preset,     # Encoder preset
        "-c:a", "aac",         # AAC audio encoder
        "-b:a", audio_bitrate, # Audio bitrate
        "-threads", str(threads), # Optimized threading
        str(output_path)       # Output file
    ]

    print(f"--- MinComp: Video Compression ---")
    print(f"Input   : {input_path}")
    print(f"Output  : {output_path}")
    print(f"Threads : {threads} (Optimized for low-end CPU)")
    print(f"CRF     : {crf} | Preset: {preset}")
    print("-" * 34)

    try:
        # Run FFmpeg, mapping its standard output and error to the console
        subprocess.run(cmd, check=True)
        print("\n[+] Compression completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"\n[!] Compression failed with error code {e.returncode}")
        sys.exit(e.returncode)
    except KeyboardInterrupt:
        print("\n[!] Compression cancelled by user.")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="MinComp - Minimal Video Compressor for low-end CPUs.")
    parser.add_argument("input", help="Path to the input video file")
    parser.add_argument("output", help="Path to the output MP4 file")
    
    # Defaulting to 28 for CRF (high compression) and 'faster' preset for weak CPUs
    parser.add_argument("--crf", type=int, default=28, 
                        help="Constant Rate Factor (18-51). Lower is better quality. Default: 28")
    parser.add_argument("--preset", type=str, default="faster", 
                        choices=["ultrafast", "superfast", "veryfast", "faster", "fast", "medium", "slow"],
                        help="Encoding speed preset. Default: faster")
    parser.add_argument("--audio-bitrate", type=str, default="128k", 
                        help="Audio bitrate (e.g. 96k, 128k). Default: 128k")

    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"[!] Error: Input file '{args.input}' does not exist.")
        sys.exit(1)

    compress_video(
        input_path=input_path,
        output_path=args.output,
        crf=args.crf,
        preset=args.preset,
        audio_bitrate=args.audio_bitrate
    )

if __name__ == "__main__":
    main()