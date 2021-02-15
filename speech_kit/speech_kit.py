import time, jwt # IAM token
import argparse, requests # synthesize
import json

OAUTH_TOKEN = 'AgAAAAAUF-tyAATuwV6y7F1yf04spZq-PDlWM4E'
FOLDER_ID = 'b1gtpi0rn6jj5s9k7o6o'

URL_REC = 'https://stt.api.cloud.yandex.net/speech/v1/stt:recognize'
URL_SYN = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
URL_TOK = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'

PATH_AUDIO = 'tmp/AUDIO.ogg'
PATH_IAM = 'tmp/IAM_TOKEN'

def create_token():
    params = {'yandexPassportOauthToken': OAUTH_TOKEN}
    response = requests.post(URL_TOK, params=params)
    decode_response = response.content.decode('UTF-8')
    response = json.loads(decode_response)
    iam_token = response.get('iamToken')
    expires_iam_token = response.get('expriresAt')

    with open(PATH_IAM, 'w') as f:
        f.write(iam_token)
    return iam_token

def recognize(bytes):
    with open(PATH_IAM, 'r') as f:
        iam_token = f.read()

    if len(bytes) == 0:
        with open(PATH_AUDIO, "rb") as f:
            request_bytes = f.read()
    else:
        request_bytes = bytes

    if len(iam_token) == 0:
        raise ValueError('IAM_TOKEN not found')
    if len(request_bytes) == 0:
        raise ValueError('AUDIO bytes not found')

    # в поле заголовка передаем IAM_TOKEN:
    headers = {'Authorization': 'Bearer ' + iam_token}

    # остальные параметры:
    params = {
        'lang': 'ru-RU',
        'folderId': FOLDER_ID,
        'sampleRateHertz': 48000,
    }

    response = requests.post(URL_REC, params=params, headers=headers, data=request_bytes)

    # бинарные ответ доступен через response.content, декодируем его:
    decode_resp = response.content.decode('UTF-8')

    # и загрузим в json, чтобы получить текст из аудио:
    text = json.loads(decode_resp)

    return text

def synthesize(text):
    with open(PATH_IAM, 'r') as f:
        iam_token = f.read()

    headers = {'Authorization': 'Bearer ' + iam_token}

    data = {
        'text': text,
        'lang': 'ru-RU',
        'folderId': FOLDER_ID
    }

    response = requests.post(URL_SYN, headers=headers, data=data)
    with open(PATH_AUDIO, 'wb') as f:
        f.write(response.content)
    return response
