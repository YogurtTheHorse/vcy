from vcy.entities.spells.spell_executor import SpellExecutor
from vcy.managers import dungeon_manager
from vcy.models import GameSession


class CollapseSpell(SpellExecutor):
    def __init__(self):
        super().__init__('collapse')

    def cast(self, session: GameSession):
        goals = dungeon_manager.find_all_goals(session.dungeon)