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
import ffmpeg
from pydub import playback

from typing import Callable, Optional

import pydub  # type: ignore

from gtts import gTTS  # type: ignore
from pydub import AudioSegment  # type: ignore
from tqdm import tqdm

from dualang.subtitle_loader import load_subtitle_file
from dualang.audio_loader import load_audio_segment
from dualang.args_helper import get_subtitle_file_name, get_output_file_name


def create_audio_from_audio(
    input_audio: str,
    subtitle_data: list,
    output_file: str,
    transition_sound: str,
    tr_lang: str,
    verbose: bool,
    translate_func: Callable[[str, str], str],
    interval: int = 100,
) -> None:
    if verbose:
        for i, subtitle in enumerate(subtitle_data):
            print(f"{i:03d} {subtitle.text}")

    input_audio = load_audio_segment(input_audio, verbose)

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
        start_time = subtitle.start
        end_time = subtitle.end

        # Extract the corresponding audio segment from the input audio
        audio_segment = input_audio[start_time:end_time]

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
            audio_segment = audio_segment.set_channels(1)
        final_audio += audio_segment + transition_sound

    # Repeat the original at the end
    final_audio += input_audio

    # Save the final audio to the output file
    final_audio.export(output_file, format="mp3")


def fromaudio_main(args):
    print("Generating bilingual TTS from audio ...")

    if "DEEPL_API_KEY" not in os.environ:
        print(
            "Error: The DEEPL_API_KEY environment variable is not set. Please set it to your DeepL API key."
        )
        exit(1)

    from dualang.translator import build_translator, TranslationStrategy

    try:
        translate_func = build_translator(TranslationStrategy(args.tr_strategy))
    except ValueError as e:
        print(str(e))
        exit(1)

    # If subtitle file is not provided, derive it from the input audio file
    subtitle_file = get_subtitle_file_name(args.input_audio, args.subtitle_file)
    if subtitle_file is None:
        print(f"Error: No subtitle file found for audio file {args.input_audio}.")
        exit(1)

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
    subtitle_data = load_subtitle_file(subtitle_file)
    subtitle_data = subtitle_data[args.offset :]
    if args.limit is not None:
        subtitle_data = subtitle_data[: args.limit]

    create_audio_from_audio(
        args.input_audio,
        subtitle_data,
        args.output_file,
        args.transition_sound,
        args.tr_lang,
        args.verbose,
        translate_func=translate_func,
        interval=args.silent_interval,
    )
