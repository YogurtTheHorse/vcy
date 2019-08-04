from typing import Optional

from vcy.entities import Answer, InputMessage, GameColors
from vcy.screens.game.game_screen import GameScreen
from vcy.text_utils import color_to_text, normalize


class RogueScreen(GameScreen):
    @staticmethod
    def get_name():
        return 'game_rogue'

    def process_message(self, message: InputMessage) -> Answer:
        if self.session.turn == 'oracle':
            return self.answer('Судя по всему сейчас не ваш ход, позалипайте в стену!')

        tokens = [normalize(w) for w in message.text.split()]

        if 'открыть' in tokens:
            colors = [
                (str(color), normalize(color_to_text(color)))
                for color in GameColors
                if normalize(color_to_text(color)) in tokens
            ]

            if len(colors) > 1 or len(colors) == 0:
                return self.answer('Не поняла, какую дверь нужно было открыть, попробуй сказать попроще')

            return self.open_door(colors[0][0])

        return self.answer('Я вас не поняла\n\n' + self.get_room_info())

    def open_door(self, color) -> Answer:
        doors = [
            d
            for d in self.connected_doors(self.rogue_room)
            if d.color == color
        ]

        if len(doors) != 1:
            return self.answer('Тут нет такой двери' + str(self.rogue_room.id))

        door = doors[0]

        if door.is_closed:
            return self.answer('Дверь закрыта, придется поискать ключ')
        else:
            another_room_id = next(i for i in [door.first_room_id, door.second_room_id] if i != self.rogue_room.id)

            self.session.rogue_room = another_room_id
            self.session.next_turn()
            self.session.save()

            return self.answer(f'Вы вошли в комнату за {color} дверью.\n\n{self.get_room_info()}')

    def get_room_info(self) -> str:
        room = self.rogue_room

        if room.id == self.dungeon.finish_room_id:
            return 'Это финиш, вы выиграли!'

        doors = self.connected_doors(room)

        doors_count_str = f'{len(doors)} {"дверью" if len(doors) == 1 else "дверями"}'
        if len(doors) == 1:
            doors_str = color_to_text(doors[0].color, 'f')
        else:
            doors_str = ', '.join(color_to_text(d.color, 'f') for d in doors[:-1]) + \
                        ' и ' + color_to_text(doors[-1].color, 'f')

        keys_info = ''

        for key in self.dungeon.keys:
            if key.room_id != room.id:
                continue

            keys_info += f'Вы нашли {color_to_text(key.color)} ключ.\n\n'

            for door in self.dungeon.doors:
                if door.is_closed and door.color == key.color:
                    door.is_closed = False

            self.dungeon.keys = [k for k in self.dungeon.keys if k.color == key.color]

        if len(keys_info) > 0:
            self.session.save()

        return f'Вы стоите в комнате с {doors_count_str}: {doors_str.lower()}.\n\n' \
               f'{keys_info}' \
               f'Что будем делать?'

    def on_open(self) -> Optional[Answer]:
        return self.answer('Вы только что украли драгоценности из подеземелий могущественного монарха. Его катакомбы '
                           'охраняются не менее могущественным Оракулом, который будет всячески вам мешать. Вам нужной '
                           'найти выход отсюда — для этого необходимо искать ключи от закрытых дверей и искать выход '
                           'наружу.\n\n'
                           'Пока вы будете бродить по лабиринту оракул будет произносить заклинания. Заклинания будут'
                           'состоять из случайных слов, но какие-то из них будут что-то значить, если вы успеете '
                           'вовремя защититься от них, то он не сможет их наложить, но для этого вам потребуется '
                           'разгадать шифр оракула.\n\n'
                           f'{self.get_room_info()}')
