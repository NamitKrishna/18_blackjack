import random

RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
SUITS = ["C", "D", "H", "S"]


class Deck:
    def __init__(self):
        self.cards = [(rank, suit) for suit in SUITS for rank in RANKS]
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None


def hand_value(hand):
    """Calculate the value of a blackjack hand, treating Aces optimally."""
    value = 0
    aces = 0

    for rank, _ in hand:
        if rank == "A":
            aces += 1
            value += 11  # Initially count Ace as 11
        elif rank in {"J", "Q", "K"}:
            value += 10
        else:
            value += int(rank)

    # Convert Aces from 11 to 1 as needed to avoid busting
    while value > 21 and aces > 0:
        value -= 10  # Convert one Ace from 11 to 1
        aces -= 1

    return value
