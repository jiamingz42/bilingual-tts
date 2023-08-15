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
    parser_fromaudio.add_argument('input_audio', help='Input audio file to process.')
    parser_fromaudio.add_argument('--tr-strategy', default='deepl', help='Translation strategy to use. Options are "deepl" and "fake". Default is "deepl".')
    parser_fromaudio.set_defaults(func=fromaudio_main)

    # Parse the arguments
    args = parser.parse_args()

    # Call the function specified by the "func" attribute of args
    args.func(args)

if __name__ == '__main__':
    main()
