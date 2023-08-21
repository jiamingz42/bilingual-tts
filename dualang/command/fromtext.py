from gtts import gTTS  # type: ignore
from pydub import AudioSegment  # type: ignore
from tqdm import tqdm

import json
import tempfile


def create_audio(
    sentences,
    output_file,
    transition_sound,
    target_lang,
    target_key,
    tr_lang,
    tr_key,
    interval,
    target_repeat,
    translation_repeat,
    verbose,
):
    final_audio = AudioSegment.silent(duration=0)

    # Load the transition sound
    transition_sound = AudioSegment.from_file(transition_sound)

    # Iterate through the sentences with a progress bar and print the currently processing sentence
    with tqdm(total=len(sentences)) as pbar:
        for i, sentence in enumerate(sentences, 1):
            if verbose:
                pbar.write(f"{i:03d} {sentence[target_key]}")
            pbar.set_postfix_str(f"Processing: {sentence[target_key]}")
            pbar.update()

            target_text = sentence[target_key]
            translation_text = sentence[tr_key]

            # Convert target language text to speech
            target_tts = gTTS(text=target_text, lang=target_lang)
            with tempfile.NamedTemporaryFile(delete=False) as target_file:
                target_tts.save(target_file.name)
                target_audio = AudioSegment.from_mp3(target_file.name)

            # Convert translation text to speech
            translation_tts = gTTS(text=translation_text, lang="en")
            with tempfile.NamedTemporaryFile(delete=False) as translation_file:
                translation_tts.save(translation_file.name)
                translation_audio = AudioSegment.from_mp3(translation_file.name)

            # Repeat and combine the audio with interval between repetitions
            combined_audio = (
                target_audio + AudioSegment.silent(duration=interval)
            ) * target_repeat
            combined_audio += (
                translation_audio * translation_repeat
                + AudioSegment.silent(duration=interval)
            )
            combined_audio += target_audio

            # Add to the final audio with a "ding" sound
            final_audio += combined_audio + transition_sound

    # Save the final audio
    final_audio.export(output_file, format="mp3")


def fromtext_main(args):
    # Validate the input file
    try:
        with open(args.input) as f:
            sentences = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: {args.input} is not a valid JSON file.")
        exit(1)

    # If output file is not provided, derive it from the input file
    if args.output is None:
        args.output = args.input.rsplit(".", 1)[0] + ".mp3"

    # Validate the output file
    if not args.output.endswith(".mp3"):
        print(f"Error: {args.output} is not a valid MP3 file.")
        exit(1)

    # If target-lang-key or tr-lang-key are not provided, use the same value from target-lang or tr-lang
    target_lang_key = args.target_lang_key if args.target_lang_key else args.target_lang
    tr_lang_key = args.tr_lang_key if args.tr_lang_key else args.tr_lang

    create_audio(
        sentences,
        args.output,
        args.transition_sound,
        args.target_lang,
        target_lang_key,
        args.tr_lang,
        tr_lang_key,
        args.interval,
        args.target_repeat,
        args.translation_repeat,
        args.verbose,
    )
