from typing import Type, Optional

from vcy.entities import Answer
from vcy.models import Chat
from vcy.screens.screen import Screen

screen_classes = dict()


def register_screen_class(screen_class: Type[Screen]):
    name = screen_class.get_name()

    if name in screen_classes:
        raise ValueError(f'screen with name {name} already registered')

    screen_classes[name] = screen_class


def get_screen_class(name: str) -> Type[Screen]:
    return screen_classes[name]


def navigate_to(chat: Chat, new_screen: str) -> Optional[Answer]:
    chat.screens_stack.append(new_screen)

    return get_screen_class(new_screen)(chat).on_open()


def switch_screen(chat: Chat, new_screen: str) -> Optional[Answer]:
    chat.screens_stack.pop()
    return navigate_to(chat, new_screen)
