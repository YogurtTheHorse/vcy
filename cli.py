from vcy import core as vcy_core
from vcy.entities import InputMessage


def main():
    vcy_core.init(True)

    session_id = input('Please write your unique id: ')
    _quit = False

    message = InputMessage(session_id, 'start', True)

    while not _quit:
        answer = vcy_core.process_input(message)
        print(answer.message)

        message_text = input('> ')
        message = InputMessage(session_id, message_text)


if __name__ == '__main__':
    main()
