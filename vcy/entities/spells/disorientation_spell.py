from vcy.entities.spells.spell_executor import SpellExecutor
from vcy.models import GameSession


class DisorientationSpell(SpellExecutor):
    def __init__(self):
        super().__init__('disorientation')

    def cast(self, session: GameSession):
        session.is_disorientated = True
