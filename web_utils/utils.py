import requests
import json


with open('web_utils/config.json', 'r') as fin:
    config = json.load(fin)

oauth_token = config['oauth_token']
skill_id = config['skill_id']


def upload_picture(path_to_picture):
    headers = {
        'Authorization': f'OAuth {oauth_token}'
        }

    files = {
        'file': open(path_to_picture, 'rb'),
    }
    url = f'https://dialogs.yandex.net/api/v1/skills/{skill_id}/images'
    response = requests.post(url, headers=headers, files=files)

    picture_id = response.json()['image']['id']
    return picture_id
