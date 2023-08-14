from gtts import gTTS
from pydub import AudioSegment

import argparse
import json
import tempfile

def create_audio(sentences, output_file, target_key="jp", translation_key="en", interval=1000, target_repeat=3, translation_repeat=1):
    final_audio = AudioSegment.silent(duration=0)

    # Load the "ding" sound
    ding_sound = AudioSegment.from_file("ding.wav")

    # Iterate through the sentences
    for sentence in sentences:
        target_text = sentence[target_key]
        translation_text = sentence[translation_key]

        # Convert target language text to speech
        target_tts = gTTS(text=target_text, lang="ja")
        with tempfile.NamedTemporaryFile(delete=False) as target_file:
            target_tts.save(target_file.name)
            target_audio = AudioSegment.from_mp3(target_file.name)

        # Convert translation text to speech
        translation_tts = gTTS(text=translation_text, lang="en")
        with tempfile.NamedTemporaryFile(delete=False) as translation_file:
            translation_tts.save(translation_file.name)
            translation_audio = AudioSegment.from_mp3(translation_file.name)

        # Repeat and combine the audio
        combined_audio = target_audio * target_repeat + AudioSegment.silent(duration=interval)
        combined_audio += translation_audio * translation_repeat + AudioSegment.silent(duration=interval)
        combined_audio += target_audio

        # Add to the final audio with a "ding" sound
        final_audio += combined_audio + ding_sound

    # Save the final audio
    final_audio.export(output_file, format="mp3")

def main():
    # Create a parser object
    parser = argparse.ArgumentParser(description='Create audio from sentences.')
    parser.add_argument('-i', '--input', type=str, required=True, help='Input JSON file with sentences')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output MP3 file')

    # Parse the arguments
    args = parser.parse_args()

    # Validate the input file
    try:
        with open(args.input) as f:
            sentences = json.load(f)
    except json.JSONDecodeError:
        print(f"Error: {args.input} is not a valid JSON file.")
        exit(1)

    # Validate the output file
    if not args.output.endswith('.mp3'):
        print(f"Error: {args.output} is not a valid MP3 file.")
        exit(1)

    create_audio(sentences, args.output)

if __name__ == '__main__':
    main()
