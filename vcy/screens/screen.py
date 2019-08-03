from abc import ABC, abstractmethod
from typing import Optional, List

from vcy.entities import InputMessage, Answer
from vcy.models import Chat


class Screen(ABC):
    def __init__(self, chat: Chat):
        self.chat = chat

    @staticmethod
    @abstractmethod
    def get_name():
        pass

    @abstractmethod
    def process_message(self, message: InputMessage) -> Answer:
        pass

    def answer(self, text: str, buttons: List[str] = None):
        return Answer(chat_id=self.chat.platform_id, message=text, buttons=buttons or list())

    @abstractmethod
    def on_open(self) -> Optional[Answer]:
        return None

    def navigate_to(self, screen_name: str) -> Answer:
        from vcy.managers import screen_manager

        return screen_manager.navigate_to(self.chat, screen_name)

    def switch_screen(self, screen_name: str) -> Answer:
        from vcy.managers import screen_manager

        return screen_manager.switch_screen(self.chat, screen_name)
