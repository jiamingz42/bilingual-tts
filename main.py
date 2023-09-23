import argparse
from dualang.command.fromtext import fromtext_main
from dualang.command.fromaudio import fromaudio_main
from dualang.command.plaintext import plaintext_main


def main():
    # Create a parser object
    parser = argparse.ArgumentParser(description="Create audio from sentences.")
    subparsers = parser.add_subparsers()

    # Create a parser for the "fromtext" command
    parser_fromtext = subparsers.add_parser("fromtext")
    parser_fromtext.set_defaults(func=fromtext_main)
    _add_fromtext_arguments(parser_fromtext)

    # Create a parser for the "fromaudio" command
    parser_fromaudio = subparsers.add_parser("fromaudio")
    _add_fromaudio_arguments(parser_fromaudio)

    # Create a parser for the "plaintext" command
    parser_plaintext = subparsers.add_parser("plaintext")
    _add_plaintext_arguments(parser_plaintext)

    # Create a parser for the "condense-audio" command
    parser_condense_audio = subparsers.add_parser("condense-audio")
    _add_condense_audio_arguments(parser_condense_audio)

    # Parse the arguments
    args = parser.parse_args()

    # Check if the "func" attribute is set
    if hasattr(args, "func"):
        # Call the function specified by the "func" attribute of args
        args.func(args)
    else:
        # Print usage message and exit
        parser.print_usage()
        exit(1)

def _add_condense_audio_arguments(parser_condense_audio):
    parser_condense_audio.add_argument(
        "-i", "--input", required=True, help="Input audio file."
    )
    parser_condense_audio.add_argument(
        "-o", "--output", help="Output audio file. If not provided, it will be derived from the input file."
    )
    parser_condense_audio.add_argument(
        "--padding",
        type=int,
        help="Padding in milliseconds between audio segments. If not provided, it will default to 0.",
    )
    parser_condense_audio.set_defaults(func=condense_audio_main)  # Placeholder function

def _add_plaintext_arguments(parser_plaintext):
    parser_plaintext.add_argument(
        "-i", "--input-file", required=True, help="Input plaintext file."
    )
    parser_plaintext.add_argument(
        "-o", "--output-file", required=True, help="Output file."
    )
    parser_plaintext.add_argument(
        "--transition-sound", required=True, help="Transition sound file."
    )
    parser_plaintext.add_argument(
        "--tr-strategy",
        default="deepl",
        help='Translation strategy to use. Options are "deepl" and "fake". Default is "deepl".',
    )
    parser_plaintext.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output."
    )
    parser_plaintext.set_defaults(func=plaintext_main)


def _add_fromtext_arguments(parser_fromtext):
    parser_fromtext.add_argument(
        "-i", "--input", required=True, help="Input JSON file with sentences."
    )
    parser_fromtext.add_argument(
        "-o",
        "--output",
        help="Output audio file. If not provided, it will be derived from the input file.",
    )
    parser_fromtext.add_argument(
        "--transition-sound", required=True, help="Transition sound file."
    )
    parser_fromtext.add_argument(
        "--target-lang", required=True, help="Target language for text to speech."
    )
    parser_fromtext.add_argument(
        "--target-lang-key",
        help="Key for target language in the input JSON. If not provided, it will be the same as target-lang.",
    )
    parser_fromtext.add_argument(
        "--tr-lang", required=True, help="Translation language for text to speech."
    )
    parser_fromtext.add_argument(
        "--tr-lang-key",
        help="Key for translation language in the input JSON. If not provided, it will be the same as tr-lang.",
    )
    parser_fromtext.add_argument(
        "--interval",
        type=int,
        default=1000,
        help="Interval in milliseconds between repetitions. Default is 1000.",
    )
    parser_fromtext.add_argument(
        "--target-repeat",
        type=int,
        default=1,
        help="Number of times to repeat the target language. Default is 1.",
    )
    parser_fromtext.add_argument(
        "--translation-repeat",
        type=int,
        default=1,
        help="Number of times to repeat the translation. Default is 1.",
    )
    parser_fromtext.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output."
    )
    parser_fromtext.set_defaults(func=fromtext_main)


def _add_fromaudio_arguments(parser_fromaudio):
    parser_fromaudio.add_argument(
        "-i", "--input-audio", required=True, help="Input audio file to process."
    )
    parser_fromaudio.add_argument(
        "-s",
        "--subtitle-file",
        help="Subtitle file to process. Supports .srt, .ass and .vtt formats. If not provided, it will be derived from the input audio file.",
    )
    parser_fromaudio.add_argument(
        "-o",
        "--output-file",
        help="Output audio file. If not provided, it will be derived from the input audio file.",
    )
    parser_fromaudio.add_argument(
        "--transition-sound", required=True, help="Transition sound file."
    )
    parser_fromaudio.add_argument(
        "--repeat-count",
        type=int,
        default=1,
        help="Number of times to repeat the audio.",
    )
    parser_fromaudio.add_argument(
        "--tr-lang", default="EN-US", help='Translation language. Default is "en".'
    )
    parser_fromaudio.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output."
    )
    parser_fromaudio.add_argument(
        "--tr-strategy",
        default="deepl",
        help='Translation strategy to use. Options are "deepl" and "fake". Default is "deepl".',
    )
    parser_fromaudio.add_argument(
        "--limit",
        type=int,
        help="Number of subtitles to process. If not provided, all subtitles will be processed.",
    )
    parser_fromaudio.add_argument(
        "--offset",
        type=int,
        default=0,
        help="Start from index-offset subtitles. If not provided, it will start from the beginning.",
    )
    parser_fromaudio.add_argument(
        "--silent-interval",
        type=int,
        default=100,
        help="Silent interval in milliseconds. If not provided, it will default to 100 milliseconds.",
    )
    parser_fromaudio.set_defaults(func=fromaudio_main)


if __name__ == "__main__":
    main()
