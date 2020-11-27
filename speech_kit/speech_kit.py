import time, jwt # IAM token
import argparse, requests # synthesize


OAUTH_TOKEN = 'AgAAAAAUF-tyAATuwV6y7F1yf04spZq-PDlWM4E'
IAM_TOKEN, EXPIRES_IAM_TOKEN = create_token()
FOLDER_ID = 'b1gtpi0rn6jj5s9k7o6o'

URL_REC = 'https://stt.api.cloud.yandex.net/speech/v1/stt:recognize'
URL_SYN = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
URL_TOK = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'


def create_token():
    params = {'yandexPassportOauthToken': OAUTH_TOKEN}
    response = requests.post(URL_TOK, params=params)
    decode_response = response.content.decode('UTF-8')
    response = json.loads(decode_response)
    iam_token = response.get('iamToken')
    expires_iam_token = text.get('expriresAt')
    
    return iam_token, expires_iam_token

def recognize(path_audio):
    with open(path_audio, "rb") as f:
        request_bytes = f.read()

    # в поле заголовка передаем IAM_TOKEN:
    headers = {'Authorization': f'Bearer {IAM_TOKEN}'}
    
    # остальные параметры:
    params = {
        'lang': 'ru-RU',
        'folderId': ID_FOLDER,
        'sampleRateHertz': 48000,
    }

    response = requests.post(URL_REC, params=params, headers=headers, data=request_bytes)
    
    # бинарные ответ доступен через response.content, декодируем его:
    decode_resp = response.content.decode('UTF-8')
    
    # и загрузим в json, чтобы получить текст из аудио:
      
    text = json.loads(decode_resp)
    
    return text

def synthesize(iam_token, text):
    headers = {'Authorization': f'Bearer {IAM_TOKEN}'}

    data = {
        'text': text,
        'lang': 'ru-RU',
        'folderId': FOLDER_ID
    }

    response = requests.post(URL_SYN, headers=headers, data=data)
    
    return response

    #with open(args.output, "wb") as f:
        #for audio_content in synthesize(args.folder_id, args.token, args.text):
            #f.write(audio_content)