import random


def check_answer(user_guess, actual_answer):
    if not 1 <= user_guess <= 100:
        print("Out of range (1–100).")
        return False
    elif user_guess > actual_answer:
        print("Too high.")
    elif user_guess < actual_answer:
        print("Too low.")
    else:
        print(f"You got it! The number was {actual_answer} 🎉")
        return True
    return False


print("Welcome to the Number Guessing Game!")
print("I'm thinking of a number between 1 and 100.")

level = input("Type 'easy' or 'hard': ").strip().lower()
attempts = 10 if level == "easy" else 5
num = random.randint(1, 100)

print(f"You have {attempts} attempts remaining.")

while attempts > 0:
    try:
        guess = int(input("Make a guess: "))
    except ValueError:
        print("Please enter a valid number.")
        continue

    if check_answer(guess, num):
        break

    attempts -= 1
    if attempts > 0:
        print(f"Guess again. Attempts left: {attempts}")
    else:
        print(f"You're out of attempts 😢. The number was {num}.")
