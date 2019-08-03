from typing import List, Optional

from mongoengine.queryset.visitor import Q
from mongoengine import Document, StringField, ReferenceField, DoesNotExist, ListField, BooleanField, DictField, \
    DynamicField, ObjectIdField


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


class Session(Document):
    oracle_chat = ReferenceField(Chat, required=True)
    seeker_chat = ReferenceField(Chat, required=True)

    passphrase = ListField(StringField(), required=True)

    turn = StringField(choices=['oracle', 'seeker'])

    @classmethod
    def find_user_session(cls, chat: str) -> Optional['Session']:
        try:
            return cls.objects.get(Q(oracle_chat=chat) | Q(seeker_chat=chat))
        except DoesNotExist:
            return None

    def init_pass(self):


