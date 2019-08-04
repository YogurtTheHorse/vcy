from abc import ABC, abstractmethod


class SpellExecutor(ABC):
    def __init__(self, name):
        self.name = name

    @property
    @abstractmethod
    def rendered_name(self) -> str:
        return ''

    # noinspection PyUnresolvedReferences
    @abstractmethod
    def cast(self, session: 'GameSession'):
        pass
