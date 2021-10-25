import requests
import zlib
import json
import base64
from copy import deepcopy
import random

random.seed(1337)
# Note that the solve isn't technically complete, since it only reveals that it can find a match out of the
# first 100 generations. It does prove that an actual solve is possible though.

def create_session():
    session = {}

    secret_board = [
        ['0','0','0','0','0'],
        ['0','0','0','0','0'],
        ['0','0','0','0','0'],
        ['0','0','0','0','0'],
        ['0','0','0','0','0']
    ]
    choices = []
    for i in range(4):
        choice = (random.randint(0, 4), random.randint(0, 4))
        while choice in choices:
            choice = (random.randint(0, 4), random.randint(0, 4))
        choices.append(choice)

    for choice in choices:
        x = choice[0]
        y = choice[1]
        secret_board[x][y] = 'x'
        # This currently wraps around, not exactly sure why, but we can make that work.
        for (xmod, ymod) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            try:
                secret_board[x + xmod][y + ymod] = str(int(secret_board[x + xmod][y + ymod]) + 1)
            except (IndexError, ValueError):
                pass

    session['secret_board'] = secret_board
    session['game'] = [
        ['?','?','?','?','?'],
        ['?','?','?','?','?'],
        ['?','?','?','?','?'],
        ['?','?','?','?','?'],
        ['?','?','?','?','?']
    ]
    session['bombs_found'] = 0
    session['move_count'] = 0

    return choices

base_url = "http://127.0.0.1:5000"

# Create a bunch of games (in their own sessions) at the same time; they will have nearby rng states.
# View results of games
# Guess rng state of specific game

possible_boards = []
for i in range(20):
    random.seed(1337)
    for j in range(i):
        random.getrandbits(32)
    possible_boards.append(create_session())
    print(possible_boards[i])
sessions = []

for i in range(10):
    s = requests.session()
    s.get(base_url + "/game")
    sessions.append(s)

locations = []

session_uuid = s.cookies['session']
for j in range(2):
    s = sessions[j]
    locations.append([])
    for i in range(4):
        match = False
        for y in range(5):
            for x in range(5):
                saved_cookies = deepcopy(s.cookies)
                resp = s.get(base_url + "/game/{}/{}".format(x, y)).text
                if resp.count('x') > i or 'hackgt8' in resp:
                    locations[j].append((x, y))
                    match = True
                    break
                else:
                    s.cookies = saved_cookies
            if match:
                break

print("--")

print(locations)

for board in possible_boards:
    count = 0
    for i in range(len(board)):
        if board[i] in locations[0]:
            count += 1
    if count == 4:
        print("MATCH!")
        print(board)
        print(locations[0])
