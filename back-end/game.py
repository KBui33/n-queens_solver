import random
from card import * 
from player import *

class Game:
    def __init__(self):
        self.deck = []
        self.board = []
        self.burnedCards = [] 
        self.players = []
        self.discardCards = []
        self.game_over = False 
        self.totalPot = 0 
        self.round = 0


        # Need a var for small blind and big blind 

    # Inital stuff to do when starting the game 
    def initGame(self):
        
        # Create the deck and shuffle it 
        self.initializeCards()
        self.shuffleDeck()

        # Deal 2 cards to each player 
        for i in len(self.players):
            print() # Temp here, deal card to player

    # Add player to the game 
    def addPlayer(self, name):
        self.players.append(Player(name))

    def __str__(self):
        return self
    def gameLoop(self):
        if(len(self.players) < 2):
            return "need at least two players to be in the game"
        #assert websocket connection for
        while(not self.game_over):
            river = []
            #get big and small blinds
            players = self.players
            players[0].wager(self.blind)
            players[1].wager(self.blind/2)

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

    # Deal a card to the player, the top of the deck is at index 0 
    def dealCard(self):
        return self.deck[0]

    def listToString(self):
        #converts a list of card objects to a single string
        s = "["
        for i in range(0, len(self.deck)):
            if(i == len(self.deck) - 1):
                s += "{\"value\":\"" + str(self.deck[i].value) + "\", \"suit\":\"" + str(self.deck[i].suit) + "\"}"
            else:
                s += "{\"value\":\"" + str(self.deck[i].value) + "\", \"suit\":\"" + str(self.deck[i].suit) + "\"},"
        s += "]"
        return s

    def printPlayers(self):
        for i in self.players:
            print(i.name)
