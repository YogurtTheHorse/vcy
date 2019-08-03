from typing import List

from mongoengine import EmbeddedDocument, EmbeddedDocumentListField, IntField, StringField

from vcy.entities import GameColors

str_colors = [str(color) for color in GameColors]


class Room(EmbeddedDocument):
    id = IntField()
    color = StringField(choices=str_colors)


class Door(EmbeddedDocument):
    id = IntField()

    first_room_id = IntField()
    second_room_id = IntField()

    color = StringField(choices=str_colors)


class Key(EmbeddedDocument):
    room_id = IntField()
    color = StringField(choices=str_colors)


class Dungeon(EmbeddedDocument):
    rooms = EmbeddedDocumentListField(Room, default=list)  # type: List[Room]
    doors = EmbeddedDocumentListField(Door, default=list)  # type: List[Door]
    keys = EmbeddedDocumentListField(Key, default=list)  # type: List[Key]

    finish_room_id = IntField()











