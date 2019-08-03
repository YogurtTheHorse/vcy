from typing import List

from mongoengine import EmbeddedDocument, EmbeddedDocumentListField, IntField, StringField, BooleanField

from vcy.entities import str_colors


class Room(EmbeddedDocument):
    id = IntField()
    color = StringField(choices=str_colors)


class Door(EmbeddedDocument):
    id = IntField()

    first_room_id = IntField()
    second_room_id = IntField()

    color = StringField(choices=str_colors)
    is_closed = BooleanField(default=False)

    def is_connected_to(self, room: Room):
        return room.id == self.first_room_id or room.id == self.second_room_id


class Key(EmbeddedDocument):
    room_id = IntField()
    color = StringField(choices=str_colors)


class Dungeon(EmbeddedDocument):
    rooms = EmbeddedDocumentListField(Room, default=list)  # type: List[Room]
    doors = EmbeddedDocumentListField(Door, default=list)  # type: List[Door]
    keys = EmbeddedDocumentListField(Key, default=list)  # type: List[Key]

    finish_room_id = IntField()
