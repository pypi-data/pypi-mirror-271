# Python program to implement Morse Code Translator
from audio import play
import time

"""
VARIABLE KEY
'cipher' -> 'stores the morse translated form of the english string'
'decipher' -> 'stores the english translated form of the morse string'
'citext' -> 'stores morse code of a single character'
'i' -> 'keeps count of the spaces between morse characters'
'message' -> 'stores the string to be encoded or decoded'
"""

# Dictionary representing the morse code chart
MORSE_CODE_DICT = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    "0": "-----",
    ", ": "--..--",
    ".": ".-.-.-",
    "?": "..--..",
    "/": "-..-.",
    "-": "-....-",
    "(": "-.--.",
    ")": "-.--.-",
}


# Function to encrypt the string
# according to the morse code chart
def encrypt(message):
    cipher = ""
    for letter in message:
        if letter != " ":
            try:
                # Looks up the dictionary and adds the
                # corresponding morse code
                # along with a space to separate
                # morse codes for different characters
                cipher += MORSE_CODE_DICT[letter] + " "
            except:
                pass
        else:
            try:
                # 1 space indicates different characters
                # and 2 indicates different words
                cipher += " "
            except:
                pass

    return cipher


# Function to decrypt the string
# from morse to english
def decrypt(message):

    # extra space added at the end to access the
    # last morse code
    message += " "

    decipher = ""
    citext = ""
    for letter in message:

        # checks for space
        if letter != " ":

            # counter to keep track of space
            i = 0

            # storing morse code of a single character
            citext += letter

        # in case of space
        else:
            # if i = 1 that indicates a new character
            i += 1

            # if i = 2 that indicates a new word
            if i == 2:

                # adding space to separate words
                decipher += " "
            else:

                # accessing the keys using their values (reverse of encryption)
                decipher += list(MORSE_CODE_DICT.keys())[
                    list(MORSE_CODE_DICT.values()).index(citext)
                ]
                citext = ""

    return decipher


# Hard-coded driver function to run the program
# def main():
#    message = input("Message: ")
#    result = encrypt(message.upper())
#    print(result)
#    long = 0.5
#    verrylong = 1
#    short = 0.2
#    current = 0
#    for i in result:
#        if i == ".":
#            current = short
#            play(length=current)
#        if i == "-":
#            current = long
#            play(length=current)
#        if i == " ":
#            time.sleep(verrylong)
# message = "--. . . -.- ... -....- ..-. --- .-. -....- --. . . -.- ... "
# result = decrypt(message)
# print(result)


# Executes the main function
if __name__ == "__main__":
    main()
