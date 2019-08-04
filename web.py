import json
import logging
from vcy import core as vcy_core
from vcy.entities import InputMessage

from flask import Flask, request

from web_utils.utils import upload_picture

app = Flask(__name__)


logging.basicConfig(level=logging.DEBUG)

sessionStorage = {}
vcy_core.init(True)


@app.route('/', methods=['GET'])
def hello():
    return 'hello world!'


@app.route('/', methods=['POST'])
def main():
    logging.info('Request: %r', request.json)

    response = {
        'version': request.json['version'],
        'session': request.json['session'],
        'response': {
            'end_session': False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )


def handle_dialog(req, res):
    # TODO: test two players with different session_id
    session_id = req['session']['session_id']

    if req['session']['new']:
        message = InputMessage(session_id, 'start', True)

        answer = vcy_core.process_input(message)
        res['response']['text'] = answer.message
        return

    message_text = req['request']['command']
    message = InputMessage(session_id, message_text)

    answer = vcy_core.process_input(message)
    res['response']['text'] = answer.message

    if answer.image:
        image_id = upload_picture(answer.image.image_path)

        res['response']['card'] = {
            'type': 'BigImage',
            'image_id': image_id,
            'title': answer.image.title,
            'description': answer.image.description
        }


if __name__ == '__main__':
    app.run(port=8000)
