let game = null;
let balance = 1000;


function createCard(card) {

    const div = document.createElement("div");

    div.classList.add("card");

    if (card.hidden) {
        div.classList.add("hidden-card");
        div.innerHTML = "🂠";
        return div;
    }

    let symbol = "";

    if (card.suit === "Hearts") {
        symbol = "♥";
    } else if (card.suit === "Diamonds") {
        symbol = "♦";
    } else if (card.suit === "Clubs") {
        symbol = "♣";
    } else {
        symbol = "♠";
    }

    if (card.suit === "Hearts" || card.suit === "Diamonds") {
        div.classList.add("red");
    }

    div.innerHTML = `
        <div>${card.rank}</div>
        <div>${symbol}</div>
    `;

    return div;
}


function displayCards(elementId, cards) {

    const container = document.getElementById(elementId);

    container.innerHTML = "";

    cards.forEach(card => {
        container.appendChild(createCard(card));
    });
}


function startGame() {

    const bet = Number(document.getElementById("bet").value);

    if (bet <= 0 || bet > balance) {
        alert("Enter a valid bet.");
        return;
    }

    fetch("/start", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            bet: bet
        })

    })
    .then(response => response.json())
    .then(data => {

        game = data;

        document.getElementById("setup").classList.add("hidden");
        document.getElementById("game").classList.remove("hidden");

        updateScreen(data);

        if (data.result === "blackjack") {
            balance += bet;
            showResult("🎉 BLACKJACK! You win!");
        }

    });
}


function hit() {

    fetch("/hit", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            game: game
        })

    })
    .then(response => response.json())
    .then(data => {

        game = data;

        updateScreen(data);

        if (data.result === "bust") {
            balance -= data.bet;
            showResult("💥 Bust! You lose.");
        }

    });
}


function stand() {

    fetch("/stand", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({
            game: game
        })

    })
    .then(response => response.json())
    .then(data => {

        game = data;

        updateScreen(data);

        if (data.result === "win" || data.result === "dealer_bust") {

            balance += data.bet;
            showResult("🎉 You win!");

        } else if (data.result === "lose") {

            balance -= data.bet;
            showResult("❌ Dealer wins.");

        } else if (data.result === "tie") {

            showResult("🤝 It's a tie!");

        }

    });
}


function updateScreen(data) {

    displayCards("player-cards", data.player_cards);

    displayCards("dealer-cards", data.dealer_cards);

    document.getElementById("player-score").textContent =
        data.player_score;

    document.getElementById("dealer-score").textContent =
        data.dealer_score;

    document.getElementById("balance").textContent =
        balance;
}


function showResult(message) {

    document.getElementById("message").textContent = message;

    document.getElementById("hit-btn").disabled = true;
    document.getElementById("stand-btn").disabled = true;

    document.getElementById("new-game-btn").classList.remove("hidden");

    document.getElementById("balance").textContent = balance;
}


function showSetup() {

    document.getElementById("game").classList.add("hidden");

    document.getElementById("setup").classList.remove("hidden");

    document.getElementById("hit-btn").disabled = false;
    document.getElementById("stand-btn").disabled = false;

    document.getElementById("message").textContent = "Your turn";

    document.getElementById("bet").value = "";

    document.getElementById("balance").textContent = balance;
}
