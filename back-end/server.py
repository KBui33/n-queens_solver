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
game = Game();

@socketio.on("check")
def check():
    players = game.players
    #assign the proper move to the current player
    for p in players:
        if(p.id == request.sid):
            p.move = "check"
    
    game.players = players
    return

@socketio.on("fold")
def fold():
    players = game.players
    
    count = 0
    winner = None
    for p in players:
        #assign the proper move to the current player
        if(p.id == request.sid):
            p.move = 'fold'
        if(p.move != "fold"):
            count += 1
            winner = p
    
    #check to see if there is exactly 1 player remaining
    if(count <= 1):
        #end the round
        #TODO: define ending a round
        game.endRound(winner)
        return

    #emit all other players of your fold

    #assign the list of players back to the game
    game.players = players;
    return

@socketio.on("raise")
def raiseMove(val):
    #TODO: add in the val to the request.sid's player's bet, remove it from their money
    players = game.players;

    if(val < game.blind):
        #the user must bet at least the big blind to raise
        return
    elif(val > game.pot):
        #emit back to user that the maximum allowed bet is the current pot
        return
    for p in players:
        if(p.id == request.sid):
            if(p.wager(val, game)):
                #emit to all other players that a wager has been made
                return
            else:
                #emit back to player that they cannot wager this amount
                return

            break
    return

@socketio.on("call")
def call():
    players = game.players;
    for p in players:
        if(p.id == request.sid):
            if(p.wager(int(game.blind/2), game)):
                #emit to all other players that a call has been made
                return
            else:
                #the player must add more money to participate in the round
                return

@socketio.on("start_game")
def start_game(data):
    global game, clients
    game.initGame();
    print(game.deck)
    #determine the total # of players before starting    
    game.start_game();

@socketio.on("connect")
def connected():
    """event listener when client connects to the server"""
    #add this player to the list of players
    p = Player("tempName", request.sid, 1000);
    print(request.sid)
    game.addPlayer(p)
    clients.append(request.sid)
    print("client has connected")
    socketio.emit("connect",{"data":{"id":request.sid, "numPlayers":game.numPlayers}}, broadcast=True)

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

def send_message(client_id, data):
    socketio.emit('output', data, room=client_id)
    print('sending message "{}" to client "{}".'.format(data, client_id))
if __name__ == '__main__':
    socketio.run(app, debug=True,port=5001)
