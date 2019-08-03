import random
from typing import List, Union

import pymorphy2
from pymorphy2.analyzer import Parse

__morph = pymorphy2.MorphAnalyzer()

words_for_pass = [
    'арбуз', 'аптека', 'борода', 'стол', 'стул', 'крематорий', 'диван', 'дверь', 'ноутбук', 'стакан', 'наушники',
    'рука', 'запятая', 'абордаж', 'ключ', 'татуировка', 'точка', 'апельсин', 'феникс', 'скорбь', 'пакет'
]


def normalize(word: str) -> str:
    return __morph.parse(word)[0].normal_form


def is_positive(text: str) -> bool:
    return text.lower() in ['хочу', 'конечно', 'да']


def is_same_word(normal_forms: Union[str, List[str]], user_input: str) -> bool:
    if isinstance(normal_forms, str):
        normal_forms = [normal_forms]

    for normal_form in normal_forms:
        morphs = __morph.parse(user_input)  # type: List[Parse]

        if morphs[0].normal_form.lower() == normal_form.lower():
            return True

        if any(m.normal_form.lower() == normal_form.lower() and m.score > 0.9 for m in morphs[1:]):
            return True

    return False


def generate_word_for_pass():
    return random.choice(words_for_pass)
