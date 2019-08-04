import random
from typing import List, Union

import pymorphy2
from pymorphy2.analyzer import Parse

from vcy.entities import GameColors

__morph = pymorphy2.MorphAnalyzer()

words_for_pass = [
    'арбуз', 'аптека', 'борода', 'стол', 'стул', 'крематорий', 'диван', 'дверь', 'ноутбук', 'стакан', 'провод',
    'рука', 'запятая', 'абордаж', 'ключ', 'татуировка', 'точка', 'апельсин', 'феникс', 'скорбь', 'пакет'
]


def normalize(word: str) -> str:
    pre = __morph.parse(word)[0].normal_form

    # AAAA!
    if pre == 'синия':
        return 'синий'

    return pre


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


def said_word(normal_form, text) -> bool:
    return any(is_same_word(normal_form, w) for w in text.split())


def color_to_text(color: Union[GameColors, str], sex: str = 'm'):
    if isinstance(color, str):
        color = GameColors(color)

    base = ''
    if color == GameColors.RED:
        base = 'Красн'
    elif color == GameColors.BLUE:
        if sex[0] == 'm':
            return 'Синий'
        else:
            return 'Синяя'
    elif color == GameColors.GREEN:
        base = 'Зелен'

    return base + ('ый' if sex[0] == 'm' else 'ая')


def generate_word_for_pass():
    return random.choice(words_for_pass)
