from vcy.entities.rules.base_rule import BaseRule
from vcy.text_utils import normalize


class OneWordRule(BaseRule):
    def is_conflicting(self, rule: BaseRule) -> bool:
        if isinstance(rule, OneWordRule):
            return self.word == rule.word
        else:
            return False

    def __init__(self, word: str):
        self.word = normalize(word)

    def check(self, text: str) -> bool:
        return self.word in [normalize(w) for w in text.split()]

    def render_to_text(self) -> str:
        return f'Если в заклинании есть слово «{self.word}», то'