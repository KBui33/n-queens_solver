import random
from card import * 
from player import *
from flask_socketio import emit
try:
    from __main__ import socketio
except ImportError:
    from flask_socketio import socketio


def send_message(client_id, data):
    emit('output', data, room=client_id)
    print('sending message "{}" to client "{}".'.format(data, client_id))
class Game:
    def __init__(self):
        self.deck = []
        self.board = []
        self.burnCards = [] 
        self.players = []
        self.blind = 10
        self.numPlayers =0
        self.pot = 0;
        self.game_over = False 

    def initGame(self):
        self.initializeCards()
        self.shuffleDeck()

    def dealCards(self):
        #takes out cards from the deck and puts them in players hands
        d = self.deck
        for p in self.players:
            p.dealHand(self.deck)

    def collectCards(self):
        #takes all the cards out of all players hands and puts in back into the deck
        for p in self.players:
            toAdd = p.hand
            p.hand = []
            for c in toAdd:
                self.deck.append(c)
        self.shuffleDeck();

    def addPlayer(self, player):
        self.players.append(player)
        self.numPlayers += 1

    def removePlayer(self, id):
        for p in self.players:
            if(p.id == id):
                self.players.remove(p)
                self.numPlayers = self.numPlayers - 1
                return True
        return False
    def __str__(self):
        return self

    def end_round(self, winner):
        #TODO: implement summing all bets of players, then add it to the winning player id
        #ends the round, adding all bets to the winning player
        return
    def start_game(self):
        #function to start an initial game and give hands to the users

        #playing 1 round
        self.dealCards();
        players = self.players;
        if(len(players) > 1): 
            players[0].wager(self.blind, self)
            players[1].wager(self.blind/2, self)
        else:
            #emit back to user that game needs more players to start

            return False

        for p in players:
            send_message(p.id, {"cards":self.listToString(p.hand), "money": str(p.money), "bet":str(p.curBet)})
        return True

    def initializeCards(self):
            #returns a list of type Card[] with all possible options, not sorted
            for i in range(0, 4):
                s =""
                if(i == 0):
                    s = "S" # Spades 
                elif(i == 1):
                    s = "D" # Diamonds 
                elif(i == 2):
                    s = "H" # Hearts 
                elif(i == 3):
                    s = "C" # Clovers 
                #11 is jack
                #12 is queen
                #13 is king
                #14 is ace
                for j in range(2, 15):
                    card = Card(j, s)
                    self.deck.append(card)


    def shuffleDeck(self):
        random.shuffle(self.deck)

    def listToString(self, cards):
        #converts a list of card objects to a single string
        s = "["
        for i in range(0, len(cards)):
            if(i == len(cards) - 1):
                s += "{\"value\":\"" + str(cards[i].value) + "\", \"suit\":\"" + str(cards[i].suit) + "\"}"
            else:
                s += "{\"value\":\"" + str(cards[i].value) + "\", \"suit\":\"" + str(cards[i].suit) + "\"},"
        s += "]"
        return s
