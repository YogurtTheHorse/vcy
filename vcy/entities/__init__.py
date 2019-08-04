from enum import Enum
from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Image:
    image_path: str
    title: str
    description: str


@dataclass
class InputMessage:
    chat_id: str
    text: str

    is_start_message: bool = False

    def answer(self, message):
        return Answer(chat_id=self.chat_id, message=message)


@dataclass
class Answer:
    message: str
    chat_id: Optional[str] = None
    buttons: List[str] = None
    image: Image = None


class GameColors(Enum):
    RED = 'red'
    GREEN = 'green'
    BLUE = 'blue'

    def __str__(self):
        return '%s' % self.value


str_colors = [str(color) for color in GameColors]
