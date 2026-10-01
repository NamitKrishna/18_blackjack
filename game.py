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

    def get_wager(self):
        """Prompt for and validate wager amount."""
        while True:
            try:
                wager_input = input(f"Enter wager (1-{self.chips}) or [q]uit: ").strip()
                if wager_input.lower() == 'q':
                    return None

                wager = int(wager_input)
                if wager < 1:
                    print("Wager must be at least 1 chip.")
                elif wager > self.chips:
                    print(f"You only have {self.chips} chips.")
                else:
                    return wager
            except ValueError:
                print("Invalid input. Please enter a number.")

    def round(self):
        print(f"\n--- New Round ---")
        print(f"Current chips: {self.chips}")

        # Get wager
        wager = self.get_wager()
        if wager is None:
            return False

        print(f"Wager: {wager} chips\n")

        deck = Deck()
        player = [deck.draw(), deck.draw()]
        dealer = [deck.draw(), deck.draw()]

        # Check for empty deck
        if None in player or None in dealer:
            print("Deck exhausted. Cannot continue round.")
            return True

        print(f"Player dealt: {player[0][0]}{player[0][1]} {player[1][0]}{player[1][1]}")
        print(f"Dealer shows: {dealer[0][0]}{dealer[0][1]}")
        self.show(player, dealer)

        # Check for natural blackjack
        player_blackjack = self.is_blackjack(player)
        dealer_blackjack = self.is_blackjack(dealer)

        if player_blackjack or dealer_blackjack:
            self.show(player, dealer, hide=False)
            if player_blackjack and dealer_blackjack:
                print("Both have Blackjack! Push.")
                print(f"Wager of {wager} chips returned.")
                return True
            elif player_blackjack:
                payout = int(wager * 1.5)  # Blackjack pays 3:2
                self.chips += payout
                print(f"Blackjack! Player wins {payout} chips.")
                return True
            else:
                self.chips -= wager
                print(f"Dealer has Blackjack. Dealer wins.")
                print(f"Lost {wager} chips.")
                return True

        # Player's turn
        round_ended = False
        while hand_value(player) < 21:
            key = input("[h]it [s]tand [q]uit: ").strip().lower()
            if key == "q":
                print("Forfeiting round...")
                self.chips -= wager
                print(f"Lost {wager} chips.")
                return False
            elif key == "s":
                print("Player stands.")
                break
            elif key == "h":
                card = deck.draw()
                if card is None:
                    print("Deck exhausted.")
                    break
                player.append(card)
                print(f"Player drew: {card[0]}{card[1]}")
                self.show(player, dealer)
                if hand_value(player) > 21:
                    print("Player busts!")
                    self.chips -= wager
                    print(f"Lost {wager} chips.")
                    round_ended = True
                    break
            else:
                print("Invalid command. Please use [h]it, [s]tand, or [q]uit.")

        if round_ended:
            return True

        # Dealer's turn (only if player didn't bust)
        print("\nDealer reveals hidden card...")
        self.show(player, dealer, hide=False)
        print(f"Dealer has: {hand_value(dealer)}")

        while hand_value(dealer) < 17:
            card = deck.draw()
            if card is None:
                print("Deck exhausted.")
                break
            dealer.append(card)
            print(f"Dealer draws: {card[0]}{card[1]}")
            print(f"Dealer has: {hand_value(dealer)}")

        # Determine winner
        pv, dv = hand_value(player), hand_value(dealer)
        print()
        if dv > 21:
            self.chips += wager
            print(f"Dealer busts! Player wins {wager} chips.")
        elif pv > dv:
            self.chips += wager
            print(f"Player wins {wager} chips!")
        elif pv < dv:
            self.chips -= wager
            print(f"Dealer wins. Lost {wager} chips.")
        else:
            print(f"Push. Wager of {wager} chips returned.")

        return True

    def run(self):
        print("=" * 40)
        print("BLACKJACK")
        print("=" * 40)
        print(f"Starting chips: {self.chips}")
        print()

        while self.chips > 0:
            if not self.round():
                break

            print(f"\nChip balance: {self.chips}")

            if self.chips <= 0:
                print("\nYou're out of chips! Game over.")
                break

            play_again = input("\nPlay again? [y/n]: ").strip().lower()
            if play_again != 'y':
                break

        print(f"\nThanks for playing! Final chips: {self.chips}")
        print("=" * 40)
