from vcy.entities.spells.spell_executor import SpellExecutor
from vcy.models import GameSession


class ColorBlindnessSpell(SpellExecutor):
    def __init__(self):
        super().__init__('blindness')

    def cast(self, session: GameSession):
        pass
