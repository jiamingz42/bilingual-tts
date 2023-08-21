import os

from dualang.split_japanese_text import split_japanese_text
from dualang.command.fromtext import generate_audio_from_sentences


def plaintext_main(args):
    # Read the input text file
    with open(args.input, 'r') as f:
        text = f.read()

    # Split the text into sentences
    sentences = split_japanese_text(text)
    print(sentences)

    # Generate TTS audio segments for each sentence
    audio_segments = generate_audio_from_sentences(sentences, args)

    # Combine the audio segments into a single audio file
    output_file = args.output or os.path.splitext(args.input)[0] + '.mp3'
    combine_audio_segments(audio_segments, output_file)