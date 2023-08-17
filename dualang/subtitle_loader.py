import os
import pyass
import pysrt
import webvtt

from dataclasses import dataclass
from typing import List


@dataclass
class Subtitle:
    start: int  # milleseconds
    end: int  # milliseconds
    text: str


def load_subtitle_file(subtitle_file: str) -> List[Subtitle]:
    # Validate if the subtitle file exists
    if not os.path.isfile(subtitle_file):
        print(f"Error: Subtitle file {subtitle_file} does not exist.")
        exit(1)

    # Load the subtitle file and parse it into a list of Subtitle objects
    if subtitle_file.endswith(".srt"):
        subtitle_data = pysrt.open(subtitle_file)
        subtitles = [
            Subtitle(s.start.ordinal, s.end.ordinal, s.text) for s in subtitle_data
        ]
    elif subtitle_file.endswith(".ass"):
        with open(subtitle_file, encoding="utf_8_sig") as f:
            subtitle_data = pyass.load(f).events
        subtitles = [
            Subtitle(e.start.total_milliseconds(), e.end.total_milliseconds(), e.text)
            for e in subtitle_data
        ]
    elif subtitle_file.endswith(".vtt"):
        subtitle_data = webvtt.read(subtitle_file)
        subtitles = [
            Subtitle(s.start_in_seconds * 1000, s.end_in_seconds * 1000, s.text)
            for s in subtitle_data
        ]
    else:
        print(
            f"Error: Unsupported subtitle file format. Only .srt, .ass and .vtt are supported."
        )
        exit(1)
    print(f"Loaded subtitle file: {len(subtitles)} lines")
    if len(subtitles) == 0:
        print(f"Error: Subtitle file is empty.")
        exit(1)

    return subtitles
