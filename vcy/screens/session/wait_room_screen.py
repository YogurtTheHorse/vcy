from vcy.entities import InputMessage, Answer
from vcy.screens.screen import Screen


class WaitRoomScreen(Screen):
    @staticmethod
    def get_name():
        return 'wait_room'

    def on_open(self) -> Answer:
        passphrase = ' '.join(self.chat.session.passphrase)

        return self.answer(f'Вашему другу нужно присоедениться к игре, а потом назвать эти четыре слова: {passphrase}. '
                           f'Когда игрок подключится, скажите «Готово».')

    def process_message(self, message: InputMessage) -> Answer:
        if self.chat.session.ready:
            raise NotImplementedError()
        else:
            return self.answer('Никто пока что не подключился')
