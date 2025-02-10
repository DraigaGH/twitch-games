from twitch_chat_irc import twitch_chat_irc
from dotenv import load_dotenv, find_dotenv
import os
import random

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

OAUTH_TOKEN = os.getenv("OAUTH_TOKEN")
CHANNEL = os.getenv("CHANNEL")
MY_CHANNEL = os.getenv("MY_CHANNEL")

connection = twitch_chat_irc.TwitchChatIRC("MY_CHANNEL", OAUTH_TOKEN)

play_game = {}

play_game_numbers = {}

#hangman stuff
with open("words.txt") as f:
    hangman_words = f.read().splitlines()

hangman_word = ""

playing_hangman = False

correct_guessed_letters = []

used_letters = {"a": False, "b": False, "c": False, "d": False, "e": False, "f": False, "g": False, "h": False, "i": False, "j": False, "k": False, "l": False,
                "m": False, "n": False, "o": False, "p": False, "q": False, "r": False, "s": False, "t": False, "u": False, "v": False, "w": False, "x": False,
                "y": False, "z": False}

guesses_left = 6

# reverse hangman stuff
reverse_word = ""
playing_reverse = False

reverse_guesses = 5

def send_command(message_sent):
    global hangman_word
    global playing_hangman
    global used_letters
    global guesses_left
    global correct_guessed_letters
    global reverse_word
    global playing_reverse
    global reverse_guesses

    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]

    if message_sent["display-name"] not in play_game:
        play_game[message_sent["display-name"]] = []
    
    if message_sent["display-name"] not in play_game_numbers:
        play_game_numbers[message_sent["display-name"]] = None

    if message_sent["message"] == "!commandlist":
        connection.send(CHANNEL, "The current command list added by Draiga is: !evidence, !subscribe, plink attack, and !playgame")

    if message_sent["message"] == "!evidence":
        connection.send(CHANNEL, "I have a stupid amount of evidence that this run is spliced. Looking for someone who can actually look at this evidence and start asking questions because the more i view the run the more i have. If this evidence is just looked away from i will make a public video on the exposure regardless, and be way harsher in the process. i assume youd like to take this to a private dm because what i have to show and tell is just to damning..")

    elif message_sent["message"] == "!subscribe":
        connection.send(CHANNEL, "Did you know that with twitch prime, you can subscribe for the low low price of 0?")

    elif message_sent["message"] == "plink attack":
        connection.send(CHANNEL, "plink plenk plinktosis plunk plink-182 plinkge")

    elif message_sent["message"] == "!playgame":
        connection.send(CHANNEL, f"@{str(message_sent["display-name"])}, I have picked a number between 1 and 10. Try to guess what it is. ")
        play_game_numbers[message_sent["display-name"]] = random.randint(1, 10)
        play_game[message_sent["display-name"]] = True
    
    elif play_game[message_sent["display-name"]]:
        integers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]

        if message_sent["message"] in integers:
            if int(message_sent["message"]) < play_game_numbers[message_sent["display-name"]]:
                connection.send(CHANNEL, f"@{message_sent["display-name"]}, your guess was too low.")
            
            if int(message_sent["message"]) > play_game_numbers[message_sent["display-name"]]:
                connection.send(CHANNEL, f"@{message_sent["display-name"]}, your guess was too high.")
            
            if int(message_sent["message"]) == play_game_numbers[message_sent["display-name"]]:
                connection.send(CHANNEL, f"@{message_sent["display-name"]}, you correctly guessed the number!")
                play_game[message_sent["display-name"]] = False
                play_game_numbers[message_sent["display-name"]] = None
    
    elif message_sent["message"] == "!hangman" and not playing_hangman:
        while len(hangman_word) < 5:
            hangman_word = hangman_words[random.randint(0, len(hangman_words))]

        first_message = "I have picked a word at random, send letters to try to guess what it is! "
        
        for i in range(len(hangman_word)):
            first_message += "_ "
        
        first_message += f"(Guesses left: {guesses_left})"

        print(f"THE WORD IS {hangman_word}")

        connection.send(CHANNEL, first_message)

        playing_hangman = True
    
    elif playing_hangman and message_sent["message"].lower() in alphabet:
        guess = message_sent["message"].lower()
        new_message = ""

        if used_letters[guess.lower()]:
            if guesses_left == 1:
                new_message = f"You've already guessed {guess}. You have {guesses_left} guess left. "
            else:
                new_message = f"You've already guessed {guess}. You have {guesses_left} guesses left. "
            
            for letter in hangman_word:
                if used_letters[letter]:
                    new_message += f"{letter} "
                
                else:
                    new_message += "_ "

            connection.send(CHANNEL, new_message)
            return None

        used_letters[guess] = True
        
        if guess in hangman_word:
            for i in range(hangman_word.count(guess)):
                correct_guessed_letters.append(guess)
        
        else:
            guesses_left -= 1
        
        if guesses_left > 1:
            new_message += f"{guesses_left} guesses left! "

        else:
            new_message += f"{guesses_left} guess left! "

        for letter in hangman_word:
            if used_letters[letter]:
                new_message += f"{letter} "
            
            else:
                new_message += "_ "
        
        if guesses_left == 0:
            new_message = ""
            new_message += "You lost! The word was "
            for letter in hangman_word:
                new_message += f"{letter}"
            
            connection.send(CHANNEL, new_message)
            playing_hangman = False

            used_letters = {"a": False, "b": False, "c": False, "d": False, "e": False, "f": False, "g": False, "h": False, "i": False, "j": False, "k": False, "l": False,
                "m": False, "n": False, "o": False, "p": False, "q": False, "r": False, "s": False, "t": False, "u": False, "v": False, "w": False, "x": False,
                "y": False, "z": False}

            guesses_left = 6

            hangman_word = ""

            correct_guessed_letters = []
        
        elif set(correct_guessed_letters) == set(list(hangman_word)):
            new_message = "You win! The word was "
            
            for letter in hangman_word:
                new_message += f"{letter}"

            connection.send(CHANNEL, new_message)
            playing_hangman = False

            used_letters = {"a": False, "b": False, "c": False, "d": False, "e": False, "f": False, "g": False, "h": False, "i": False, "j": False, "k": False, "l": False,
                "m": False, "n": False, "o": False, "p": False, "q": False, "r": False, "s": False, "t": False, "u": False, "v": False, "w": False, "x": False,
                "y": False, "z": False}

            guesses_left = 6

            hangman_word = ""

            correct_guessed_letters = []
        
        else:
            connection.send(CHANNEL, new_message)

    elif message_sent["message"].split()[0] == "!guessword" and playing_hangman:
        if len(message_sent["message"].split()) == 1:
            new_message = "Please add the word you wish to guess after !guessword. "

            if guesses_left == 1:
                new_message += f"{guesses_left} guess left. "
            
            else:
                new_message += f"{guesses_left} guesses left. "

            for letter in hangman_word: 
                if used_letters[letter]:
                    new_message += f"{letter} "
                
                else:
                    new_message += "_ "
        
            connection.send(CHANNEL, new_message)
    
        else:
            if message_sent["message"].split()[1].lower() == hangman_word:
                new_message = f"You win! The word was {hangman_word}"

                playing_hangman = False

                used_letters = {"a": False, "b": False, "c": False, "d": False, "e": False, "f": False, "g": False, "h": False, "i": False, "j": False, "k": False, "l": False,
                    "m": False, "n": False, "o": False, "p": False, "q": False, "r": False, "s": False, "t": False, "u": False, "v": False, "w": False, "x": False,
                    "y": False, "z": False}

                guesses_left = 6

                hangman_word = ""

                correct_guessed_letters = []

                connection.send(CHANNEL, new_message)
            
            else:
                new_message = f"{message_sent["message"].split()[1].lower()} was not the word. "

                guesses_left -= 1
                
                if guesses_left == 1:
                    new_message += f"{guesses_left} guess left. "
            
                else:
                    new_message += f"{guesses_left} guesses left. "

                for letter in hangman_word:
                    if used_letters[letter]:
                        new_message += f"{letter} "
                    
                    else:
                        new_message += "_ "
                
                if guesses_left == 0:
                    new_message = f"You lost! The word was {hangman_word}"

                    playing_hangman = False

                    used_letters = {"a": False, "b": False, "c": False, "d": False, "e": False, "f": False, "g": False, "h": False, "i": False, "j": False, "k": False, "l": False,
                        "m": False, "n": False, "o": False, "p": False, "q": False, "r": False, "s": False, "t": False, "u": False, "v": False, "w": False, "x": False,
                        "y": False, "z": False}

                    guesses_left = 6

                    hangman_word = ""

                    correct_guessed_letters = []

                connection.send(CHANNEL, new_message)
    
    # --------- REVERSE HANGMAN HERE -------------
    elif message_sent["message"] == "!reversehangman" and not playing_reverse:
        print(f"THE LENGTH IS {len(reverse_word)}")
        while len(reverse_word) < 5 or len(reverse_word) > 8:
            reverse_word = hangman_words[random.randint(0, len(hangman_words))]

        print(f"THE WORD IS {reverse_word}")

        first_message = f"I have picked a word at random with length {len(reverse_word)} and letters "

        reverse_letters = []

        for letter in reverse_word:
            if letter not in reverse_letters:
                reverse_letters.append(letter)

        random.shuffle(reverse_letters)

        for letter in reverse_letters[0:len(reverse_letters) - 1]:
            first_message += f"{letter}, "
        
        first_message += reverse_letters[-1]
        
        first_message += ". What word am I thinking of? "

        first_message += f"You have {reverse_guesses} guesses."

        playing_reverse = True
        connection.send(CHANNEL, first_message)
    
    elif message_sent["message"].split()[0] == "!guess" and playing_reverse:
        if len(message_sent["message"].split()) == 1:
            if reverse_guesses > 1:
                new_message = f"Please add the word you want to guess after !guess. You have {reverse_guesses} guesses left"
            else:
                new_message += f"Please add the word you want to guess after !guess. You have {reverse_guesses} guess left"
            
            connection.send(CHANNEL, new_message)

        else:
            if message_sent["message"].split()[1].lower() == reverse_word:
                new_message = f"You win! The word was {reverse_word}"

                connection.send(CHANNEL, new_message)

                reverse_word = ""
                playing_reverse = False
                reverse_guesses = 5
            
            else:
                reverse_guesses -= 1
                
                if reverse_guesses == 1:
                    new_message = f"{message_sent["message"].split()[1].lower()} was not the word. You have {reverse_guesses} guess left."
                
                elif reverse_guesses > 1:
                    new_message = f"{message_sent["message"].split()[1].lower()} was not the word. You have {reverse_guesses} guesses left."
                
                else:
                    new_message = f"You lose! The word was {reverse_word}"
                    playing_reverse = False
                    reverse_word = ""
                    reverse_guesses = 5

                connection.send(CHANNEL, new_message)
            
            
def main():
    connection.listen(CHANNEL, on_message=send_command)


if __name__ == "__main__":
    main()