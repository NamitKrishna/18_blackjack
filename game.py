from cards import Deck, hand_value


class Blackjack:
    def __init__(self):
        self.chips = 100

    def show(self, player, dealer, hide=True):
        if hide:
            # Show dealer's first card, hide second
            shown_dealer = [f"{dealer[0][0]}{dealer[0][1]}", "??"] if len(dealer) >= 2 else ["??"]
        else:
            shown_dealer = [f"{r}{s}" for r, s in dealer]
        print("Dealer:", " ".join(shown_dealer))
        print("Player:", " ".join(f"{r}{s}" for r, s in player),
              "=", hand_value(player))

    def is_blackjack(self, hand):
        """Check if hand is a natural blackjack (21 with exactly 2 cards)."""
        return len(hand) == 2 and hand_value(hand) == 21

    def round(self):
        deck = Deck()
        player = [deck.draw(), deck.draw()]
        dealer = [deck.draw(), deck.draw()]

        # Check for empty deck
        if None in player or None in dealer:
            print("Deck exhausted. Cannot continue round.")
            return True

        self.show(player, dealer)

        # Check for natural blackjack
        player_blackjack = self.is_blackjack(player)
        dealer_blackjack = self.is_blackjack(dealer)

        if player_blackjack or dealer_blackjack:
            self.show(player, dealer, hide=False)
            if player_blackjack and dealer_blackjack:
                print("Both have Blackjack! Push.")
                return True
            elif player_blackjack:
                self.chips += 15  # Blackjack pays 3:2 on a 10 chip bet
                print("Blackjack! Player wins.")
                return True
            else:
                self.chips -= 10
                print("Dealer has Blackjack. Dealer wins.")
                return True

        # Player's turn
        round_ended = False
        while hand_value(player) < 21:
            key = input("[h]it [s]tand [q]uit: ").strip().lower()
            if key == "q":
                return False
            if key == "s":
                break
            if key == "h":
                card = deck.draw()
                if card is None:
                    print("Deck exhausted.")
                    break
                player.append(card)
                self.show(player, dealer)
                if hand_value(player) > 21:
                    print("Player busts.")
                    self.chips -= 10
                    round_ended = True
                    break
            else:
                print("Invalid command. Use [h]it, [s]tand, or [q]uit.")

        if round_ended:
            return True

        # Dealer's turn (only if player didn't bust)
        print("\nDealer's turn...")
        self.show(player, dealer, hide=False)

        while hand_value(dealer) < 17:
            card = deck.draw()
            if card is None:
                print("Deck exhausted.")
                break
            dealer.append(card)
            print(f"Dealer draws: {card[0]}{card[1]}")
            self.show(player, dealer, hide=False)

        # Determine winner
        pv, dv = hand_value(player), hand_value(dealer)
        if dv > 21:
            self.chips += 10
            print("Dealer busts. Player wins.")
        elif pv > dv:
            self.chips += 10
            print("Player wins.")
        elif pv < dv:
            self.chips -= 10
            print("Dealer wins.")
        else:
            print("Push.")

        return True

    def run(self):
        print("Blackjack — starting chips:", self.chips)
        while self.chips > 0:
            if not self.round():
                return
            print(f"Current chips: {self.chips}")
            if input("Play again? [y/n]: ").strip().lower() != "y":
                return
