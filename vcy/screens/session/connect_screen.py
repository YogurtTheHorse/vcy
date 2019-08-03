from typing import Optional

from vcy.entities import InputMessage, Answer
from vcy.models import Session
from vcy.screens.screen import Screen


class ConnectScreen(Screen):
    @staticmethod
    def get_name():
        return 'connect_to_game'

    def on_open(self) -> Optional[Answer]:
        return self.answer('Отлично, назовите четыре кодовых слова, чтобы присоедениться к игре.')

    def process_message(self, message: InputMessage) -> Answer:
        words = message.text.split()

        if len(words) != 4:
            return self.answer('Нужно сказать четыре слова')

        available_session = Session.find_by_pass(words)

        if available_session is None:
            return self.answer('Не найдено игр с такими кодовыми словам, попробуйте еще раз')
        else:
            available_session.join(self.chat)
            available_session.save()

            return self.switch_screen(self.chat.game_screen_name)


