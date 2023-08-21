import os
import tempfile

from gtts import gTTS  # type: ignore
from pydub import AudioSegment  # type: ignore
from tqdm import tqdm

from dualang.split_japanese_text import split_japanese_text


def create_audio(
    sentences,
    transition_sound,
    target_lang,
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
                pbar.write(f"{i:03d} {sentence}")
            pbar.set_postfix_str(f"Processing: {sentence}")
            pbar.update()

            target_text = sentence
            translation_text = "hello world" # TODO

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

    return final_audio

def plaintext_main(args):
    with open(args.input_file, 'r', encoding='utf-8') as file:
        text = file.read()

    output_file = args.output_file or os.path.splitext(args.input)[0] + '.mp3'

    # Split the text into sentences
    sentences = split_japanese_text(text)

    print("Sentences:")
    for i, sentence in enumerate(sentences):
        print(f" {i:03d} {sentence}")

    # Generate TTS audio segments for each sentence
    final_audio = create_audio(
        sentences = sentences,
        transition_sound = args.transition_sound,
        target_lang = "ja",
        interval = 100,
        target_repeat = 3,
        translation_repeat = 1,
        verbose = args.verbose,
    )

    # Save the final audio
    final_audio.export(output_file, format="mp3", tags=None)
