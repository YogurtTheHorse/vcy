from typing import Optional

from vcy.entities import Answer, InputMessage
from vcy.screens.screen import Screen


class SeekerScreen(Screen):
    @staticmethod
    def get_name():
        return 'game_seeker'

    def process_message(self, message: InputMessage) -> Answer:
        return self.answer(message.text)

    def on_open(self) -> Optional[Answer]:
        return self.answer('seeker')
