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