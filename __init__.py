from __future__ import unicode_literals

import json
import logging
from vcy import core as vcy_core
from vcy.entities import InputMessage

from flask import Flask, request
app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)

sessionStorage = {}
vcy_core.init(True)


@app.route("/", methods=['GET'])
def hello():
    return "hello world!"


# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])
def main():
    # Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )


# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    user_id = req['session']['user_id']
    # _quit = False
    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.
        message = InputMessage(user_id, 'start', True)

        answer = vcy_core.process_input(message)
        res['response']['text'] = answer.message
        return

    message_text = req['request']['command']
    message = InputMessage(user_id, message_text)

    answer = vcy_core.process_input(message)
    res['response']['text'] = answer.message
    return
    



if __name__ == '__main__':
    app.run(port=8000)
