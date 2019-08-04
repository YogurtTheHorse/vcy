from typing import List, Union

from cached_property import cached_property
from mongoengine import EmbeddedDocument, EmbeddedDocumentListField, IntField, StringField, BooleanField, DictField

from vcy.entities import str_colors
from vcy.entities.rules.base_rule import BaseRule


class Room(EmbeddedDocument):
    id = IntField()
    color = StringField(choices=str_colors)


class Door(EmbeddedDocument):
    id = IntField()

    first_room_id = IntField()
    second_room_id = IntField()

    color = StringField(choices=str_colors)
    is_closed = BooleanField(default=False)

    def is_connected_to(self, room: Union[Room, int]):
        rid = room if isinstance(room, int) else room.id

        return rid == self.first_room_id or rid == self.second_room_id


class Key(EmbeddedDocument):
    room_id = IntField()
    color = StringField(choices=str_colors)


class Dungeon(EmbeddedDocument):
    rooms = EmbeddedDocumentListField(Room, default=list)  # type: List[Room]
    doors = EmbeddedDocumentListField(Door, default=list)  # type: List[Door]
    keys = EmbeddedDocumentListField(Key, default=list)  # type: List[Key]

    finish_room_id = IntField()


class Spell(EmbeddedDocument):
    rule_dict = DictField(StringField())
    spell_type = StringField()

    @cached_property
    def spell_rule(self) -> BaseRule:
        from vcy.managers import rules_manager

        return rules_manager.deserialize(self.rule_dict)
