class Game:
    def __init__(self, deck):
        self.deck = deck
        self.board = []
        self.burnCards = [] 
        self.players = []
        self.game_over = False 

    def addPlayer(self, player):
        self.players.append(player)

