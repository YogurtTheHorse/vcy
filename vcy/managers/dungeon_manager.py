import random
from typing import Tuple, List, Union

from graphviz import Graph

from vcy.dungeon_models import Dungeon, Room, Door, Key
from vcy.entities import GameColors, str_colors


def connected_doors(room: Union[Room, int], doors: List[Door]) -> List[Door]:
    return [
        d
        for d in doors
        if d.is_connected_to(room)
    ]


def count_doors(room: Room, doors: List[Door]) -> int:
    return len(connected_doors(room, doors))


def generate_component(dungeon, color, actions_count_range: Tuple[int, int] = (5, 7)):
    next_room_id = (dungeon.rooms[-1].id + 1) if len(dungeon.rooms) > 0 else 0
    next_door_id = (dungeon.doors[-1].id + 1) if len(dungeon.doors) > 0 else 0

    actions_count = random.randint(*actions_count_range)

    start_room_id = next_room_id

    component_rooms = [Room(id=start_room_id, color=str(color))]  # type: List[Room]
    component_doors = []  # type: List[Door]

    next_room_id += 1

    for i in range(actions_count):
        available_rooms = []

        for room in component_rooms:
            doors_count = count_doors(room, component_doors)

            if (doors_count < 3 and room.id != start_room_id) or doors_count < 2:
                available_rooms.append(room)

        if len(available_rooms) == 0:
            break

        if len(available_rooms) < 3 or random.random() > 0.5:  # generate room
            new_room = Room(id=next_room_id, color=str(color))
            next_room_id += 1

            room_to_connect = random.choice(available_rooms)

            component_rooms.append(new_room)
            component_doors.append(Door(id=next_door_id,
                                        first_room_id=new_room.id,
                                        second_room_id=room_to_connect.id))

            next_door_id += 1
        else:  # generate new door
            first_room = random.choice(available_rooms)
            second_room = random.choice([r for r in available_rooms if r.id != first_room.id])

            component_doors.append(Door(id=next_door_id,
                                        first_room_id=first_room.id,
                                        second_room_id=second_room.id))
            next_door_id += 1

    component_door = None
    if len(dungeon.rooms) > 0:
        # connect component to dungeon

        room_to_connect_components_id = random.choice([
            r
            for r in dungeon.rooms
            if str(color) not in [
                d.color for d in connected_doors(r, dungeon.doors)
            ]
        ]).id

        second_room_to_connect_components_id = component_rooms[0].id

        component_door = Door(id=next_door_id,
                              first_room_id=room_to_connect_components_id,
                              second_room_id=second_room_to_connect_components_id,
                              color=str(color),
                              is_closed=True)

        dungeon.keys.append(Key(
            room_id=random.choice(dungeon.rooms[1:]).id,
            color=str(color)
        ))

    for room in component_rooms:
        doors = connected_doors(room, component_doors)
        used_colors = [d.color for d in doors if d.color]

        available_colors = [
            color
            for color in str_colors
            if color not in used_colors
        ]

        random.shuffle(available_colors)

        for door in doors:
            if not door.color:
                door.color = available_colors.pop()

    for room in component_rooms:
        doors = connected_doors(room, component_doors)
        used_colors = []

        for door in doors:
            if door.color in used_colors:
                raise IndexError()
            else:
                used_colors.append(door.color)

    dungeon.doors.extend(component_doors)
    dungeon.rooms.extend(component_rooms)

    if component_door:
        dungeon.doors.append(component_door)


def generate_dungeon() -> Dungeon:
    generated = False
    dungeon = Dungeon()

    while not generated:
        try:
            for color in GameColors:
                generate_component(dungeon, color)

            dungeon.finish_room_id = random.choice([
                room
                for room in dungeon.rooms
                if room.color == str(GameColors.BLUE)
            ]).id

            generated = True
        except IndexError:
            dungeon = Dungeon()

    return dungeon


def render_dungeon(dungeon: Dungeon, session_id: str, rogue_position: int):
    filename = f'./dungeons/d-{session_id}.gv'
    g = Graph('Dungeon_graph', filename=filename, format='png', engine='fdp')

    for room in dungeon.rooms:
        contains_key = any(key.room_id == room.id for key in dungeon.keys)

        shape = 'circle'
        if rogue_position == room.id:
            shape = 'triangle'
        elif contains_key:
            shape = 'doublecircle'
        elif room.id == dungeon.finish_room_id:
            shape = 'star'

        g.attr('node', color=str(room.color), shape=shape)
        g.node(str(room.id))

    for door in dungeon.doors:
        if door.is_closed:
            style = 'dashed'
        else:
            style = 'solid'
        g.attr('edge', color=str(door.color), style=style)
        g.edge(str(door.first_room_id), str(door.second_room_id))

    g.render()

    return f'{filename}.png'


def get_all_accessible_rooms(dungeon: Dungeon, start: int):
    rooms_queue = [start]
    answer = []
    visited = []

    while len(rooms_queue) > 0:
        r = rooms_queue.pop()

        answer.append(r)
        doors = [d for d in connected_doors(r, dungeon.doors) if not d.is_closed]

        for door in doors:
            if door.first_room_id != r and door.first_room_id not in answer:
                rooms_queue.append(door.first_room_id)
            elif door.second_room_id != r and door.second_room_id not in answer:
                rooms_queue.append(door.second_room_id)

    return answer


def find_all_goals(dungeon: Dungeon) -> List[int]:
    return [key.room_id for key in dungeon.keys] + \
           [dungeon.finish_room_id]


def is_accessible_without_door(dungeon: Dungeon, goal: int, start: int, door_id: int):
    rooms_queue = [start]
    visited = []

    while len(rooms_queue) > 0:
        r = rooms_queue.pop()

        visited.append(r)
        doors = [d for d in connected_doors(r, dungeon.doors) if not d.is_closed and d.id != door_id]

        for door in doors:
            if door.first_room_id != r and door.first_room_id not in visited:
                rooms_queue.append(door.first_room_id)
            elif door.second_room_id != r and door.second_room_id not in visited:
                rooms_queue.append(door.second_room_id)

    return goal in visited
