class Player:
    def __init__(self, n, pid):
        self.name = n
        self.id = pid
        self.hand = []
        self.handSize = 2
        self.money= 1000
        self.curBet = 0
    def __init__(self, n, pid, m):
        self.name = n
        self.id = pid
        self.hand = []
        self.handSize = 2
        self.money = m
        self.curBet = 0
        self.ready = False
        
    def dealHand(self, deck):
        for i in range(0, self.handSize):
            self.hand.append(deck.pop(0))
    def wager(self, val):
        if(val > self.money):
            #we cannot make this bet
            return False
        else:
            self.curBet += val
            self.money - val
            return True
        