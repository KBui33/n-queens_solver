from flask import Flask, request,jsonify
from flask_socketio import SocketIO,emit
from flask_cors import CORS
from game import Game
from player import Player

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app,resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app,cors_allowed_origins="*")

clients = []
game = Game()

@socketio.on("start_game")
def start_game(data):
    global game, clients
    game.initGame()
    print(game.deck)
    #determine the total # of players before starting    
    game.gameLoop()

@socketio.on("connect")
def connected():
    """event listener when client connects to the server"""
    #add this player to the list of players
    clients.append(request.sid)
    print("client has connected")


@socketio.on("set_name")
def set_name(name):
    # print(name)
    p = Player(name, request.sid, 1000)
    print(request.sid)
    game.addPlayer(p)
    
    game.printPlayers()
    # return {"data":{"id":request.sid, "numPlayers":game.numPlayers}}
    socketio.emit("num_players",{"data":{"id":request.sid, "numPlayers":game.numPlayers}}, broadcast=True)

@socketio.on('data')
def handle_message(data):
    """event listener when client types a message"""
    print("data from the front end: ",str(data))
    emit("data",{'data':data,'id':request.sid},broadcast=True)

@socketio.on("disconnect")
def disconnected():
    """event listener when client disconnects to the server"""
    #remove this player and its connection from the list of players
    game.removePlayer(request.sid)
    clients.remove(request.sid)
    print("user disconnected")
    emit("disconnect",{"data":{"id":request.sid, "numPlayers":game.numPlayers}}, broadcast=True)

@socketio.on("ready_player")
def ready_player(client_id):
    # print(client_id)
    
    return 

def send_message(client_id, data):
    socketio.emit('output', data, room=client_id)
    print('sending message "{}" to client "{}".'.format(data, client_id))
if __name__ == '__main__':
    socketio.run(app, debug=True,port=5001)
