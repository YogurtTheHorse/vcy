from typing import Optional, List

from vcy.dungeon_models import Spell
from vcy.entities import Answer, InputMessage, Image
from vcy.managers import spells_manager
from vcy.managers.dungeon_manager import render_dungeon
from vcy.screens.game.game_screen import GameScreen
from vcy.text_utils import said_word


class OracleScreen(GameScreen):
    @staticmethod
    def get_name():
        return 'game_oracle'

    def process_message(self, message: InputMessage) -> Answer:
        if self.session.map_researched:
            if said_word('карта', message.text) and said_word('посмотреть', message.text):
                rendered_map = render_dungeon(self.dungeon, str(self.session.id), self.rogue_room.id)

                return self.answer('%STUB%',
                                   image=Image(
                                       title='Карта подземелья',
                                       description='Вор находится где-то тут.',
                                       image_path=rendered_map
                                   ))
            elif self.session.turn == 'oracle':
                return self.process_turn(message)
            else:
                return self.answer('Сейчас ход вора, нужно подождать, пока он разберется, что делать, он находится в '
                                   f'комнате под номером {self.rogue_room.id}.')
        else:
            self.session.map_researched = True
            self.session.save()

            rules_str = '\n'.join([
                f'{spell.spell_rule.render_to_text()} сработает '
                f'{spells_manager.get_spell_by_name(spell.spell_type).rendered_name}'

                for spell in self.session.spells
            ])

            return self.answer('Отлично, теперь когда ты вспомнил, что ты вообще там себе охраняешь можно рассказать '
                               'тебе про заклинания.\n\n'
                               'Заклинание это любой набор слов, но есть несолько правил:\n\n'
                               f'{rules_str}\n\n'
                               f'Можешь начинать колдовать — старайся запутать вора, иначе он догадается и начнет '
                               f'принимать контр-меры.')

    def on_open(self) -> Optional[Answer]:
        rendered_map = render_dungeon(self.dungeon, str(self.session.id), self.rogue_room.id)

        return self.answer('%STUB%',
                           image=Image(
                               title='Карта подземелья',
                               description='Вы оракул и охраняете сокровища подземелья. Сейчас кто-то пробрался в '
                                           'хоромы и вам нужно остановить его. В вашем распоряжение находится карта '
                                           'подземелья. Изучите ее.',
                               image_path=rendered_map
                           ))

    def process_turn(self, message: InputMessage) -> Answer:
        spells = [
            spell
            for spell in self.session.spells
            if spell.spell_rule.check(message.text)
        ]  # type: List[Spell]

        if len(spells) != 1:
            player_info = ''

            if self.session.rogue_status == 'saved':
                player_info = '\n\nК слов, вор спасся от прошлого заклинания!'
            elif self.session.rogue_status == 'doomed':
                player_info = '\n\nВор попался в твою ловушку!'

            return self.answer(f'Как-то слишком запутанно получилось. Давай еще раз.{player_info}')

        self.session.target_cast = spells[0].spell_type
        self.session.cast_text = message.text
        self.session.next_turn()
        self.session.save()

        return self.answer('Отлично, посмотрим, получится ли у нас и что будет дальше... Сейчас вор находится в '
                           f'комнате под номером {self.rogue_room.id}')
