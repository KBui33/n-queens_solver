from flask import Flask, request
from flask_cors import CORS
from queens import nQueens, WallNQueens

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


# @app.route("/")
# def hello_world():
#     print("got soething")
#     return {"bb": "Hello, World!"}


@app.route("/combo", methods=['POST'])
def get_combo():
    json = None
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
    else:
        return 'Content-Type not supported!'

    # This one does not consider the walls
    # queen = nQueens(json["n"])
    # combo = queen.solve(4)
    # print(combo)
    # board = queen.boardFromString(combo)
    # print(board)

    # This one considers walls
    wallQueen = WallNQueens(json["n"], json["rightWall"], json["bottomWall"])
    boardStr = wallQueen.solve(7)
    board = wallQueen.boardFromString(boardStr)
    return board


if __name__ == '__main__':
    app.run(debug=True)
