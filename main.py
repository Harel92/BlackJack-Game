from Deck import Deck
from Player import Player


# Take bet amount from player
def take_bet():
    is_bet = True
    while is_bet:
        try:
            cash = int(input(f'{player.name}, How much to bet? (Current Chips: {player.chips}) '))
            if cash <= player.chips:
                player.bet = cash
                is_bet = False
                print("Bet approved")
            else:
                print("Not enough chips, choose another value")
        except:
            print("Wrong Input")


# Hit another card to player or dealer
def hit(deck, the_player):
    card = deck.deal()
    the_player.value += card.value
    if card.rank == 'Ace':
        the_player.aces += 1
    the_player.hand.append(card)


# Show all cards except 1 hidden of Dealer
def show_some(the_player, dealer):
    print()
    print(f'-------{the_player.name} Cards-------')
    for card in the_player.hand:
        print(f'<{card}>')
    print(f'-------Total: {the_player.value}---------')
    print()
    print(f'-------{dealer.name} Cards-------')
    print(f'<{dealer.hand[0]}>')
    print("<Hidden Card>")
    print(f'-------Total: {dealer.hand[0].value}----------')
    print()


# Show all player and dealer cards
def show_all(the_player, dealer):
    print()
    print(f'-------{the_player.name} Cards-------')
    for card in the_player.hand:
        print(f'<{card}>')
    print(f'-------Total: {the_player.value}---------')
    print()
    print(f'-------{dealer.name} Cards-------')
    for card in dealer.hand:
        print(f'<{card}>')
    print(f'-------Total: {dealer.value}------------')
    print()


# Check if the player wants to keep playing
def another_round():
    while True:
        keep = input('Play Another Round? (y/n) ')
        if keep == 'y':
            return True
        elif keep == 'n':
            return False
        else:
            print("Wrong Input")


def player_busts():
    print('You exceeds 21, You Lose The Round')
    player.lose_bet()
    reset()


def player_wins():
    print("You Won The Dealer")
    player.win_bet()
    reset()


def dealer_busts():
    print('Dealer exceeds 21, You Won The Round')
    player.win_bet()
    reset()


def dealer_wins():
    print("You Lose The Round")
    player.lose_bet()
    reset()


def push():
    print("Its A Tie!")
    reset()


def reset():
    player.aces = 0
    player.value = 0
    player.hand = []
    AI.aces = 0
    AI.value = 0
    AI.hand = []


print()
print("Welcome to BlackJack! Get as close to 21 as you can without going over!")
print("Dealer hits until she reaches 17. Aces count as 1 or 11.")
name = input("Please Enter Your Name: ")
player = Player(name)
AI = Player("Dealer")

game_on = True

# Start Playing
while game_on:
    # New Game Round
    new_deck = Deck()
    new_deck.shuffle()

    # Player out of chips
    if player.chips <= 0:
        print("You Are Out of Chips, Game Over")
        break

    # Take bet and serve 2 cards to each player
    take_bet()
    hit(new_deck, player)
    hit(new_deck, AI)
    hit(new_deck, player)
    hit(new_deck, AI)

    # Adjust if started with 2 aces
    if player.aces == 2:
        player.adjust_for_ace()

    # Show current game
    show_some(player, AI)

    same_round = True
    # Playing same round
    while same_round:

        # Player Hits or stand
        print("Your Turn")
        while player.value < 21:
            play = input("hit or stand? ")

            if play == 'hit':
                hit(new_deck, player)
                if player.value > 21 and player.aces > 0:
                    player.adjust_for_ace()

                elif player.value > 21 and player.aces == 0:
                    show_some(player, AI)
                    player_busts()
                    same_round = False
                    game_on = another_round()
                    break

                show_some(player, AI)

            elif play == 'stand':
                break

        if not same_round:
            break

        # Dealer Reveal Card
        print("Dealer's Turn, Reveal Card")
        show_all(player, AI)
        if AI.aces == 2:
            AI.adjust_for_ace()

        # Dealer Hit
        while same_round and AI.value < 17:
            print("Dealer Draw")
            hit(new_deck, AI)
            if AI.value > 21 and AI.aces > 0:
                AI.adjust_for_ace()

            elif AI.value > 21 and AI.aces == 0:
                show_all(player, AI)
                dealer_busts()
                same_round = False
                game_on = another_round()
                break

            show_all(player, AI)

        # No one bust, Check who won
        if same_round:
            if player.value > AI.value:
                player_wins()
            elif player.value < AI.value:
                dealer_wins()
            else:
                push()

            same_round = False
            game_on = another_round()

if not game_on:
    print(f"Thanks For Playing Earnings is: {player.chips} Chips")
