import argparse
from fromtext import fromtext_main
from fromaudio import fromaudio_main

def main():
    # Create a parser object
    parser = argparse.ArgumentParser(description='Create audio from sentences.')
    subparsers = parser.add_subparsers()

    # Create a parser for the "fromtext" command
    parser_fromtext = subparsers.add_parser('fromtext')
    parser_fromtext.set_defaults(func=fromtext_main)

    # Create a parser for the "fromaudio" command
    parser_fromaudio = subparsers.add_parser('fromaudio')
    parser_fromaudio.add_argument('--input-audio', required=True, help='Input audio file to process.')
    parser_fromaudio.add_argument('--subtitle-file', required=True, help='Subtitle file to process.')
    parser_fromaudio.add_argument('--output-file', help='Output audio file. If not provided, it will be derived from the input audio file.')
    parser_fromaudio.add_argument('--transition-sound', help='Transition sound file.')
    parser_fromaudio.add_argument('--repeat-count', type=int, default=1, help='Number of times to repeat the audio.')
    parser_fromaudio.add_argument('--tr-lang', default='en', help='Translation language. Default is "en".')
    parser_fromaudio.add_argument('--verbose', action='store_true', help='Enable verbose output.')
    parser_fromaudio.add_argument('--tr-strategy', default='deepl', help='Translation strategy to use. Options are "deepl" and "fake". Default is "deepl".')
    parser_fromaudio.set_defaults(func=fromaudio_main)

    # Parse the arguments
    args = parser.parse_args()

    # Call the function specified by the "func" attribute of args
    args.func(args)

if __name__ == '__main__':
    main()
