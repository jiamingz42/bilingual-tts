"""
This module provides a function to generate bilingual TTS from audio and
subtitle files. The function takes an input audio file, a subtitle file, and
other optional parameters such as a transition sound file, a translation
strategy, and a translation language. The function extracts audio segments from
the input audio file based on the start and end times in the subtitle file, and
generates a TTS translation of the subtitle text using the specified translation
strategy and language. The TTS translations are concatenated with the original
audio segments and a transition sound to create a final bilingual TTS audio
file.

Functions:
- create_audio_from_audio: Generates bilingual TTS from audio and subtitle files.
"""
import tempfile
import os
import hashlib

from typing import Callable, Optional

import pydub  # type: ignore
import deepl  # type: ignore

from gtts import gTTS  # type: ignore
from pydub import AudioSegment  # type: ignore
from tqdm import tqdm

from dualang.subtitle_loader import load_subtitle_file

def fake_translate_func(text: str, target_lang: str) -> str:
    """
    A fake translation function that always returns "Hello world".

    Args:
        text (str): The text to be translated.
        target_lang (str): The target language for the translation.

    Returns:
        str: The translated text.
    """
    return f"[{target_lang}] Hello world"


def create_audio_from_audio(
    input_audio: str,
    subtitle_data: list,
    output_file: str,
    transition_sound: str,
    repeat_count: int,
    tr_lang: str,
    verbose: bool,
    translate_func: Callable[[str, str], str],
    interval: int = 500,
    limit: Optional[int] = None,
) -> None:
    if verbose:
        for i, subtitle in enumerate(subtitle_data):
            print(f"{i:03d} {subtitle.text}")

    # Load the input audio file using AudioSegment.from_file
    input_audio = AudioSegment.from_file(input_audio)
    print("Loaded input audio")

    # Create a temporary directory to store the audio segments
    temp_dir = tempfile.mkdtemp()

    # Create an empty list to store the audio segments
    audio_segments = []

    # Iterate over the sentences in the subtitle file
    for subtitle in tqdm(subtitle_data, desc="Processing sentences"):
        if not subtitle.text:
            continue

        # Extract the start and end times from the subtitle
        # Assuming subtitle.start and subtitle.end are in milliseconds
        start_time = subtitle.start / 1000  # Convert from milliseconds to seconds
        end_time = subtitle.end / 1000  # Convert from milliseconds to seconds

        # Extract the corresponding audio segment from the input audio
        audio_segment = input_audio[
            start_time * 1000 : end_time * 1000
        ]  # Convert from seconds to milliseconds

        # Repeat the audio segment three times with a silent interval in between
        repeated_audio_segment = audio_segment + AudioSegment.silent(
            duration=1000
        )  # 1 second silent interval
        repeated_audio_segment = repeated_audio_segment * 3

        # Translate the subtitle text using the provided translate function
        translation = translate_func(subtitle.text, target_lang=tr_lang)

        # Convert the translation into speech using gTTS
        # Use the text attribute of the TextResult object
        tts = gTTS(text=translation.text, lang=tr_lang)

        # Generate a hash of the subtitle text
        subtitle_hash = hashlib.md5(subtitle.text.encode()).hexdigest()

        # Save the translated speech to a temporary file using the hash as the filename
        tts_file = os.path.join(temp_dir, f"{subtitle_hash}.mp3")
        tts.save(tts_file)

        # Load the translated speech as an audio segment
        tts_audio_segment = AudioSegment.from_file(tts_file)

        # Append the TTS translation to the repeated audio segments with a silent interval
        repeated_audio_segment += (
            AudioSegment.silent(duration=interval) + tts_audio_segment
        )

        # Append the original extracted audio segment one more time with a silent interval
        repeated_audio_segment += AudioSegment.silent(duration=interval) + audio_segment

        # Append the repeated audio segment to the list of audio segments
        audio_segments.append(repeated_audio_segment)

    # Load the transition sound
    transition_sound = AudioSegment.from_file(transition_sound)

    # Concatenate the audio segments into a single audio file
    final_audio = pydub.AudioSegment.empty()
    for audio_segment in tqdm(audio_segments, desc="Processing audio segments"):
        # Append the transition sound to each audio segment
        if audio_segment.channels > 1:
            import ipdb
            ipdb.set_trace()
            audio_segment = audio_segment.set_channels(3)
        final_audio += audio_segment + transition_sound

    # Save the final audio to the output file
    final_audio.export(output_file, format="mp3")


def fromaudio_main(args):
    print("Generating bilingual TTS from audio ...")

    if "DEEPL_API_KEY" not in os.environ:
        print(
            "Error: The DEEPL_API_KEY environment variable is not set. Please set it to your DeepL API key."
        )
        exit(1)

    translate_func: Callable[[str, str], str]
    if args.tr_strategy == "deepl":
        translator = deepl.Translator(os.environ["DEEPL_API_KEY"])
        translate_func = translator.translate_text
    elif args.tr_strategy == "fake":
        translate_func = fake_translate_func
    else:
        print(f"Error: Unsupported translation strategy {args.tr_strategy}.")
        exit(1)


    # If subtitle file is not provided, derive it from the input audio file
    if args.subtitle_file is None:
        args.subtitle_file = args.input_audio.rsplit(".", 1)[0] + ".srt"

    # Validate if the audio file and transition sound file exist
    if not os.path.isfile(args.input_audio):
        print(f"Error: Audio file {args.input_audio} does not exist.")
        exit(1)

    if not os.path.isfile(args.transition_sound):
        print(f"Error: Transition sound file {args.transition_sound} does not exist.")
        exit(1)

    # If output file is not provided, derive it from the input audio file
    args.output_file = get_output_file_name(args.input_audio, args.output_file)

    # Load the subtitle file and parse it into a list of sentences
    subtitle_data = load_subtitle_file(args.subtitle_file)
    subtitle_data = subtitle_data[args.offset:]
    if args.limit is not None:
        subtitle_data = subtitle_data[: args.limit]

    create_audio_from_audio(
        args.input_audio,
        subtitle_data,
        args.output_file,
        args.transition_sound,
        args.repeat_count,
        args.tr_lang,
        args.verbose,
        translate_func=translate_func,
        limit=args.limit,
    )


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
