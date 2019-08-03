import random
from typing import Tuple, List

from vcy.dungeon_models import Dungeon, Room, Door
from vcy.entities import GameColors, str_colors


def generate_component(dungeon, color, actions_count_range: Tuple[int, int] = (5, 7)):
    next_room_id = (dungeon.rooms[-1].id + 1) if len(dungeon.rooms) > 0 else 0
    next_door_id = (dungeon.doors[-1].id + 1) if len(dungeon.doors) > 0 else 0

    actions_count = random.randint(*actions_count_range)

    component_rooms = [Room(id=next_room_id, color=str(color))]  # type: List[Room]
    component_doors = []  # type: List[Door]

    next_room_id += 1

    for i in range(actions_count):
        available_rooms = [r for r in component_rooms if
                           len(list(d for d in component_doors if d.is_connected_to(r))) < 2]

        if len(available_rooms) == 0:
            break

        if random.random() > 0.3:  # generate room
            new_room = Room(id=next_room_id, color=str(color))
            next_room_id += 1

            room_to_connect = random.choice(available_rooms)
            used_colors = [d.color for d in component_doors if d.is_connected_to(room_to_connect)]
            new_door_color = random.choice([color for color in str_colors if color not in used_colors])

            component_rooms.append(new_room)
            component_doors.append(Door(id=next_door_id,
                                        first_room_id=new_room.id,
                                        second_room_id=room_to_connect.id,
                                        color=new_door_color))
            next_door_id += 1
        else:  # generate new door
            pass

    room_to_connect_components_id = random.choice(dungeon.rooms).id
    second_room_to_connect_components_id = random.choice(component_rooms).id

    dungeon.doors.extend(component_doors)
    dungeon.rooms.extend(component_rooms)

    dungeon.doors.append(Door(id=next_door_id,
                              first_room_id=room_to_connect_components_id,
                              second_room_id=second_room_to_connect_components_id,
                              color=str(color)))


def generate_dungeon() -> Dungeon:
    dungeon = Dungeon()
    dungeon.rooms.append(Room(id=0, color=str(GameColors.RED)))

    for color in GameColors:
        generate_component(dungeon, color)

    return dungeon
