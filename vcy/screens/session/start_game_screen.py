from typing import Optional

from vcy import text_utils
from vcy.entities import InputMessage, Answer
from vcy.managers import screen_manager
from vcy.screens.screen import Screen


class StartGameScreen(Screen):
    @staticmethod
    def get_name():
        return 'start_game'

    def on_open(self) -> Optional[Answer]:
        return self.answer('Ты бы хотел создать игру или присоединиться?', ['Создать', 'Присоедениться'])

    def process_message(self, message: InputMessage) -> Answer:
        if text_utils.is_same_word('создать', message.text):
            return screen_manager.switch_screen(self.chat, 'new_game')
        elif text_utils.is_same_word('присоединиться', message.text):
            return screen_manager.switch_screen(self.chat, 'connect_to_game')
        else:
            return self.answer('Я не смогла разобрать. Выбери либо Создать, либо Присоедениться.')
