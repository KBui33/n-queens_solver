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

#moves to be implemented once game state looks functional

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
    game.players = players
    return

@socketio.on("raise")
def raiseMove(val):
    #TODO: add in the val to the request.sid's player's bet, remove it from their money
    players = game.players

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

#this is the call to initialize the game and start the first round
@socketio.on("start_game")
def start_game():
    global game, clients
    game.initGame()
    print(game.deck)
    #determine the total # of players before starting    
    game.gameLoop()

    #emit scoreboard to all players
    emit("scoreboard", game.getScoreboard(), room=clients)
    #determine the total # of players before starting    
    # result = game.start_game()
    # if(result == True):
    #     #game has run as normal
    #     return
    # else:
    #     emit("notEnoughPlayers", room=request.sid)

#a call whenever a new connection is established. this does not mean that the current connection is a player
@socketio.on("connect")
def connected():
    """event listener when client connects to the server"""
    for p in game.players:
        if(p.id == request.sid):
            #resume their current progress (later)
            return
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

#a call whenever the player attempts to join the game. They just provide their wager, and their name to join
@socketio.on("join")
def join(wager, name):
    #add in try-catch for casting wager in case of user input error (shouldnt happen tho)
    num = float(wager)
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
#a call whenever a connection is lost from the server
@socketio.on("disconnect")
def disconnected():
    """event listener when client disconnects to the server"""
    #remove this player and its connection from the list of players
    n = game.removePlayer(request.sid)
    if(n == False):
        print("Player failed to be removed")
        return
    clients.remove(request.sid)
    print("user {} disconnected", n)
    emit("disconnect",{"data":{"id":request.sid, "name":n, "numPlayers":game.numPlayers}}, broadcast=True)

@socketio.on("ready_player")
def ready_player(data):
    print(data)
    
    game.setPlayerReadyStatus(data["playerName"], data["status"])

# import game


def send_message(client_id, data):
    socketio.emit('output', data, room=client_id)
    print('sending message "{}" to client "{}".'.format(data, client_id))
if __name__ == '__main__':
    socketio.run(app, debug=True,port=5001)
