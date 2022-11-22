import time
import random
from flask import Flask
from flask import request, session
from flask_session import Session
app = Flask(__name__)
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
class Player:
    def __init__(self, n):
        self.name = n
        self.hand = []
        self.chips = 0
        self.handSize = 2
    def addToHand(self, card):
        self.hand.append(card)
    def removeFromHand(self, card):
        for c in self.hand:
            if(c.suit == card.suit and c.value == card.value):
                self.hand.remove(c)
                return

class Card:
    def __init__(self, val, s):
        self.value = val
        self.suit = s
    def initializeCards():
        #returns a list of type Card[] with all possible options, not sorted
        cards = []
        for i in range(0, 4):
            s =""
            if(i == 0):
                s = "S"
            elif(i == 1):
                s = "D"
            elif(i == 2):
                s = "H"
            elif(i == 3):
                s = "C"
            #11 is jack
            #12 is queen
            #13 is king
            #14 is ace
            for j in range(2, 15):
                card = Card(j, s)
                cards.append(card)
        return cards
    def shuffleCards(cards):
        random.shuffle(cards)
        return cards
    def listToString(cards):
        #converts a list of card objects to a single string
        s = "["
        for i in range(0, len(cards)):
            if(i == len(cards) - 1):
                s += "{\"value\":\"" + str(cards[i].value) + "\", \"suit\":\"" + str(cards[i].suit) + "\"}"
            else:
                s += "{\"value\":\"" + str(cards[i].value) + "\", \"suit\":\"" + str(cards[i].suit) + "\"},"
        s += "]"
        return s
    def drawHand(cards, player):
        #remove player.handsize cards from cards, and add them to player's hand    
        for i in range(0, player.handSize):
            card = cards[0]
            player.addToHand(card)
            cards.remove(card)




deck = []
players = []

@app.route('/init_cards')
def init_cards():
    global deck
    if(deck == None or deck == []):
        deck = Card.initializeCards()
        deck = Card.shuffleCards(deck)
    else:
        return {"error": "Deck is already made"}
    return {"success": "Deck was created"}

@app.route('/draw/<user_name>', methods=['POST'])
def draw_hand(user_name):
    #draw a hand for the user with user_name
    global deck, players
    player = None
    for p in players:
        if(p.name == user_name):
            player = p
    if(player == None):
        return {"error": "Player not found"}
    if(deck == None or deck == []):
        return {"error": "Deck not initialized"}
    Card.drawHand(deck, player)
    for i in range(0, len(players)):
        if(players[i].name == user_name):
            players[i] = player
    return {"success": Card.listToString(player.hand)}
    
    
@app.route('/leave_game/<user_name>', methods=['POST'])
def leave_game(user_name):
    #remove player from list of players
    global deck, players
    for p in players:
        if(p.name == user_name):
            print('removing player')
            players.remove(p)
            #readd the players hand to the deck
            break;
    return {"success": "The player was removed"}

@app.route('/join_game/<user_name>', methods=['GET', 'POST'])
def join_game(user_name):
    global players
    if(players == None or players == []):
        p = Player(user_name)
        players.append(p)
    return {"success": "The player was added"}


