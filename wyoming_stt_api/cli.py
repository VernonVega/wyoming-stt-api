import argparse
import sys
from pathlib import Path

from wyoming_stt_api.dependencies import ats_client


def main():
    parser = argparse.ArgumentParser(description="Transcribe audio file")
    parser.add_argument("file_path", type=Path, help="Path to audio file")

    args = parser.parse_args()

    if not args.file_path.exists():
        print(f"Error: File not found: {args.file_path}")
        sys.exit(1)

    with open(args.file_path, "rb") as audio_file:
        ats_client.speech_to_text(audio_file)


if __name__ == "__main__":
    main()
