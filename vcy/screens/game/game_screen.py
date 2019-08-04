from abc import ABC

from vcy.dungeon_models import Dungeon, Room
from vcy.managers.dungeon_manager import connected_doors
from vcy.models import GameSession
from vcy.screens.screen import Screen


class GameScreen(Screen, ABC):
    @property
    def session(self) -> GameSession:
        return self.chat.session

    @property
    def dungeon(self) -> Dungeon:
        return self.session.dungeon

    @property
    def rogue_room(self) -> Room:
        return next(r for r in self.dungeon.rooms if r.id == self.session.rogue_room)

    def connected_doors(self, room):
        return connected_doors(room, self.dungeon.doors)
