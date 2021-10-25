Name: Reverse Minesweeper 1
Category: Web
Difficulty: Hard
Author: Nathan Peercy / nsnc (Praetorian)
Description: Well... version 2 was insecure I guess. Hopefully storing sessions server-side will be enough.
Flag: `hackgt8{n3v3r_3v3r_us3_4_c0nst4nt_s33d_also_mersenne_twister_is_insecure}`

Note:
- share `app.py`, but do not share `create_board.py`
- The last hint will make the challenge significantly easier. Part of the challenge
is identifying how the choices are generated. If people are stuck though, it may be
necessary to reveal the algorithm.

Hints (reveal these if there's not many solves or it otherwise makes sense):
- How is random used? How are boards generated? Can you exploit that somehow?
- The first board generated after starting the app had mines at: (4, 4), (2, 4), (4, 1), (2, 3).
- The source code for `generate_choices` is:
```
def generate_choices():
    choices = []
    for i in range(4):
        choice = (random.randint(0, 4), random.randint(0, 4))
        while choice in choices:
            choice = (random.randint(0, 4), random.randint(0, 4))
        choices.append(choice)
    return choices
```
