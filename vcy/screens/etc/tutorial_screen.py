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
        return self.answer('Привет, это игра для двух игроков, которые не слушат друг друга — например находятся в '
                           'разных комнатах. Первый игрок — Оракул. Его задача разобраться в задании и с помощью '
                           'магического шара передать необходимую информацию о задании Искателю — второму игроку. '
                           'Искатель же должен следовать указаниям Оракула и сообщать ему о том, что он видит. \n\n'
                           'Искатель будет бродить по подезмелью, защищенному магическим щитом, поэтому Оракул не '
                           'может видеть, что вокруг искателя, а связь через магический шар нестабильна. \n\n'
                           'Повторить еще раз?')

    def process_message(self, message: InputMessage) -> Answer:
        if text_utils.is_positive(message.text):
            return self.on_open()
        else:
            return screen_manager.switch_screen(self.chat, 'start_game')

