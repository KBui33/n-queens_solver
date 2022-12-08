from flask import Flask, request
from flask_cors import CORS
from queens import nQueens

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

    print(json)
    return "it worked"


if __name__ == '__main__':
    app.run(debug=True)
