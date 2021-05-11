from http import HTTPStatus

from flask import Flask, jsonify, request

app = Flask(__name__)
app.debug = True

board = []
board_size = len(board)
ships = []


@app.route('/battleship', methods=['POST'])
def create_battleship_game():
    params = request.get_json()
    g_board = create_game_board(10, 10)
    global board_size
    board_size = len(g_board)
    for param in params.get("ships"):
        valid = validate_and_place_ship(param.get("x"), param.get("y"), param.get("size"), param.get("direction"))
        if not valid:
            return jsonify({"message": "Problem Detected"}), HTTPStatus.BAD_REQUEST
    preview_board()
    return jsonify(board), HTTPStatus.OK


def create_game_board(x_axis: int, y_axis: int) -> list:
    global board
    for i in range(x_axis):
        row = []
        for j in range(y_axis):
            row.append("_")
        board.append(row)
    return board


def validate_and_place_ship(x_axis: int, y_axis: int, size: int, direction: str):
    global board
    x_axis_final = x_axis + 1
    y_axis_final = y_axis + 1
    if direction == "V":
        if y_axis - size < 0 and x_axis + size >= board_size:
            return False
        else:
            y_axis_final = y_axis + size

    if direction == "H":
        if x_axis - size < 0 and x_axis + size > board_size:
            return False
        else:
            x_axis_final = x_axis + size
    try:
        ship_start_location = board[x_axis][y_axis]
        ship_final_location = board[x_axis_final][y_axis_final]
    except IndexError:
        return False
    return try_place_ship(x_axis, y_axis, x_axis_final, y_axis_final)


def try_place_ship(x_axis, y_axis, final_x_axis, final_y_axis):
    for i in range(x_axis, final_x_axis):
        for j in range(y_axis, final_y_axis):
            if board[i][j] != "_":
                return False
            board[i][j] = str("0")
        ships.append([x_axis, y_axis, final_x_axis, final_y_axis])
    return True


def preview_board():
    global board
    x = [i for i in range(len(board))]
    for row in range(len(board)):
        print(x[row], end=") ")
        for col in range(len(board[row])):
            if board[row][col] == "O":
                if app.debug:
                    print("O", end=" ")
                else:
                    print("_", end=" ")
            else:
                print(board[row][col], end=" ")
        print("")

    print("  ", end=" ")
    for i in range(len(board[0])):
        print(str(i), end=" ")
    print("")


@app.route('/battleship', methods=['PUT'])
def shot():
    params = request.get_json()
    x = params.get("x")
    y = params.get("y")
    is_valid = validate_shot(x, y)
    if not is_valid:
        return jsonify({"result": "Problem Detected"}), HTTPStatus.BAD_REQUEST
    result = shot_ship(x, y)
    return jsonify({"result": result}), HTTPStatus.OK


def validate_shot(x, y):
    try:
        shot_position = board[x][y]
    except IndexError:
        return False
    return True


def check_ship_sunk(x, y):
    global ships
    global board
    for ship in ships:
        x_axis = ship[0]
        y_axis = ship[1]
        x_axis_final = ship[2]
        y_axis_final = ship[3]
        if x_axis <= x <= x_axis_final and y_axis <= y <= y_axis_final:
            for i in range(x_axis, x_axis_final):
                for j in range(y_axis, y_axis_final):
                    if board[i][j] != "X":
                        return False
            return True


def shot_ship(x, y):
    if board[x][y] == "0":
        board[x][y] = "X"
        is_sunk = check_ship_sunk(x, y)
        if is_sunk:
            result = "SINK"
            return result
        result = "HIT"
    elif board[x][y] == "X":
        result = "HIT"
    else:
        result = "WATER"
    return result


@app.route('/battleship', methods=['DELETE'])
def delete_battleship_game():
    global board
    global board_size
    global ships
    board = []
    board_size = len(board)
    ships = []
    return jsonify({"result": "Game Deleted"}), HTTPStatus.OK
