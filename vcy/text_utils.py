import random
from typing import List

import pymorphy2
from pymorphy2.analyzer import Parse

__morph = pymorphy2.MorphAnalyzer()

words_for_pass = [
    'арбуз', 'аптека', 'борода', 'стол', 'стул', 'крематорий', 'диван', 'дверь', 'ноутбук', 'стакан', 'наушники',
    ''
]

def is_positive(text: str) -> bool:
    return text.lower() in ['хочу', 'конечно', 'да']


def is_same_word(normal_form: str, user_input: str) -> bool:
    morphs = __morph.parse(user_input)  # type: List[Parse]

    return any(m.normal_form.lower() == normal_form.lower() and m.score > 0.9 for m in morphs)


def generate_word_for_pass():
    return random.choice(words_for_pass)
