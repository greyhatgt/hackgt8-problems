import requests
import zlib
import json
import base64

base_url = "http://127.0.0.1:5000"

s = requests.session()

s.get(base_url + "/game")

# Manually, ignoring signatures
session_data = json.loads(zlib.decompress(base64.urlsafe_b64decode(s.cookies["session"] + "===")))
secret_board = session_data['secret_board']

for y in range(5):
    for x in range(5):
        if secret_board[x][y] == 'x':
            s.get(base_url + "/game/{}/{}".format(x, y))

print(s.get(base_url + "/game").text)
