from flask import Flask
from flask import request, session
from flask_session import Session
from game import *


app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

game = Game()

# Start the game with the player 
@app.route('/start_game')
def start_game():
    if game is not None:
        game.initGame()
        print(game.listToString())
    return "sucess"

# Player joins a game 
@app.route('/join/<name>', methods=['GET', 'POST'])
def player_join(name):
    game.addPlayer(name)
    return "Player %s joined game" % name      

# PLayer leaves a game
@app.route('/leave/<name>')
def player_leave(name):
    return 


# @app.route('/draw/<user_name>', methods=['POST'])
# def draw_hand(user_name):
#     #draw a hand for the user with user_name
#     global deck, players
#     player = None
#     for p in players:
#         if(p.name == user_name):
#             player = p
#     if(player == None):
#         return {"error": "Player not found"}
#     if(deck == None or deck == []):
#         return {"error": "Deck not initialized"}
#     Card.drawHand(deck, player)
#     for i in range(0, len(players)):
#         if(players[i].name == user_name):
#             players[i] = player
#     return {"success": Card.listToString(player.hand)}
    
    
# @app.route('/leave_game/<user_name>', methods=['POST'])
# def leave_game(user_name):
#     #remove player from list of players
#     global deck, players
#     for p in players:
#         if(p.name == user_name):
#             print('removing player')
#             players.remove(p)
#             #readd the players hand to the deck
#             break;
#     return {"success": "The player was removed"}

# @app.route('/join_game/<user_name>', methods=['GET', 'POST'])
# def join_game(user_name):
#     global players
#     if(players == None or players == []):
#         p = Player(user_name)
#         players.append(p)
#     return {"success": "The player was added"}


if __name__ == "__main__":
    app.run(debug=True)