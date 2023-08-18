import os
from typing import Optional

def get_subtitle_file_name(input_audio: str, subtitle_file: Optional[str]) -> Optional[str]:
    """
    Returns the subtitle file name for the given input audio file and subtitle file path.
    If the subtitle file path is not provided, it is derived from the input audio file path.

    Args:
    - input_audio (str): Path to the input audio file.
    - subtitle_file (Optional[str]): Path to the subtitle file. If not provided, it is derived from the input audio file path.

    Returns:
    - subtitle_file (str): Path to the subtitle file.
    """
    if subtitle_file:
        return subtitle_file

    base_name = input_audio.rsplit(".", 1)[0]
    for ext in [".srt", ".ass", ".vtt"]:
        subtitle_file = base_name + ext
        if os.path.isfile(subtitle_file):
            return subtitle_file

    for prefix in ["", ".ja", ".en", ".fr", ".de", ".es", ".it", ".nl", ".pl", ".pt", ".ru", ".zh"]:
        for ext in [".srt", ".ass", ".vtt"]:
            subtitle_file = base_name + prefix + ext
            if os.path.isfile(subtitle_file):
                return subtitle_file

    print("Fail to found subtitle file")
    return None

def get_output_file_name(input_audio: str, output_file: Optional[str]) -> str:
    """
    Returns the output file name for the given input audio file and output file path.
    If the output file path is not provided, it is generated based on the input audio file path.
    If the output file path is a directory, the output file is generated in that directory with the same name as the input audio file.
    If the output file path is the same as the input audio file, the output file is generated with a '_out' suffix.

    Args:
    - input_audio (str): Path to the input audio file.
    - output_file (Optional[str]): Path to the output file. If not provided, it is generated based on the input audio file path.

    Returns:
    - output_file (str): Path to the output file.
    """
    if output_file is None:
        output_file = os.path.join(
            os.path.dirname(input_audio),
            os.path.basename(input_audio).rsplit(".", 1)[0] + ".mp3",
        )
        if output_file == input_audio:
            output_file = output_file.rsplit(".", 1)[0] + "_out.mp3"
    elif os.path.isdir(output_file):
        output_file = os.path.join(
            output_file, os.path.basename(input_audio).rsplit(".", 1)[0] + ".mp3"
        )
        if output_file == input_audio:
            output_file = output_file.rsplit(".", 1)[0] + "_out.mp3"
    return output_file
