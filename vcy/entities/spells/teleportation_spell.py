import random

from vcy.entities.spells.spell_executor import SpellExecutor
from vcy.managers.dungeon_manager import get_all_accessible_rooms
from vcy.models import GameSession


class TeleportationSpell(SpellExecutor):
    def __init__(self):
        super().__init__('teleportation')

    @property
    def rendered_name(self) -> str:
        return 'заклинание телепортации'

    def cast(self, session: GameSession):
        ac = get_all_accessible_rooms(session.dungeon, session.rogue_room)

        session.rogue_room = random.choice(ac)
        session.save()
