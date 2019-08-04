import random

from vcy.entities.spells.spell_executor import SpellExecutor
from vcy.managers import dungeon_manager
from vcy.managers.dungeon_manager import is_accessible_without_door
from vcy.models import GameSession


class CollapseSpell(SpellExecutor):
    def __init__(self):
        super().__init__('collapse')

    @property
    def rendered_name(self) -> str:
        return 'заклинание обвала двери'

    def cast(self, session: GameSession):
        goals = dungeon_manager.find_all_goals(session.dungeon)

        some_doors = session.dungeon.doors
        random.shuffle(some_doors)

        good_door = next((
            door
            for door in some_doors
            if all(
                is_accessible_without_door(
                    session.dungeon,
                    g,
                    session.rogue_room,
                    door.id
                )
                for g in goals
            )
        ), None)

        if good_door is not None:
            session.dungeon.doors = [
                d
                for d in session.dungeon.doors
                if d.id != good_door.id
            ]
            session.save()
