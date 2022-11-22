import random
from card import * 

class Game:
    def __init__(self):
        self.deck = []
        self.board = []
        self.burnCards = [] 
        self.players = []
        self.game_over = False 

    def initGame(self):
        self.initializeCards()
        self.shuffleDeck()

    def addPlayer(self, player):
        self.players.append(player)

    def __str__(self):
        return self

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
                    print(card)
                    self.deck.append(card)


    def shuffleDeck(self):
        random.shuffle(self.deck)

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
    # def drawHand(cards, player):
    #     #remove player.handsize cards from cards, and add them to player's hand    
    #     for i in range(0, player.handSize):
    #         card = cards[0]
    #         player.addToHand(card)
    #         cards.remove(card)