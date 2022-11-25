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
        self.burnedCards = [] 
        self.players = []
        self.discardCards = []
        self.blind = 10
        self.numPlayers =0
        self.game_over = False 
        self.totalPot = 0 
        self.round = 0
        # Need a var for small blind and big blind 

    def setPlayerReadyStatus(self, player, stats):
        """
        Readys the player and checks if everyone is ready. If all players ready start game, else emit to wait 

        Args:
            player - Name of the player or socket id (not sure which one is better so name for now)
            stats - True or False, the status the player wants to put on 
        """

        # Set the player to ready 
        for p in self.players:
            if p.name == player:
                p.ready = stats
                # Emit to player that updated 

                break 

        self.printPlayers()

        # Check if all players are ready 
        for p in self.players:
            if not p.ready and len(self.players) <= 4:
                print() # Emit to the players that they need to wait for other players to be ready 
                return False 
        
        # Start the game 
        self.initGame()
        return 


    def dealCard(self, player):
        # Takes out cards from the deck and puts them in players hands
        card = self.deck.pop(0)
        player.hand.append(card)
        return 

    def collectCards(self):
        # Takes all the cards out of all players hands and puts in back into the deck
        for p in self.players:
            toAdd = p.hand
            p.hand = []
            for c in toAdd:
                self.deck.append(c)
        self.shuffleDeck()

    def addPlayer(self, player):
        # Adds a player to the player set 
        self.players.append(player)
        self.numPlayers += 1

    def removePlayer(self, id):
        # Removes players from the player set
        for p in self.players:
            if(p.id == id):
                self.players.remove(p)
                self.numPlayers = self.numPlayers - 1
                return True
        return False

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
    
    # Inital stuff to do when starting the game 
    def initGame(self):
        
        # Create the deck and shuffle it 
        self.initializeCards()
        self.shuffleDeck()

        # Deal 2 cards to each player that not the dealer  
        for p in self.players:
            if (not p.dealer):
                self.dealCard(p)
                self.dealCard(p)

        self.gameLoop()


    def gameLoop(self):
        print("we are in the game loop")
        return 
        # if(len(self.players) < 2):
        #     return "need at least two players to be in the game"
        # # assert websocket connection for
        # while(not self.game_over):
        #     river = []
        #     #get big and small blinds
        #     players = self.players
        #     players[0].wager(self.blind)
        #     players[1].wager(self.blind/2)
        # if(len(self.players) < 2):
        #     return "need at least two players to be in the game"
        # # assert websocket connection for all players

        # #playing 1 round
        # self.dealCards()
        # river = []
        # players = self.players
        # if(players[0]): players[0].wager(self.blind)

        # for p in players:
        #     send_message(p.id, {"cards":self.listToString(p.hand), "money": str(p.money), "bet":str(p.curBet)})
        # # while(not self.game_over):
        # #     self.dealCards(); #deal each player a new hand
        # #     river = []
        # #     #get big and small blinds
        # #     players = self.players;
        # #     if(players[0]): players[0].wager(self.blind)

        # #     #send game info to the players
        # #     for p in players:
        # #         send_message(p.id, {"cards":self.listToString(p.hand), "money": str(p.money), "bet":str(p.curBet)})

    def printPlayers(self):
        print("Player currently in game")
        for p in self.players:
            print(vars(p))


