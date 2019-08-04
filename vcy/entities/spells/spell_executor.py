from abc import ABC, abstractmethod

from vcy.models import GameSession


class SpellExecutor(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def cast(self, session: GameSession):
        pass
