import random
from card import *
from player import *
from flask_socketio import emit, join_room, leave_room, send
from itertools import combinations
try:
    from __main__ import socketio
except ImportError:
    from flask_socketio import socketio


def send_message(tag, client_id, data):
    emit(tag, data, room=client_id)
    print('sending message "{}" to client "{}".'.format(data, client_id))


class Game:
    def __init__(self):
        self.deck = []              # List of 52 cards
        # List of cards that hold the game cards (Flop, Turn, River rounds)
        self.board = []
        self.burnedCards = []       # List of burned cards
        # List of players in the game (including the AI)
        self.players = []
        self.activePlayers = []     # List of players that have not folded
        # The minimum amount of money needed for betting for the blinds
        self.blindAmount = 10
        # Amount of players in the game (not including the AI)
        self.numPlayers = 0
        self.gameOver = False       # Game status
        self.totalPot = 0           # The total amount of money through each iteration of rounds
        self.round = 0              # Current Round
        self.smallBlind = 0         # The index of the current person with the small blind
        self.bigBlind = 0           # The index of the current person with the big blind
        self.currentPlayerTurn = 0  # The index of the current turn of the person

    def dealCard(self, player):
        # Takes out cards from the deck and puts them in players hands
        card = self.deck.pop(0)
        player.hand.append(card)

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
            if (p.id == id):
                n = p.name
                self.players.remove(p)
                self.numPlayers = self.numPlayers - 1
                return n
        return False

    def initializeCards(self):
        # returns a list of type Card[] with all possible options, not sorted
        for i in range(0, 4):
            s = ""
            if (i == 0):
                s = "S"  # Spades
            elif (i == 1):
                s = "D"  # Diamonds
            elif (i == 2):
                s = "H"  # Hearts
            elif (i == 3):
                s = "C"  # Clovers
            #11 is jack
            #12 is queen
            #13 is king
            #14 is ace
            for j in range(2, 15):
                card = Card(j, s)
                self.deck.append(card)

    def shuffleDeck(self):
        # Shuffles the deck randomly
        random.shuffle(self.deck)

    def getScoreboard(self):
        # returns an array of objects of the form {name: '', curBet:0, money:0}
        s = "["
        for i in range(0, len(self.players)):
            if (i == len(self.players) - 1):
                # dont include the comma
                s += "{\"name\":\"" + str(self.players[i].name) + "\", \"curBet\":\"" + str(self.players[i].curBet) + "\", \"money\":\"" + str(
                    self.players[i].money) + "\", \"move\":\"" + str(self.players[i].move) + "\"}"
            else:
                s += "{\"name\":\"" + str(self.players[i].name) + "\", \"curBet\":\"" + str(self.players[i].curBet) + "\", \"money\":\"" + str(
                    self.players[i].money) + "\", \"move\":\"" + str(self.players[i].move) + "\"};"
        s += "]"
        return s

    def listToString(self, cards):
        # converts a list of card objects to a single string
        s = "["
        for i in range(0, len(cards)):
            if (i == len(cards) - 1):
                s += "{\"value\":\"" + str(cards[i].value) + \
                    "\", \"suit\":\"" + str(cards[i].suit) + "\"}"
            else:
                s += "{\"value\":\"" + str(cards[i].value) + \
                    "\", \"suit\":\"" + str(cards[i].suit) + "\"},"
        s += "]"
        return s

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
                break

        # Check if all players are ready
        for p in self.players:
            if not p.ready or len(self.players) < 3:
                print("Game not ready yet")
                # Emit to the players that they need to wait for other players to be ready
                emit("game_start_status", {
                     "msg": "Wait from more ppl to join", "start": False})
                return False

        # Start the game
        self.initGame()
        return

    # Inital stuff to do when starting the game.
    def initGame(self):
        # Create the deck and shuffle it
        print("Starting game")
        emit("game_start_status", {
             "msg": "Starting Game", "start": True}, broadcast=True)

        self.initializeCards()
        self.shuffleDeck()

        # Set the small blind and Big blind to players
        # The dealer is not in the players array, but rather the game instance it self.
        # For the start the small blind is 0, big blind 1. Move up after
        self.smallBlind = 0
        self.bigBlind = self.smallBlind + 1

        # Notify the players with blind to place a bet
        # Prob need to group the blinds ppl in a room, then send out the thing with their repective amount
        # room = 'blindRoom'
        smallId = self.players[self.smallBlind].id
        bigId = self.players[self.bigBlind].id

        print(f"Small blind ${smallId}, Big blind ${bigId}")

        emit("blind", f"You are the small blind.", to=smallId)
        emit("blind", f"You are the big blind", to=bigId)

        # Start the game

        # Deal 2 cards to each player thats not the dealer
        print("setting the hand")
        for p in self.players:
            self.dealCard(p)
            self.dealCard(p)

    def nextRound(self):
        # Go through each player and see what they do

        # The person next to the big blind starts. Players either call, raise or fold

        # Once we hit back to the starting person pot is collected

        # Burn one card
        # Put 3 cards on the board (The flop)

        # The left active player gets to start first. Can put a bet, check, or fold.
        # If players place bet then everyone needs to put that much until it goes back to that player. Samething if raise happens

        # Burn one card
        # Add the 4th card (The turn)
        # Do another betting round (like the one above)

        # Burn one card
        # 5th card is placed (the River)
        # Do another betting round (like the one above)
        # ==============================================================================

        self.updateStatus()
        # Check if all players did their turn
        if (self.currentPlayerTurn + 1 == len(self.activePlayers)):

            if (len(self.board) == 5):
                # At the showdown, need to check ppl hand and end game
                self.endGame()
                return

            # Dealer burns a card
            self.burnedCards.append(self.deck.pop(0))

            # Starting round
            if (self.round == 0):
                # The flop cards
                for _ in range(3):
                    self.board.append(self.deck.pop(0))
            else:
                # The turn and river
                self.board.append(self.deck.pop(0))

            # reset and go back to the person who is left of the dealer
            self.currentPlayerTurn = 0

        # Go to next player
        self.currentPlayerTurn += 1

        # Get the player
        player = self.activePlayers[self.currentPlayerTurn]
        # Emitt to the player that it is their turn
        emit('player_turn', "Its your turn", to=player.id)
        return

    def endGame(self):
        # Showdown, everyone shows their cards.
        # Find the best card combo wins the pot

        # Restart and move BB and SB

        # Start of the round, cards are given to players
        return

    def findHighestHand(self, player):
        """
        Given the player, find the best combination the player can have 
        Return cards with the highest ranking + highest total
        """
        # Rankings are based off the index number, the higher the number the better the hand
        handRanking = ['High Card', 'Pair', 'Three of a kind', 'Straight',
                       'Flush', 'Full House', 'Four of a Kind', 'Straight Flush', 'Royal Flush']

        # Create combinations of length 5
        combos = combinations(player.hand + self.board, 5)

        handCombos = []  # Used to determine ties. If we have hands with the same rank, need to look at the total to see the better one
        # Go through each combo and determine which one is the best hand combo.
        for idx, c in enumerate(combos):
            handRank = self.determineHand(c)
            handTotal = sum([card.value for card in c])

            handCombos.append((handRanking.index(handRank), handTotal, idx))

        return combos[max(handCombos)[2]]

    def determineHand(self, cards):
        """ 
        Determine the type of hand of 5 cards 
        i.e. This hand is a pair
        Return a string of hand type 
        """
        suits = [card.suit for card in cards]  # Get all the suits from hand
        ranks = [card.value for card in cards]  # Get all the value from hand

        # There is a straight, determine if it can be better
        if self.isConsecutive(ranks):
            return (
                'Straight' if not len(set(suits)) != 1 else
                'Straight flush' if max(ranks) < 14 else
                'Royal flush'
            )

        # There are no duplicates which means that all the ranks are the same
        if len(set(suits)) == 1:
            return "Flush"

        # Count the amount repetitions in the set for each element
        return ({
            4 + 4 + 4 + 4 + 1: 'Four of a kind',
            3 + 3 + 3 + 2 + 2: 'Full house',
            3 + 3 + 3 + 1 + 1: 'Three of a kind',
            2 + 2 + 2 + 2 + 1: 'Two pair',
            2 + 2 + 1 + 1 + 1: 'One pair',
            1 + 1 + 1 + 1 + 1: 'High card',
        }[sum(ranks.count(r) for r in ranks)], sum(ranks))

    def isConsecutive(self, lst):
        """
        Return true if the list contains a consecutive order
        """
        return len(set(lst)) == len(lst) and max(lst) - min(lst) == len(lst) - 1

    def addToPot(self):
        # Get all of the players current bet and add to pot
        for p in self.activePlayers:
            self.totalPot += p.curBet

        return

    def updateStatus(self):
        for p in self.players:
            if p.fold == False:
                self.activePlayers.append(p)

    def printPlayers(self):
        print("Player currently in game")
        for p in self.players:
            print(vars(p))
