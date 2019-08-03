from vcy import text_utils
from vcy.entities import InputMessage
from vcy.managers import screen_manager
from vcy.models import Chat
from vcy.screens.screen import Screen


class GreetingsScreen(Screen):
    def __init__(self, chat: Chat):
        super().__init__(chat)

    @staticmethod
    def get_name():
        return 'greetings'

    def process_message(self, message: InputMessage):
        if message.is_start_message:
            if self.chat.first_play:
                self.chat.first_play = False
                return message.answer('Привет, кажется ты играешь первый раз, не хочешь узнать, что нужно сделать?')
            else:
                return message.answer('Привет, давно не виделись. Напомнить правила игры?')
        else:
            new_screen = 'tutorial' if text_utils.is_positive(message.text) else 'start_game'
            return screen_manager.switch_screen(self.chat, new_screen)
