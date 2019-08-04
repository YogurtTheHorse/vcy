import random
from typing import List, Dict

from vcy.entities.rules.base_rule import BaseRule
from vcy.entities.rules.one_word_rule import OneWordRule

magic_words = [
    'арбуз', 'аптека', 'борода', 'стол', 'стул', 'крематорий', 'диван', 'дверь', 'ноутбук', 'стакан', 'провод',
    'рука', 'запятая', 'абордаж', 'ключ', 'татуировка', 'точка', 'апельсин', 'феникс', 'скорбь', 'пакет', 'окно'
]


def generate_rule() -> BaseRule:
    return OneWordRule(random.choice(magic_words))


def generate_non_conflict_rule(rules: List[BaseRule]) -> BaseRule:
    conflicting = True
    rule = None

    while conflicting:
        rule = generate_rule()

        conflicting = any(r.is_conflicting(rule) for r in rules)

    return rule


def serialize(rule: BaseRule) -> dict:
    if isinstance(rule, OneWordRule):
        return {
            'type': 'owr',
            'word': OneWordRule.word
        }
    else:
        raise ValueError()


def deserialize(rule_dict: Dict) -> BaseRule:
    rule_type = rule_dict.get('type', None)

    if rule_type == 'owr':
        return OneWordRule(rule_dict['word'])
    else:
        raise ValueError()
