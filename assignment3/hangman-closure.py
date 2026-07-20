def make_hangman(secret_word):
    guesses = []

    def hangman_closure(guess):
        if guess not in guesses:
            guesses.append(guess)

        so_far = ""

        for letter in secret_word:
            if letter in guesses:
                so_far += letter
            else:
                so_far += "_"
        
        print(so_far)

        for letter in so_far:
            if letter not in secret_word:
                return False

        return True
    
    return hangman_closure

print("--- Task 4 ---\n")
print("Welcome to Hangman!\n")

secret_word = input("What's the secret word?: ")
game = make_hangman(secret_word)

complete = False

while complete == False:
    guess = input("Guess a letter: ")
    complete = game(guess)

print(f"You guessed the word {secret_word}!")