class Player:

    def __init__(self, name, bet=100):
        self.name = name
        # A new player has no cards
        self.hand = []
        self.value = 0
        self.aces = 0
        self.chips = 100
        self.bet = bet

    def add_card(self, card):
        self.hand.append(card)

    def __str__(self):
        return f'Player {self.name} has {len(self.hand)} cards.'

    def win_bet(self):
        self.chips += self.bet*2

    def lose_bet(self):
        self.chips -= self.bet

    def adjust_for_ace(self):
        self.value -= 10
        self.aces -= 1
