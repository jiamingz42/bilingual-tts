# Overview

This script is used to create an audio file from a set of sentences. The sentences are provided in a JSON file. The script uses Google Text-to-Speech to convert the sentences into speech. The speech is then combined with a transition sound to create the final audio file. The script allows the user to specify the target language, the translation language, the interval between repetitions, and the number of times to repeat the target language and the translation.

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

The `fromaudio` subcommand is used to create an audio file from an existing audio file and a subtitle file. The subtitle file is translated into the target language using the DeepL API. The translated text is then converted into speech and combined with the original audio to create the final audio file.

Before using the `fromaudio` subcommand, you need to set the `DEEPL_API_KEY` environment variable to your DeepL API key. You can do this in a bash shell with the `export` command:

```bash
export DEEPL_API_KEY=your_api_key_here
```

Here is an example of how to use the `fromaudio` subcommand:

```bash
source env/bin/activate
python main.py fromaudio --input-audio input.mp3 --subtitle-file subtitles.srt --output-file output.mp3 --transition-sound ding.mp3 --repeat-count 2 --tr-lang en
```
