from typing import List, Optional

from cached_property import cached_property
from mongoengine.queryset.visitor import Q
from mongoengine import Document, StringField, ReferenceField, DoesNotExist, ListField, BooleanField, DictField, \
    DynamicField

from vcy import text_utils


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
    def session(self) -> 'Session':
        return Session.find_user_session(self)


class Session(Document):
    oracle_chat = ReferenceField(Chat)
    seeker_chat = ReferenceField(Chat)

    passphrase = ListField(StringField(), required=True)

    turn = StringField(choices=['oracle', 'seeker'])

    @classmethod
    def find_user_session(cls, chat: Chat) -> Optional['Session']:
        try:
            return cls.objects.get(Q(oracle_chat=chat) | Q(seeker_chat=chat))
        except DoesNotExist:
            return None

    @classmethod
    def find_by_pass(cls, words: List[str]) -> Optional['Session']:
        try:
            return cls.objects.get(passphrase=[text_utils.normalize(w) for w in words])
        except DoesNotExist:
            return None

    @property
    def ready(self):
        return self.oracle_chat is not None and self.seeker_chat is not None

    def init_pass(self):
        self.passphrase = [text_utils.generate_word_for_pass() for i in range(4)]

    def join(self, chat: Chat):
        if self.oracle_chat is None:
            self.oracle_chat = chat
        elif self.seeker_chat is None:
            self.seeker_chat = chat
        else:
            raise ValueError()
