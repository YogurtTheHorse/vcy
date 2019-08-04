from abc import ABC, abstractmethod


class BaseRule(ABC):
    @abstractmethod
    def check(self, text: str) -> bool:
        return False

    @abstractmethod
    def render_to_text(self) -> str:
        return ''

    @abstractmethod
    def is_conflicting(self, rule: 'BaseRule') -> bool:
        pass
