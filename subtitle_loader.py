import os
import pysrt  # type: ignore
import pyass  # type: ignore

def load_subtitle_file(subtitle_file: str):
    # Validate if the subtitle file exists
    if not os.path.isfile(subtitle_file):
        print(f"Error: Subtitle file {subtitle_file} does not exist.")
        exit(1)

    # Load the subtitle file and parse it into a list of sentences
    if subtitle_file.endswith('.srt'):
        subtitle_data = pysrt.open(subtitle_file)
    elif subtitle_file.endswith('.ass'):
        with open(subtitle_file, encoding="utf_8_sig") as f:
            subtitle_data = pyass.load(f).events
    else:
        print(f"Error: Unsupported subtitle file format. Only .srt and .ass are supported.")
        exit(1)
    print("Loaded subtitle file")
    if (len(subtitle_data) == 0):
        print(f"Error: Subtitle file is empty.")
        exit(1)

    return subtitle_data
