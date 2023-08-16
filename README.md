# Overview

This script is used to create an audio file from a set of sentences. The sentences are provided in a JSON file. The script uses Google Text-to-Speech to convert the sentences into speech. The speech is then combined with a transition sound to create the final audio file. The script allows the user to specify the target language, the translation language, the interval between repetitions, and the number of times to repeat the target language and the translation.

# Type Checking

This project uses type hinting to help catch certain types of errors. You can use `mypy` to check the types in this project. Install `mypy` using pip:

```bash
pip install mypy
```

Then run `mypy` on the project:

```bash
mypy .
```

This will check all files in the current directory and any subdirectories. If there are any type inconsistencies, `mypy` will print them to the console.

# Development

## Linter and Formatter

This project uses `flake8` for linting and `black` for formatting.

To install these tools, run:

```bash
pip install -r requirements-dev.txt
```

To check your code for PEP8 compliance and other potential issues, run:

```bash
flake8 .
```

To automatically format your code to comply with PEP8, run:

```bash
black .
```

## Dependencies

This project has two sets of dependencies: production and development.

Production dependencies are listed in `requirements.txt`. These are necessary for running the application.

Development dependencies are listed in `requirements-dev.txt`. These are not necessary for running the application, but are useful for development. To install these dependencies, run:

```bash
pip install -r requirements-dev.txt
```

# Usage

This script now supports two subcommands: `fromtext` and `fromaudio`.

Here are examples of how to use these subcommands:

1. Basic usage with default parameters for `fromtext`:

```bash
source env/bin/activate
python main.py fromtext --input sentences.json --output output.mp3
```

2. Specify the target language and translation language for `fromtext`:

```bash
source env/bin/activate
python main.py fromtext --input sentences.json --output output.mp3 --target-lang ja --tr-lang en
```

3. Specify the interval and repetition parameters for `fromtext`:

```bash
source env/bin/activate
python main.py fromtext --input sentences.json --output output.mp3 --interval 2000 --target-repeat 2 --translation-repeat 2
```

The `fromaudio` subcommand is used to create an audio file from an existing audio file and a subtitle file. The subtitle file, which can be in .srt or .ass format, is translated into the target language using the DeepL API. The translated text is then converted into speech and combined with the original audio to create the final audio file.

Before using the `fromaudio` subcommand, you need to set the `DEEPL_API_KEY` environment variable to your DeepL API key. You can do this in a bash shell with the `export` command:

```bash
export DEEPL_API_KEY=your_api_key_here
```

Here is an example of how to use the `fromaudio` subcommand:

```bash
source env/bin/activate
python main.py fromaudio --input-audio input.mp3 --subtitle-file subtitles.srt --output-file output.mp3 --transition-sound ding.mp3 --repeat-count 2 --tr-lang en
```

If the `--subtitle-file` or `--output-file` options are not provided, they will be derived from the `--input-audio` file. If the `--output-file` option is a directory, the output file will be written to that directory with a name derived from the `--input-audio` file.
