import random
import tkinter as tk
from tkinter import messagebox

# ---------------------------
# Game Logic
# ---------------------------
suits_symbols = {"hearts": "♥", "diamonds": "♦", "clubs": "♣", "spades": "♠"}
ranks = {
    "A": 11,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10,
}

deck = [(rank, suit) for suit in suits_symbols for rank in ranks]


def deal_card():
    return random.choice(deck)


def calculate_score(hand):
    values = [ranks[card[0]] for card in hand]
    score = sum(values)
    while score > 21 and 11 in values:
        values[values.index(11)] = 1
        score = sum(values)
    return score


# ---------------------------
# GUI Blackjack
# ---------------------------
class BlackjackGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Blackjack Casino")
        self.root.config(bg="darkgreen")

        # Dealer Area
        self.dealer_label = tk.Label(
            root,
            text="Dealer's Hand:",
            font=("Arial", 14, "bold"),
            bg="darkgreen",
            fg="white",
        )
        self.dealer_label.pack(pady=5)
        self.dealer_hand_label = tk.Label(
            root, text="", font=("Arial", 16), bg="darkgreen", fg="white"
        )
        self.dealer_hand_label.pack(pady=10)

        # Player Area
        self.player_label = tk.Label(
            root,
            text="Your Hand:",
            font=("Arial", 14, "bold"),
            bg="darkgreen",
            fg="white",
        )
        self.player_label.pack(pady=5)
        self.player_hand_label = tk.Label(
            root, text="", font=("Arial", 16), bg="darkgreen", fg="white"
        )
        self.player_hand_label.pack(pady=10)

        # Status
        self.status_label = tk.Label(
            root, text="", font=("Arial", 16, "bold"), bg="darkgreen", fg="yellow"
        )
        self.status_label.pack(pady=10)

        # Buttons
        button_frame = tk.Frame(root, bg="darkgreen")
        button_frame.pack(pady=20)

        self.hit_button = tk.Button(
            button_frame, text="Hit", font=("Arial", 14), width=10, command=self.hit
        )
        self.hit_button.grid(row=0, column=0, padx=10)

        self.stand_button = tk.Button(
            button_frame, text="Stand", font=("Arial", 14), width=10, command=self.stand
        )
        self.stand_button.grid(row=0, column=1, padx=10)

        self.reset_button = tk.Button(
            button_frame,
            text="Reset",
            font=("Arial", 14),
            width=10,
            command=self.reset_game,
        )
        self.reset_button.grid(row=0, column=2, padx=10)

        self.reset_game()

    def format_hand(self, hand, hide_first=False):
        display = []
        for i, (rank, suit) in enumerate(hand):
            if i == 0 and hide_first:
                display.append("??")
            else:
                display.append(f"{rank}{suits_symbols[suit]}")
        return "  ".join(display)

    def deal_initial_cards(self):
        self.player_cards = [deal_card(), deal_card()]
        self.dealer_cards = [deal_card(), deal_card()]

    def update_display(self, hide_dealer=True):
        self.player_hand_label.config(
            text=f"{self.format_hand(self.player_cards)}  (Score: {calculate_score(self.player_cards)})"
        )
        if hide_dealer:
            self.dealer_hand_label.config(
                text=f"{self.format_hand(self.dealer_cards, hide_first=True)}"
            )
        else:
            self.dealer_hand_label.config(
                text=f"{self.format_hand(self.dealer_cards)}  (Score: {calculate_score(self.dealer_cards)})"
            )

    def hit(self):
        self.player_cards.append(deal_card())
        self.update_display()

        if calculate_score(self.player_cards) > 21:
            self.end_game("You went over 21. You lose!")

    def stand(self):
        while calculate_score(self.dealer_cards) < 17:
            self.dealer_cards.append(deal_card())

        self.update_display(hide_dealer=False)

        player_score = calculate_score(self.player_cards)
        dealer_score = calculate_score(self.dealer_cards)

        if dealer_score > 21 or player_score > dealer_score:
            self.end_game("You win!")
        elif player_score < dealer_score:
            self.end_game("You lose!")
        else:
            self.end_game("It's a draw!")

    def end_game(self, result):
        self.status_label.config(text=result)
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)

    def reset_game(self):
        self.status_label.config(text="")
        self.deal_initial_cards()
        self.update_display()
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)


# ---------------------------
# Run
# ---------------------------
if __name__ == "__main__":
    root = tk.Tk()
    game = BlackjackGUI(root)
    root.mainloop()
