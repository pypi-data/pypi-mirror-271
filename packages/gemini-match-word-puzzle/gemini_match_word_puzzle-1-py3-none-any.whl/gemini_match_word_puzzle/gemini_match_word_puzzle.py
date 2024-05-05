"""
This file contains code for the game "Gemini Match Word Puzzle".
Author: SoftwareApkDev
"""


# Importing necessary libraries


import sys
import random
import copy
import google.generativeai as gemini
import os
from dotenv import load_dotenv
from mpmath import mp, mpf
from tabulate import tabulate

mp.pretty = True


# Creating static functions to be used in this game.


def is_number(string: str) -> bool:
    try:
        mpf(string)
        return True
    except ValueError:
        return False


def all_tiles_opened(board: list) -> bool:
    for y in range(len(board)):
        for x in range(len(board[y])):
            curr_tile: Tile = board[y][x]
            if not curr_tile.is_opened:
                return False
    return True


def clear():
    # type: () -> None
    if sys.platform.startswith('win'):
        os.system('cls')  # For Windows System
    else:
        os.system('clear')  # For Linux System


# Creating necessary class.


class Tile:
    """
    This class contains attributes of a tile on a board.
    """

    def __init__(self, contents):
        # type: (str) -> None
        self.contents: str = contents
        self.is_opened: bool = False

    def open(self):
        # type: () -> None
        self.is_opened = True

    def __str__(self):
        # type: () -> str
        return self.contents.upper() if self.is_opened else "CLOSED"

    def clone(self):
        # type: () -> Tile
        return copy.deepcopy(self)


# Creating main function used to run the application.


def main() -> int:
    """
    This main function is used to run the application.
    :return: an integer
    """

    load_dotenv()
    gemini.configure(api_key=os.environ['GEMINI_API_KEY'])

    # Asking user input values for generation config
    temperature: str = input("Please enter temperature (0 - 1): ")
    while not is_number(temperature) or float(temperature) < 0 or float(temperature) > 1:
        temperature = input("Sorry, invalid input! Please re-enter temperature (0 - 1): ")

    float_temperature: float = float(temperature)

    top_p: str = input("Please enter Top P (0 - 1): ")
    while not is_number(top_p) or float(top_p) < 0 or float(top_p) > 1:
        top_p = input("Sorry, invalid input! Please re-enter Top P (0 - 1): ")

    float_top_p: float = float(top_p)

    top_k: str = input("Please enter Top K (at least 1): ")
    while not is_number(top_k) or int(top_k) < 1:
        top_k = input("Sorry, invalid input! Please re-enter Top K (at least 1): ")

    float_top_k: int = int(top_k)

    max_output_tokens: str = input("Please enter maximum input tokens (at least 1): ")
    while not is_number(max_output_tokens) or int(max_output_tokens) < 1:
        max_output_tokens = input("Sorry, invalid input! Please re-enter maximum input tokens (at least 1): ")

    int_max_output_tokens: int = int(max_output_tokens)

    # Set up the model
    generation_config = {
        "temperature": float_temperature,
        "top_p": float_top_p,
        "top_k": float_top_k,
        "max_output_tokens": int_max_output_tokens,
    }

    safety_settings = [
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE"
        },
    ]

    model = gemini.GenerativeModel(model_name="gemini-1.0-pro",
                                   generation_config=generation_config,
                                   safety_settings=safety_settings)

    convo = model.start_chat(history=[
    ])

    while True:
        clear()
        num_words: int = random.randint(2, 10)
        words: list = []  # initial value
        language: str = random.choice(["Python", "Java", "C++", "JavaScript", "SQL", "PHP"])
        prompt: str = "Generate " + str(num_words) + " random " + str(language) \
                      + " keywords (include the list of keywords only in your response, one word per line)!"
        convo.send_message(prompt)
        response: str = str(convo.last.text)
        response_lines: list = response.split("\n")
        for line in response_lines:
            line_words: list = line.split(" ")
            if len(line_words) > 1:
                words.append(line.split(" ")[1].upper())
            else:
                words.append(line.upper())

        words_tally: dict = {}
        for word in words:
            words_tally[word] = 0

        board: list = [[], []]
        for i in range(len(board)):
            for j in range(num_words):
                curr_word: str = random.choice(words)
                while words_tally[curr_word] >= 2:
                    curr_word = random.choice(words)

                board[i].append(Tile(curr_word))
                words_tally[curr_word] += 1

        while not all_tiles_opened(board):
            print("Below is how the board looks like:\n" +
                  str(tabulate(board, headers='firstrow', tablefmt='fancy_grid')))
            x_coords1: int = int(input("Please enter x-coordinates of the first tile "
                                       "you want to open (0 - " + str(len(board[0]) - 1) + "): "))
            y_coords1: int = int(input("Please enter y-coordinates of the first tile "
                                       "you want to open (0 - " + str(len(board) - 1) + "): "))
            while x_coords1 < 0 or x_coords1 >= len(board[0]) or y_coords1 < 0 or y_coords1 >= len(board):
                print("Sorry, invalid input!")
                x_coords1 = int(input("Please enter x-coordinates of the first tile "
                                           "you want to open (0 - " + str(len(board[0]) - 1) + "): "))
                y_coords1 = int(input("Please enter y-coordinates of the first tile "
                                           "you want to open (0 - " + str(len(board) - 1) + "): "))

            x_coords2: int = int(input("Please enter x-coordinates of the second tile "
                                       "you want to open (0 - " + str(len(board[0]) - 1) + "): "))
            y_coords2: int = int(input("Please enter y-coordinates of the second tile "
                                       "you want to open (0 - " + str(len(board) - 1) + "): "))
            while x_coords2 < 0 or x_coords2 >= len(board[0]) or y_coords2 < 0 or y_coords2 >= len(board) or \
                    (x_coords1 == x_coords2 and y_coords1 == y_coords2):
                print("Sorry, invalid input!")
                x_coords2 = int(input("Please enter x-coordinates of the second tile "
                                           "you want to open (0 - " + str(len(board[0]) - 1) + "): "))
                y_coords2 = int(input("Please enter y-coordinates of the second tile "
                                           "you want to open (0 - " + str(len(board) - 1) + "): "))

            first_tile: Tile = board[y_coords1][x_coords1]
            second_tile: Tile = board[y_coords2][x_coords2]
            if first_tile.contents == second_tile.contents:
                first_tile.open()
                second_tile.open()

        print("You completed the puzzle!")
        print("Enter \"Y\" for yes.")
        print("Enter anything else for no.")
        continue_playing: str = input("Do you want to continue playing \"Gemini Match Word Puzzle\"? ")
        if continue_playing != "Y":
            return 0


if __name__ == '__main__':
    main()
