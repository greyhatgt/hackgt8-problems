from flask import Flask, render_template_string, request, session, redirect, url_for
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad, unpad
import random
import secrets
import json
from create_board import generate_choices

app = Flask(__name__)

# ECB is good enough :) There might be some trick, but that's harder than the other solve.
# Use your ECB knowledge if you want to.
app.secret_key = secrets.token_bytes(16)

def session_get(key):
    if session.get("session") == None:
        decrypted_session = {}
        cipher = AES.new(app.secret_key, AES.MODE_ECB)
        session["session"] = cipher.encrypt(pad(json.dumps(decrypted_session).encode('utf8'), AES.block_size))

    try:
        cipher = AES.new(app.secret_key, AES.MODE_ECB)
        decrypted_session = json.loads(unpad(cipher.decrypt(session['session']), AES.block_size))
        return decrypted_session[key]
    except KeyError:
        return None

def session_set(key, val):
    if session.get("session") == None:
        decrypted_session = {}
        cipher = AES.new(app.secret_key, AES.MODE_ECB)
        session["session"] = cipher.encrypt(pad(json.dumps(decrypted_session).encode('utf8'), AES.block_size))
    
    cipher = AES.new(app.secret_key, AES.MODE_ECB)
    decrypted_session = json.loads(unpad(cipher.decrypt(session['session']), AES.block_size))
    decrypted_session[key] = val
    session["session"] = cipher.encrypt(pad(json.dumps(decrypted_session).encode('utf8'), AES.block_size))
    session.modified = True


with open('./flag.txt', 'r') as f:
    flag = f.read()

def install_game():
    secret_board = [
        ['0','0','0','0','0'],
        ['0','0','0','0','0'],
        ['0','0','0','0','0'],
        ['0','0','0','0','0'],
        ['0','0','0','0','0']
    ]

    choices = generate_choices()
    print(choices)

    for choice in choices:
        x = choice[0]
        y = choice[1]
        secret_board[x][y] = 'x'
        for (xmod, ymod) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            try:
                secret_board[x + xmod][y + ymod] = str(int(secret_board[x + xmod][y + ymod]) + 1)
            except (IndexError, ValueError):
                pass

    session_set('secret_board', secret_board)
    session_set('game', [
        ['?','?','?','?','?'],
        ['?','?','?','?','?'],
        ['?','?','?','?','?'],
        ['?','?','?','?','?'],
        ['?','?','?','?','?']
    ])
    session_set('bombs_found', 0)
    session_set('move_count', 0)


@app.route('/game/<int:x>/<int:y>')
def make_move(x, y):
    updated_board = session_get('game')
    updated_board[x][y] = session_get('secret_board')[x][y]
    session_set('game', updated_board)

    if session_get('secret_board')[x][y] == 'x':
        session_set('bombs_found',  session_get('bombs_found') + 1)

    session_set('move_count',  session_get('move_count') + 1)

    if session_get('bombs_found') == 4:
        if session_get('move_count') == 4:
            return '<p>You won! {}</p><p><a href="/reset">reset</a></p>'.format(flag)
        return '<p>You won! Win in 4 moves to get the flag.</p><p><a href="/reset">reset</a></p>'

    return redirect('/game')

@app.route('/game')
def play_game():
    if 'session' not in session:
        install_game()

    if session_get('bombs_found') == 4:
        if session_get('move_count') == 4:
            return '<p>You won! {}</p><p><a href="/reset">reset</a></p>'.format(flag)
        return '<p>You won! Win in 4 moves to get the flag.</p><p><a href="/reset">reset</a></p>'

    return render_template_string("""
<html>
<body>
<table>
<thead>
  <tr>
    <td><a href='/game/0/0'>{{ session_get('game')[0][0] }}</a></td>
    <td><a href='/game/0/1'>{{ session_get('game')[0][1] }}</a></td>
    <td><a href='/game/0/2'>{{ session_get('game')[0][2] }}</a></td>
    <td><a href='/game/0/3'>{{ session_get('game')[0][3] }}</a></td>
    <td><a href='/game/0/4'>{{ session_get('game')[0][4] }}</a></td>
  </tr>
  <tr>
    <td><a href='/game/1/0'>{{ session_get('game')[1][0] }}</a></td>
    <td><a href='/game/1/1'>{{ session_get('game')[1][1] }}</a></td>
    <td><a href='/game/1/2'>{{ session_get('game')[1][2] }}</a></td>
    <td><a href='/game/1/3'>{{ session_get('game')[1][3] }}</a></td>
    <td><a href='/game/1/4'>{{ session_get('game')[1][4] }}</a></td>
  </tr>
  <tr>
    <td><a href='/game/2/0'>{{ session_get('game')[2][0] }}</a></td>
    <td><a href='/game/2/1'>{{ session_get('game')[2][1] }}</a></td>
    <td><a href='/game/2/2'>{{ session_get('game')[2][2] }}</a></td>
    <td><a href='/game/2/3'>{{ session_get('game')[2][3] }}</a></td>
    <td><a href='/game/2/4'>{{ session_get('game')[2][4] }}</a></td>
  </tr>
  <tr>
    <td><a href='/game/3/0'>{{ session_get('game')[3][0] }}</a></td>
    <td><a href='/game/3/1'>{{ session_get('game')[3][1] }}</a></td>
    <td><a href='/game/3/2'>{{ session_get('game')[3][2] }}</a></td>
    <td><a href='/game/3/3'>{{ session_get('game')[3][3] }}</a></td>
    <td><a href='/game/3/4'>{{ session_get('game')[3][4] }}</a></td>
  </tr>
  <tr>
    <td><a href='/game/4/0'>{{ session_get('game')[4][0] }}</a></td>
    <td><a href='/game/4/1'>{{ session_get('game')[4][1] }}</a></td>
    <td><a href='/game/4/2'>{{ session_get('game')[4][2] }}</a></td>
    <td><a href='/game/4/3'>{{ session_get('game')[4][3] }}</a></td>
    <td><a href='/game/4/4'>{{ session_get('game')[4][4] }}</a></td>
  </tr>
<p><a href="/reset">reset</a></p>
</body>
</html>
            {% if session['email'] %}
                <h1>Welcome {{ session['email'] }}!</h1>
            {% else %}
                <h1></h1>
            {% endif %}
        """, session_get=session_get)

@app.route('/reset')
def reset():
    session.pop('session', default=None)
    return redirect('/game')

@app.route('/')
def index():
    return redirect('/game')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=False)
