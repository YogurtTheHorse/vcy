from typing import Optional

from vcy.entities import Answer, InputMessage, Image
from vcy.managers.dungeon_manager import render_dungeon
from vcy.screens.game.game_screen import GameScreen


class OracleScreen(GameScreen):
    @staticmethod
    def get_name():
        return 'game_oracle'

    def process_message(self, message: InputMessage) -> Answer:
        if self.session.map_researched:
            if self.session.turn == 'oracle':
                return self.process_turn(message)
            else:
                return self.answer('Сейчас ход вора, нужно подождать, пока он разберется, что делать.')
        else:
            self.session.map_researched = True

            rules_str = '\n'.join([])

            return self.answer('Отлично, теперь когда ты вспомнил, что ты вообще там себе охраняешь можно рассказать '
                               'тебе про <speaker effect="megaphone">заклинания.<speaker effect="-">\n\n'
                               'Заклинание это любой набор слов, но есть несолько правил:\n\n'
                               f'{rules_str}')

    def on_open(self) -> Optional[Answer]:
        rendered_map = render_dungeon(self.dungeon, str(self.session.id))

        return self.answer('%STUB%',
                           image=Image(
                               title='Карта подземелья',
                               description='Вы оракул и охраняете сокровища подземелья. Сейчас кто-то пробрался в '
                                           'хоромы и вам нужно остановить его. В вашем распоряжение находится карта '
                                           'подземелья. Изучите ее.',
                               image_path=rendered_map
                           ))

    def process_turn(self, message: InputMessage) -> Answer:
        pass
