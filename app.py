from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)


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


def card_data(card):
    return {
        "rank": card[0],
        "suit": card[1]
    }


def new_game(bet):
    deck = create_deck()

    player_hand = [deck.pop(), deck.pop()]
    dealer_hand = [deck.pop(), deck.pop()]

    return {
        "deck": deck,
        "player_hand": player_hand,
        "dealer_hand": dealer_hand,
        "bet": bet,
        "game_over": False
    }


def get_game_data(game, hide_dealer=True):
    player_hand = game["player_hand"]
    dealer_hand = game["dealer_hand"]

    data = {
        "player_cards": [card_data(card) for card in player_hand],
        "player_score": calculate_score(player_hand),
        "bet": game["bet"],
        "game_over": game["game_over"]
    }

    if hide_dealer:
        data["dealer_cards"] = [
            card_data(dealer_hand[0]),
            {"hidden": True}
        ]
        data["dealer_score"] = "?"
    else:
        data["dealer_cards"] = [
            card_data(card) for card in dealer_hand
        ]
        data["dealer_score"] = calculate_score(dealer_hand)

    return data


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/start", methods=["POST"])
def start():
    data = request.json
    bet = int(data["bet"])

    game = new_game(bet)

    player_score = calculate_score(game["player_hand"])

    if player_score == 21:
        game["game_over"] = True
        result = "blackjack"
        return jsonify({
            **get_game_data(game, False),
            "result": result
        })

    return jsonify(get_game_data(game))


@app.route("/hit", methods=["POST"])
def hit():
    data = request.json
    game = data["game"]

    game["deck"] = [tuple(card) for card in game["deck"]]
    game["player_hand"] = [tuple(card) for card in game["player_hand"]]
    game["dealer_hand"] = [tuple(card) for card in game["dealer_hand"]]

    game["player_hand"].append(game["deck"].pop())

    score = calculate_score(game["player_hand"])

    if score > 21:
        game["game_over"] = True

        return jsonify({
            **get_game_data(game, False),
            "result": "bust"
        })

    return jsonify(get_game_data(game))


@app.route("/stand", methods=["POST"])
def stand():
    data = request.json
    game = data["game"]

    game["deck"] = [tuple(card) for card in game["deck"]]
    game["player_hand"] = [tuple(card) for card in game["player_hand"]]
    game["dealer_hand"] = [tuple(card) for card in game["dealer_hand"]]

    while calculate_score(game["dealer_hand"]) < 17:
        game["dealer_hand"].append(game["deck"].pop())

    player_score = calculate_score(game["player_hand"])
    dealer_score = calculate_score(game["dealer_hand"])

    game["game_over"] = True

    if dealer_score > 21:
        result = "dealer_bust"

    elif player_score > dealer_score:
        result = "win"

    elif player_score < dealer_score:
        result = "lose"

    else:
        result = "tie"

    return jsonify({
        **get_game_data(game, False),
        "result": result
    })


if __name__ == "__main__":
    app.run(debug=True)
