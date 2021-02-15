import time, jwt # IAM token
import argparse, requests # synthesize

SERVICE_ACCOUNT_ID = "ajep4v4gl845b2uqal66"
KEY_ID = "aje77ttk8bl305renr7e" # ID ресурса Key, который принадлежит сервисному аккаунту.

FOLDER_ID = "b1gtpi0rn6jj5s9k7o6o"


def IAM_token():
    with open("keys/speechKey", 'r') as private:
        private_key = private.read() # Чтение закрытого ключа из файла.

    now = int(time.time())
    payload = {
            'aud': 'https://iam.api.cloud.yandex.net/iam/v1/tokens',
            'iss': SERVICE_ACCOUNT_ID,
            'iat': now,
            'exp': now + 360
            }

    # Формирование JWT.
    encoded_token = jwt.encode(
        payload,
        private_key,
        algorithm='PS256',
        headers={'kid': KEY_ID})
    
    # Обмен JWT на iam
    url = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
    
    headers = {
        'Content-Type: application/json'
    }
    
    data = {
        'jwt': encoded_token
    }
    
    with requests.post(url, headers=headers, data=data, stream=True) as resp:
        if resp.status_code != 200:
            raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))

        for chunk in resp.iter_content(chunk_size=None):
            yield chunk

def synthesize(iam_token, text):
    url = 'https://tts.api.cloud.yandex.net/speech/v1/tts:synthesize'
    
    headers = {
        'Authorization': 'Bearer ' + iam_token,
    }

    data = {
        'text': text,
        'lang': 'ru-RU',
        'folderId': FOLDER_ID
    }

    with requests.post(url, headers=headers, data=data, stream=True) as resp:
        if resp.status_code != 200:
            raise RuntimeError("Invalid response received: code: %d, message: %s" % (resp.status_code, resp.text))

        for chunk in resp.iter_content(chunk_size=None):
            yield chunk


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--token", required=True, help="IAM token")
    parser.add_argument("--folder_id", required=True, help="Folder id")
    parser.add_argument("--text", required=True, help="Text for synthesize")
    parser.add_argument("--output", required=True, help="Output file name")
    args = parser.parse_args()

    with open(args.output, "wb") as f:
        for audio_content in synthesize(args.folder_id, args.token, args.text):
            f.write(audio_content)
