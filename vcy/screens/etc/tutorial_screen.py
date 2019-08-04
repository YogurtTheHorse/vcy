from typing import Optional

from vcy import text_utils
from vcy.entities import InputMessage, Answer
from vcy.managers import screen_manager
from vcy.screens.screen import Screen


class TutorialScreen(Screen):
    @staticmethod
    def get_name():
        return 'tutorial'

    def on_open(self) -> Optional[Answer]:
        return self.answer('Привет, это игра для двух игроков, которые мешают друг другу. В подземелье пробрался вор и '
                           'пытается выбраться из него с сокровищами, а оракул — хранитель подземелья — наоборот '
                           'мешает ему. Колдун шифрует заклинания с помощью случайных слов, а вор пытается расшифровать '
                           'что тот пытается сделать и противостоять ему.'
                           '\n\n'
                           'Повторить еще раз?')

    def process_message(self, message: InputMessage) -> Answer:
        if text_utils.is_positive(message.text):
            return self.on_open()
        else:
            return screen_manager.switch_screen(self.chat, 'start_game')

