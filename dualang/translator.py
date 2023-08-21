import os
from enum import Enum
from typing import Callable
import deepl
from dualang.fake_translate_func import fake_translate_func

class TranslationStrategy(Enum):
    DEEPL = "deepl"
    FAKE = "fake"

def build_translator(strategy: TranslationStrategy) -> Callable[[str, str], str]:
    if strategy == TranslationStrategy.DEEPL:
        translator = deepl.Translator(os.environ["DEEPL_API_KEY"])
        return translator.translate_text
    elif strategy == TranslationStrategy.FAKE:
        return fake_translate_func
    else:
        raise ValueError(f"Unsupported translation strategy {strategy}.")
