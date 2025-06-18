from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room
import uuid

app = Flask(__name__, static_url_path='/static')
socketio = SocketIO(app, cors_allowed_origins="*")

games = {}

def create_new_board():
    return [[" " for _ in range(3)] for _ in range(3)]

def check_winner(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != " ":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != " ":
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]
    return None

def is_tie(board):
    return all(cell != " " for row in board for cell in row)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/game/<room>")
def game(room):
    return render_template("game.html", room=room)

@app.route("/create")
def create():
    room = str(uuid.uuid4())[:6]
    games[room] = {
        "board": create_new_board(),
        "turn": "X",
        "winner": None,
        "tie": False
    }
    return {"room": room}

@socketio.on("join")
def on_join(data):
    room = data["room"]
    join_room(room)
    emit("update", games[room], room=room)

@socketio.on("move")
def on_move(data):
    room = data["room"]
    row, col = data["row"], data["col"]
    game = games.get(room)
    if game and game["board"][row][col] == " " and not game["winner"]:
        game["board"][row][col] = game["turn"]
        game["winner"] = check_winner(game["board"])
        game["tie"] = is_tie(game["board"]) and not game["winner"]
        if not game["winner"]:
            game["turn"] = "O" if game["turn"] == "X" else "X"
        emit("update", game, room=room)

@socketio.on("reset")
def on_reset(data):
    room = data["room"]
    if room in games:
        games[room] = {
            "board": create_new_board(),
            "turn": "X",
            "winner": None,
            "tie": False
        }
        emit("update", games[room], room=room)

if __name__ == "__main__":
    socketio.run(app, debug=True)