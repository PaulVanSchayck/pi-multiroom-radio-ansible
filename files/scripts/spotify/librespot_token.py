import json
import os
import time
from subprocess import check_output


def get_token():
    output = check_output(["/home/pi/get_token", "/var/lib/raspotify", "c1a475bba9294ee7bc4618cc8f711f6b"],
                          encoding='UTF-8')

    return output.strip()


def store_token(token, username):
    with open('/tmp/spotipy-token.json', 'w+') as f:
        json.dump({'token': token, 'username': username, 'valid_until': time.time() + 3600}, f)


def token():
    with open('/var/lib/raspotify/credentials.json') as f:
        credentials = json.load(f)

    t = None

    if os.path.exists('/tmp/spotipy-token.json'):
        with open('/tmp/spotipy-token.json') as f:
            token_data = json.load(f)
        if token_data['username'] == credentials['username'] and token_data['valid_until'] > time.time():
            t = token_data['token']

    if t is None:
        t = get_token()
        store_token(t, credentials['username'])

    return t
