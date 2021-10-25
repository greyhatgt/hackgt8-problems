from flask import Flask, render_template_string, request, session, redirect, url_for
import random
import secrets
from create_board import generate_choices

app = Flask(__name__)

app.secret_key = secrets.token_bytes(16)

with open("./flag.txt", "r") as f:
    flag = f.read()


def install_game():
    secret_board = [
        ["0", "0", "0", "0", "0"],
        ["0", "0", "0", "0", "0"],
        ["0", "0", "0", "0", "0"],
        ["0", "0", "0", "0", "0"],
        ["0", "0", "0", "0", "0"],
    ]

    choices = generate_choices()
    print(choices)

    for choice in choices:
        x = choice[0]
        y = choice[1]
        secret_board[x][y] = "x"
        for (xmod, ymod) in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            try:
                secret_board[x + xmod][y + ymod] = str(
                    int(secret_board[x + xmod][y + ymod]) + 1
                )
            except (IndexError, ValueError):
                pass

    session["secret_board"] = secret_board
    session["game"] = [
        ["?", "?", "?", "?", "?"],
        ["?", "?", "?", "?", "?"],
        ["?", "?", "?", "?", "?"],
        ["?", "?", "?", "?", "?"],
        ["?", "?", "?", "?", "?"],
    ]
    session["bombs_found"] = 0
    session["move_count"] = 0


@app.route("/game/<int:x>/<int:y>")
def make_move(x, y):
    session["game"][x][y] = session["secret_board"][x][y]
    if session["secret_board"][x][y] == "x":
        session["bombs_found"] += 1

    session["move_count"] += 1

    session.modified = True

    if session["bombs_found"] == 4:
        if session["move_count"] == 4:
            return '<p>You won! {}</p><p><a href="/reset">reset</a></p>'.format(flag)
        return '<p>You won! Win in 4 moves to get the flag.</p><p><a href="/reset">reset</a></p>'

    return redirect("/game")


@app.route("/game")
def play_game():
    if "game" not in session:
        install_game()

    if session["bombs_found"] == 4:
        if session["move_count"] == 4:
            return '<p>You won! {}</p><p><a href="/reset">reset</a></p>'.format(flag)
        return '<p>You won! Win in 4 moves to get the flag.</p><p><a href="/reset">reset</a></p>'

    return render_template_string(
        """
<html>
<body>
<table>
<thead>
  <tr>
    <td><a href='/game/0/0'>{{ session['game'][0][0] }}</a></td>
    <td><a href='/game/0/1'>{{ session['game'][0][1] }}</a></td>
    <td><a href='/game/0/2'>{{ session['game'][0][2] }}</a></td>
    <td><a href='/game/0/3'>{{ session['game'][0][3] }}</a></td>
    <td><a href='/game/0/4'>{{ session['game'][0][4] }}</a></td>
  </tr>
  <tr>
    <td><a href='/game/1/0'>{{ session['game'][1][0] }}</a></td>
    <td><a href='/game/1/1'>{{ session['game'][1][1] }}</a></td>
    <td><a href='/game/1/2'>{{ session['game'][1][2] }}</a></td>
    <td><a href='/game/1/3'>{{ session['game'][1][3] }}</a></td>
    <td><a href='/game/1/4'>{{ session['game'][1][4] }}</a></td>
  </tr>
  <tr>
    <td><a href='/game/2/0'>{{ session['game'][2][0] }}</a></td>
    <td><a href='/game/2/1'>{{ session['game'][2][1] }}</a></td>
    <td><a href='/game/2/2'>{{ session['game'][2][2] }}</a></td>
    <td><a href='/game/2/3'>{{ session['game'][2][3] }}</a></td>
    <td><a href='/game/2/4'>{{ session['game'][2][4] }}</a></td>
  </tr>
  <tr>
    <td><a href='/game/3/0'>{{ session['game'][3][0] }}</a></td>
    <td><a href='/game/3/1'>{{ session['game'][3][1] }}</a></td>
    <td><a href='/game/3/2'>{{ session['game'][3][2] }}</a></td>
    <td><a href='/game/3/3'>{{ session['game'][3][3] }}</a></td>
    <td><a href='/game/3/4'>{{ session['game'][3][4] }}</a></td>
  </tr>
  <tr>
    <td><a href='/game/4/0'>{{ session['game'][4][0] }}</a></td>
    <td><a href='/game/4/1'>{{ session['game'][4][1] }}</a></td>
    <td><a href='/game/4/2'>{{ session['game'][4][2] }}</a></td>
    <td><a href='/game/4/3'>{{ session['game'][4][3] }}</a></td>
    <td><a href='/game/4/4'>{{ session['game'][4][4] }}</a></td>
  </tr>
<p><a href="/reset">reset</a></p>
</body>
</html>
            {% if session['email'] %}
                <h1>Welcome {{ session['email'] }}!</h1>
            {% else %}
                <h1></h1>
            {% endif %}
        """
    )


@app.route("/reset")
def reset():
    session["a_lot"] = "A" * 1000
    session.pop("game", default=None)
    return redirect("/game")


@app.route("/")
def index():
    return redirect("/game")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
