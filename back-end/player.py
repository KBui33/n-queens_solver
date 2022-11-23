class Player:
    def __init__(self, n, pid, m):
        self.name = n
        self.id = pid
        self.hand = []
        self.handSize = 2
        self.money = m
        self.curBet = 0
        self.move = None
    def dealHand(self, deck):
        for i in range(0, self.handSize):
            self.hand.append(deck.pop(0))
    def wager(self, val, game):
        if(val > self.money):
            #we cannot make this bet
            return False
        else:
            game.pot += val
            self.curBet += val
            self.money - val
            return True;
        