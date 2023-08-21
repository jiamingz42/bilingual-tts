import os
from enum import Enum
from typing import Callable
import deepl


class TranslationStrategy(Enum):
    DEEPL = "deepl"
    FAKE = "fake"

def build_translator(strategy: TranslationStrategy) -> Callable[[str, str], str]:
    if strategy == TranslationStrategy.DEEPL:
        translator = deepl.Translator(os.environ["DEEPL_API_KEY"])
        return translator.translate_text
    elif strategy == TranslationStrategy.FAKE:
        return _fake_translate_func
    else:
        raise ValueError(f"Unsupported translation strategy {strategy}.")


def _fake_translate_func(text: str, target_lang: str) -> str:
    return f"[{target_lang}] Hello world"

