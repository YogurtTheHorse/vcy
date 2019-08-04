from typing import List, Optional

from cached_property import cached_property
from mongoengine.queryset.visitor import Q
from mongoengine import Document, StringField, ReferenceField, DoesNotExist, ListField, BooleanField, DictField, \
    DynamicField, EmbeddedDocumentField, IntField

from vcy import text_utils
from vcy.dungeon_models import Dungeon
from vcy.managers.dungeon_manager import generate_dungeon


class Chat(Document):
    platform_id = StringField(unique=True)  # type: str
    first_play = BooleanField(default=True)  # type: bool
    screens_stack = ListField(StringField(), default=lambda: list(['greetings']))  # type: List[str]

    temporary_variables = DictField(DynamicField(), default=dict)

    @classmethod
    def get_by_platform_id(cls, _id: str) -> 'Chat':
        try:
            return cls.objects.get(platform_id=_id)
        except DoesNotExist:
            # noinspection PyTypeChecker
            return Chat(platform_id=_id)

    @cached_property
    def session(self) -> 'GameSession':
        return GameSession.find_user_session(self)

    @property
    def is_oracle(self):
        return self.session is not None and self.session.oracle_chat.platform_id == self.platform_id

    @property
    def game_screen_name(self):
        return 'game_oracle' if self.is_oracle else 'game_rogue'


class GameSession(Document):
    oracle_chat = ReferenceField(Chat)  # type: Chat
    rogue_chat = ReferenceField(Chat)  # type: Chat

    passphrase = ListField(StringField(), required=True)  # type: List[str]

    turn = StringField(choices=['oracle', 'rogue'], default='rogue')  # type: str
    rogue_room = IntField(default=0)  # type: int

    # oracle stuff
    map_researched = BooleanField(default=False)  # type: bool

    # thief stuff
    is_disorientated = BooleanField(default=False)  # type: bool

    dungeon = EmbeddedDocumentField(Dungeon, default=generate_dungeon)  # type: Dungeon

    @classmethod
    def find_user_session(cls, chat: Chat) -> Optional['GameSession']:
        try:
            return cls.objects.get(Q(oracle_chat=chat) | Q(rogue_chat=chat))
        except DoesNotExist:
            return None

    @classmethod
    def find_by_pass(cls, words: List[str]) -> Optional['GameSession']:
        try:
            return cls.objects.get(passphrase=[text_utils.normalize(w) for w in words])
        except DoesNotExist:
            return None

    @property
    def ready(self):
        return self.oracle_chat is not None and self.rogue_chat is not None

    def init_pass(self):
        self.passphrase = [text_utils.generate_word_for_pass() for i in range(4)]

    def join(self, chat: Chat):
        if self.oracle_chat is None:
            self.oracle_chat = chat
        elif self.rogue_chat is None:
            self.rogue_chat = chat
        else:
            raise ValueError()

    def next_turn(self):
        if self.turn == 'oracle':
            self.turn = 'rogue'
        else:
            self.turn = 'oracle'
