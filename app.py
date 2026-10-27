import random


def create_deck():
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10",
             "J", "Q", "K", "A"]

    deck = []

    for suit in suits:
        for rank in ranks:
            deck.append((rank, suit))

    random.shuffle(deck)
    return deck


def calculate_score(hand):
    score = 0
    aces = 0

    for rank, suit in hand:

        if rank in ["J", "Q", "K"]:
            score += 10

        elif rank == "A":
            score += 11
            aces += 1

        else:
            score += int(rank)

    while score > 21 and aces > 0:
        score -= 10
        aces -= 1

    return score


def show_hand(name, hand):
    print(f"\n{name}'s hand:")

    for rank, suit in hand:
        print(f"{rank} of {suit}")

    print(f"Score: {calculate_score(hand)}")


def play_game():

    print("================================")
    print("       🃏 BLACKJACK 🃏")
    print("================================")
    print("Get as close to 21 as possible.")
    print("Starting balance: 1000 virtual tokens")
    print("================================\n")

    balance = 1000

    while balance > 0:

        print(f"Current Balance: {balance} tokens")

        # Get bet
        try:
            bet = int(input(f"Enter your bet (1-{balance}): "))
        except ValueError:
            print("❌ Enter a valid number.\n")
            continue

        if bet <= 0 or bet > balance:
            print("❌ Invalid bet amount.\n")
            continue

        # Create and shuffle deck
        deck = create_deck()

        # Deal cards
        player_hand = [deck.pop(), deck.pop()]
        dealer_hand = [deck.pop(), deck.pop()]

        show_hand("Your", player_hand)

        print("\nDealer's hand:")
        print(f"{dealer_hand[0][0]} of {dealer_hand[0][1]}")
        print("Hidden card")

        # Check for blackjack
        player_score = calculate_score(player_hand)

        if player_score == 21:

            print("\n🎉 BLACKJACK!")

            balance += bet
            print(f"You won {bet} tokens.")

        else:

            # Player's turn
            while True:

                choice = input("\nChoose Hit or Stand (h/s): ").lower().strip()

                if choice == "h":

                    player_hand.append(deck.pop())
                    show_hand("Your", player_hand)

                    player_score = calculate_score(player_hand)

                    if player_score > 21:
                        print("\n💥 Bust! You went over 21.")
                        balance -= bet
                        break

                elif choice == "s":
                    break

                else:
                    print("❌ Enter h for Hit or s for Stand.")

            # Continue only if player did not bust
            if player_score <= 21:

                # Dealer's turn
                while calculate_score(dealer_hand) < 17:
                    dealer_hand.append(deck.pop())

                show_hand("Dealer", dealer_hand)

                dealer_score = calculate_score(dealer_hand)

                # Decide winner
                if dealer_score > 21:
                    print("\n🎉 Dealer busted! You win!")
                    balance += bet

                elif player_score > dealer_score:
                    print("\n🎉 You win!")
                    balance += bet

                elif player_score < dealer_score:
                    print("\n❌ Dealer wins!")
                    balance -= bet

                else:
                    print("\n🤝 It's a tie!")
                    print("Your bet is returned.")

        print(f"New Balance: {balance} tokens\n")

        if balance == 0:
            print("💥 You have no tokens left.")
            print("Game Over!")
            break

        play_again = input("Play again? (y/n): ").lower().strip()

        if play_again != "y":
            print("\n================================")
            print(f"Final Balance: {balance} tokens")
            print("Thanks for playing!")
            print("================================")
            break


play_game()