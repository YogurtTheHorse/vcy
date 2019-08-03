from graphviz import Graph


def show_dungeon(dungeon):
    g = Graph('Dungeon_graph', filename='dung_graph.gv', format='png')

    for room in dungeon.rooms:
        g.attr('node', color=str(room.color))
        g.node(str(room.id))

    for door in dungeon.doors:
        if door.is_closed:
            style = 'dashed'
        else:
            style = 'solid'
        g.attr('edge', color=str(door.color), style=style)
        g.edge(str(door.first_room_id), str(door.second_room_id))

    g.render()
    return './dung_graph.gv.png'
