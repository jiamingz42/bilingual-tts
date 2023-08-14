# Overview

This script is used to create an audio file from a set of sentences. The sentences are provided in a JSON file. The script uses Google Text-to-Speech to convert the sentences into speech. The speech is then combined with a transition sound to create the final audio file. The script allows the user to specify the target language, the translation language, the interval between repetitions, and the number of times to repeat the target language and the translation.

# Usage

Here are three examples of how to use this script:

1. Basic usage with default parameters:

```bash
source env/bin/activate
python main.py --input sentences.json --output output.mp3
```

2. Specify the target language and translation language:

```bash
source env/bin/activate
python main.py --input sentences.json --output output.mp3 --target-lang ja --tr-lang en
```

3. Specify the interval and repetition parameters:

```bash
source env/bin/activate
python main.py --input sentences.json --output output.mp3 --interval 2000 --target-repeat 2 --translation-repeat 2
```
