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

@app.route('/blind')
def blind():
    #return the game's blind
    if(game == None):
        return {"error": "game not initialzied"}
    return {"success":game.blind}
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
def start_game():
    global game, clients
    game.initGame();
    #determine the total # of players before starting    
    result = game.start_game();
    if(result == True):
        #game has run as normal
        return
    else:
        emit("notEnoughPlayers", room=request.sid)

@socketio.on("connect")
def connected():
    """event listener when client connects to the server"""
    for p in game.players:
        if(p.id == request.sid):
            #resume their current progress (later)
            return
    clients.append(request.sid)
    print("client has connected")
    socketio.emit("connect",{"data":{"id":request.sid, "numPlayers":game.numPlayers}}, broadcast=True)

#
@socketio.on("join")
def join(wager, name):
    #add in try-catch for casting wager in case of user input error (shouldnt happen tho)
    num = float(wager)
    print(type(name))
    if(num < 0):
        #emit back that the user must enter a number > 0
        emit("inputError", "wLessZero", room=request.sid)
        return
    if(num < game.blind):
        #emit back to the user that they need at least the value of the blind
        emit("inputError", "lessThanBlind", room=request.sid)
        return
    p = Player(name, request.sid, num)
    game.addPlayer(p)
    
    #emit to all other players that a new player has joined
    emit("numPlayers", game.numPlayers, room=clients)
    #emit to the current player that their join was successful
    return

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
