import random

word_list = ["aardvark", "baboon", "camel"]
lives = 6
chosen_word = random.choice(word_list)
print("Randomly selected word:", chosen_word)

placeholder = ""
word_length = len(chosen_word)
for postion in range(word_length):
    placeholder += "_ "
print(placeholder)

game_over = False
correct_letters = []


while not game_over:
    guess = input("Guess the letter: ").lower()
    display = ""
    print("Your guess:", guess)

    for letter in chosen_word:
        if letter == guess:
            display += letter
            correct_letters.append(letter)
        elif letter in correct_letters:
            display += letter
        else:
            display += "_"

    print(display)

    if guess not in chosen_word:
        lives -= 1
        if lives == 0:
            print("You lose! The word was:", chosen_word)
            game_over = True
        print("Incorrect guess. Try again.")

    if "_" not in display:
        print("Congratulations! You've guessed the word:", chosen_word)
        game_over = True
