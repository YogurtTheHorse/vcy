import os

import mongoengine

from vcy.entities import InputMessage, Answer
from vcy.entities.spells.collapse_spell import CollapseSpell
from vcy.entities.spells.disorientation_spell import DisorientationSpell
from vcy.entities.spells.teleportation_spell import TeleportationSpell
from vcy.models import Chat
from vcy.managers import screen_manager, spells_manager
from vcy.screens.etc.greetings_screen import GreetingsScreen
from vcy.screens.etc.tutorial_screen import TutorialScreen
from vcy.screens.game.oracle_screen import OracleScreen
from vcy.screens.game.rogue_screen import RogueScreen
from vcy.screens.session.connect_screen import ConnectScreen
from vcy.screens.session.new_game_screen import NewGameScreen
from vcy.screens.session.start_game_screen import StartGameScreen
from vcy.screens.session.wait_room_screen import WaitRoomScreen


def init(connect_to_database: bool = False):
    if connect_to_database:
        mongoengine.connect('vcy')

    register_screens()
    register_spells()

    # dir with dungeons
    os.makedirs('dungeons', exist_ok=True)


def register_spells():
    spells = [
        DisorientationSpell(),
        CollapseSpell(),
        TeleportationSpell()
    ]

    for spell in spells:
        spells_manager.register_spell(spell)


def register_screens():
    screens_classes = [
        GreetingsScreen, TutorialScreen, StartGameScreen, NewGameScreen, WaitRoomScreen, ConnectScreen,
        RogueScreen, OracleScreen
    ]

    for screen_class in screens_classes:
        screen_manager.register_screen_class(screen_class)


def process_input(message: InputMessage) -> Answer:
    chat = Chat.get_by_platform_id(message.chat_id)

    screen_class = screen_manager.get_screen_class(chat.screens_stack[-1])
    screen = screen_class(chat)

    answer = screen.process_message(message)
    chat.save()

    if not answer.chat_id:
        answer.chat_id = message.chat_id

    return answer
