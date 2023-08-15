import argparse
import json
import tempfile
from gtts import gTTS
from pydub import AudioSegment
from tqdm import tqdm
import pydub
import os
import pysrt
import deepl

def fake_translate_func(text, target_lang):
    return "Hello world"

def create_audio_from_audio(
    input_audio,
    subtitle_file,
    output_file,
    transition_sound,
    repeat_count,
    tr_lang,
    verbose,
    translate_func,
):
    # Check if the DEEPL_API_KEY environment variable is set
    if 'DEEPL_API_KEY' not in os.environ:
        print("Error: The DEEPL_API_KEY environment variable is not set. Please set it to your DeepL API key.")
        exit(1)
    # Load the input audio file using AudioSegment.from_file
    input_audio = AudioSegment.from_file(input_audio)

    # Load the subtitle file and parse it into a list of sentences
    subtitle_data = pysrt.open(subtitle_file)
    sentences = [subtitle.text for subtitle in subtitle_data]

    # Create a temporary directory to store the audio segments
    temp_dir = tempfile.mkdtemp()

    # Create an empty list to store the audio segments
    audio_segments = []

    # Iterate over the sentences in the subtitle file
    for sentence in tqdm(sentences, desc='Processing sentences', disable=not verbose):
        # Translate the sentence using the provided translate function
        translation = translate_func(sentence, target_lang=tr_lang)

        # Convert the translation into speech using gTTS
        tts = gTTS(text=translation, lang=tr_lang)

        # Save the translated speech to a temporary file
        tts_file = os.path.join(temp_dir, f'{sentence}.mp3')
        tts.save(tts_file)

        # Load the translated speech as an audio segment
        tts_audio_segment = AudioSegment.from_file(tts_file)

        # Append the translated speech to the list of audio segments
        audio_segments.append(tts_audio_segment)

    # Concatenate the audio segments into a single audio file
    final_audio = pydub.AudioSegment.empty()
    for audio_segment in audio_segments:
        final_audio += audio_segment

    # Append the transition sound to the final audio
    transition_sound = AudioSegment.from_file(transition_sound)
    final_audio += transition_sound

    # Save the final audio to the output file
    final_audio.export(output_file, format='mp3')

def fromaudio_main(args):
    if args.tr_strategy == "deepl":
        translate_func = deepl.translate_text
    else:
        translate_func = fake_translate_func

    # If output file is not provided, derive it from the input audio file
    if args.output_file is None:
        args.output_file = args.input_audio.rsplit('.', 1)[0] + '.mp3'

    create_audio_from_audio(
        args.input_audio,
        args.subtitle_file,
        args.output_file,
        args.transition_sound,
        args.repeat_count,
        args.tr_lang,
        args.verbose,
        translate_func=translate_func,
    )
