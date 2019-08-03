import mongoengine

from vcy.entities import InputMessage, Answer
from vcy.models import Chat
from vcy.managers import screen_manager
from vcy.screens.etc.greetings_screen import GreetingsScreen
from vcy.screens.etc.tutorial_screen import TutorialScreen
from vcy.screens.session.start_game_screen import StartGameScreen


def init(connect_to_database: bool = False):
    if connect_to_database:
        mongoengine.connect('vcy')

    register_screens()


def register_screens():
    screens_classes = [GreetingsScreen, TutorialScreen, StartGameScreen]

    for screen_class in screens_classes:
        screen_manager.register_screen_class(screen_class)


def process_input(message: InputMessage) -> Answer:
    chat = Chat.get_by_platform_id(message.chat_id)

    # TODO: remove
    if message.is_start_message:
        chat.screens_stack = ['greetings']

    screen_class = screen_manager.get_screen_class(chat.screens_stack[-1])
    screen = screen_class(chat)

    answer = screen.process_message(message)
    chat.save()

    if not answer.chat_id:
        answer.chat_id = message.chat_id

    return answer
