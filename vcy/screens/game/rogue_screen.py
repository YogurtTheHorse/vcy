from typing import Optional

from vcy.entities import Answer, InputMessage
from vcy.screens.screen import Screen


class RogueScreen(Screen):
    @staticmethod
    def get_name():
        return 'game_rogue'

    def process_message(self, message: InputMessage) -> Answer:
        return self.answer(message.text)

    def on_open(self) -> Optional[Answer]:
        return self.answer('rogue')
