import tkinter as tk
import random
from tkinter import messagebox


class TicTacToeAI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("AI Tic Tac Toe Trainer Using Genetic Algorithm")
        self.board = [""] * 9
        self.buttons = []
        self.population = self.initialize_population(10)
        self.fitness_scores = [0] * len(self.population)
        self.current_player = "Player"
        self.starting_player = "Player"
        self.score = {"Player": 0, "AI": 0}
        self.best_fitness = -float('inf')
        self.mode = "AI"  # AI or Player vs Player
        self.create_ui()
        self.start_game()

    def create_ui(self):
        frame = tk.Frame(self.window)
        frame.pack()
        for row in range(3):
            for col in range(3):
                button = tk.Button(
                    frame,
                    text="",
                    font=("Arial", 24),
                    width=5,
                    height=2,
                    command=lambda r=row, c=col: self.player_move(r * 3 + c),
                )
                button.grid(row=row, column=col)
                self.buttons.append(button)

        reset_button = tk.Button(
            self.window, text="Reset Game", command=self.reset_game
        )
        reset_button.pack()

        self.score_label = tk.Label(self.window, text=f"Player: {self.score['Player']} - AI: {self.score['AI']}")
        self.score_label.pack()

    def initialize_population(self, size):
        return [[random.randint(0, 1) for _ in range(9)] for _ in range(size)]

    def start_game(self):
        self.board = [""] * 9
        for button in self.buttons:
            button.config(text="", state=tk.NORMAL)
        self.current_player = self.starting_player
        if self.mode == "AI" and self.current_player == "AI":
            self.ai_move()

    def reset_game(self):
        self.score = {"Player": 0, "AI": 0}
        self.best_fitness = -float('inf')  # Reset best fitness when resetting the game
        self.score_label.config(text=f"Player: {self.score['Player']} - AI: {self.score['AI']}")
        self.start_game()

    def player_move(self, index):
        if self.board[index] == "" and self.current_player == "Player":
            self.board[index] = "X"
            self.buttons[index].config(text="X", state=tk.DISABLED)
            if not self.check_winner():
                self.current_player = "AI"
                if self.mode == "AI":
                    self.ai_move()

    def ai_move(self):
        best_move = self.get_best_move()
        if best_move is not None:
            self.board[best_move] = "O"
            self.buttons[best_move].config(text="O", state=tk.DISABLED)
            if not self.check_winner():
                self.current_player = "Player"

    def get_best_move(self):
        valid_moves = [i for i, cell in enumerate(self.board) if cell == ""]
        if not valid_moves:
            return None

        # Check for a winning move
        winning_move = self.find_winning_move("O")
        if winning_move is not None:
            return winning_move

        # Check if the player has a winning move that needs to be blocked
        blocking_move = self.find_winning_move("X")
        if blocking_move is not None:
            return blocking_move

        # Otherwise, take the center if available, then corners
        if 4 in valid_moves:
            return 4  # Center position
        corners = [0, 2, 6, 8]
        for corner in corners:
            if corner in valid_moves:
                return corner

        # Take any available valid move
        return random.choice(valid_moves)

    def find_winning_move(self, player):
        for line in self.get_winning_lines():
            values = [self.board[i] for i in line]
            if values.count(player) == 2 and values.count("") == 1:
                return line[values.index("")]
        return None

    def get_winning_lines(self):
        return [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]

    def check_winner(self):
        for line in self.get_winning_lines():
            values = [self.board[i] for i in line]
            if values.count("X") == 3:
                self.end_game("Player Wins!")
                return True
            elif values.count("O") == 3:
                self.end_game("AI Wins!")
                return True
        if "" not in self.board:
            self.end_game("It's a Draw!")
            return True
        return False

    def end_game(self, message):
        for button in self.buttons:
            button.config(state=tk.DISABLED)
        messagebox.showinfo("Game Over", message)
        if "Player" in message:
            self.score["Player"] += 1
        elif "AI" in message:
            self.score["AI"] += 1
        self.score_label.config(text=f"Player: {self.score['Player']} - AI: {self.score['AI']}")
        self.start_game()
        self.update_fitness(message)

    def update_fitness(self, result):
        fitness_change = 0
        if "Player Wins" in result:
            fitness_change = -10  # AI loses
        elif "AI Wins" in result:
            fitness_change = 10  # AI wins
        elif "It's a Draw" in result:
            fitness_change = 0  # No change for a draw
        self.update_population(fitness_change)
        self.print_best_fitness()

    def update_population(self, fitness_change):
        for i, individual in enumerate(self.population):
            self.fitness_scores[i] += fitness_change
        self.population = self.evolve_population()

    def evolve_population(self):
        sorted_population = sorted(
            zip(self.population, self.fitness_scores), key=lambda x: x[1], reverse=True
        )
        top_individuals = [x[0] for x in sorted_population[:len(self.population) // 2]]
        new_population = []
        for _ in range(len(self.population)):
            parent1 = random.choice(top_individuals)
            parent2 = random.choice(top_individuals)
            if parent1 is not None and parent2 is not None:
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                new_population.append(child)
        return new_population

    def crossover(self, parent1, parent2):
        crossover_point = random.randint(0, len(parent1) - 1)
        return parent1[:crossover_point] + parent2[crossover_point:]

    def mutate(self, individual, mutation_rate=0.1):
        return [gene if random.random() > mutation_rate else 1 - gene for gene in individual]

    def print_best_fitness(self):
        current_best_fitness = max(self.fitness_scores)
        if current_best_fitness > self.best_fitness:
            self.best_fitness = current_best_fitness
        print(f"Best fitness achieved: {self.best_fitness}")

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    game = TicTacToeAI()
    game.run()
