from typing import List, Dict

from vcy.dungeon_models import Spell
from vcy.entities.spells.spell_executor import SpellExecutor
from vcy.managers.rules_manager import generate_non_conflict_rule, serialize

__spells = dict()  # type: Dict[str, SpellExecutor]


def get_spell_by_name(name) -> SpellExecutor:
    return __spells[name]


def register_spell(spell: SpellExecutor):
    if spell.name in __spells:
        raise ValueError()

    __spells[spell.name] = spell


def generate_spells() -> List[Spell]:
    rules = []

    for _ in __spells.keys():
        rules.append(generate_non_conflict_rule(rules))

    return [
        Spell(
            rule_dict=serialize(rules.pop()),
            spell_type=spell.name
        )

        for spell in __spells.values()
    ]
