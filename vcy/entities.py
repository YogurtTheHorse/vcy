from dataclasses import dataclass
from typing import Optional, List


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
