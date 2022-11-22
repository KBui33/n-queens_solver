import time
import random
from flask import Flask
app = Flask(__name__)

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
@app.route('/time')
def get_current_time():
    return {'time': time.time()}

@app.route('/init_cards')
def init_cards():
    cards = Card.initializeCards()
    cards = Card.shuffleCards(cards)

    return {'cards': Card.listToString(cards)}


