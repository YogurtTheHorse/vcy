from typing import Optional

from vcy import text_utils
from vcy.entities import InputMessage, Answer
from vcy.managers import screen_manager
from vcy.models import GameSession
from vcy.screens.screen import Screen


class NewGameScreen(Screen):
    @staticmethod
    def get_name():
        return 'new_game'

    def on_open(self) -> Optional[Answer]:
        return self.answer('Выбери за кого ты хочешь играть: Оракул или Вор?', ['Оракул', 'Вор'])

    def start_session(self, role: str) -> Answer:
        game_session = GameSession()

        if role == 'oracle':
            game_session.oracle_chat = self.chat
        else:
            game_session.rogue_chat = self.chat

        game_session.init_pass()
        game_session.save()

        return screen_manager.navigate_to(self.chat, 'wait_room')

    def process_message(self, message: InputMessage) -> Answer:
        if text_utils.is_same_word(['оракул', 'оракл'], message.text.split()[-1]):
            return self.start_session('oracle')
        elif text_utils.is_same_word('вор', message.text.split()[-1]):
            return self.start_session('rogue')
        else:
            return self.answer('Я вас не понял, попробуй сказать еще раз: искатель или оракул.')

