"""
tic_tac_toe (projekt_2.py): 
druhý projekt do Engeto Online Python Akademie

author: Ludek Mraz
email: ludek.mraz@centrum.cz
discord: Luděk M.#5570
"""

import os
import platform

all_positions = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
blank_field = " "


def clear_screen():
    '''
    Check OS platform to clear screen correctly
    '''
    if platform.system().lower() == "windows":
        os.system("cls")
    else:
        os.system("clear")


def game_fields() -> dict:
    '''
    Create dictionary from list of strings as keys and
    default values - blank.
    :return:
        Dictionary representing fields on the game board
    '''
    fields = dict()
    for position in all_positions:
        fields[position] = blank_field
    return fields
        

def game_board(fields: dict) -> str:
    '''
    Create game board from "fields" dictionary values.
    :param fields:
            Dictionary representing positions on the game board
            and stored values -> default is blank. Values get modified
            by player move.
    :return:
            Actual state of game board after each players' moves
    '''
    f = fields
    return f'''
    Fields map      Game board      
    +---+---+---+   +---+---+---+                                 
    | 1 | 2 | 3 |   | {f["1"]} | {f["2"]} | {f["3"]} |
    +---+---+---+   +---+---+---+                                 
    | 4 | 5 | 6 |   | {f["4"]} | {f["5"]} | {f["6"]} |  
    +---+---+---+   +---+---+---+                                 
    | 7 | 8 | 9 |   | {f["7"]} | {f["8"]} | {f["9"]} |
    +---+---+---+   +---+---+---+                                
    '''


def valid_move(fields: dict, player_move: str) -> bool:
    '''
    Check if move is valid.
    :param fields:
            Dictionary representing positions on the game board
            and stored values -> default is blank. Values get modified
            by player move.
    :param player_move:
            String representing player's input value.
            Value can only be put on blank fileds
    :return:
            True -> player's move is valid.
            False -> player's move is not valid.
    '''
    return player_move in all_positions and fields[player_move] == blank_field


def update_game_fields(fields: dict, player_move: str, player_stamp: str):
    '''
    Update game field in the dictionary with player's stamp.
    :param fields:
            Dictionary representing positions on the game board
            and stored values -> default is blank. Values get modified
            by player move.
    :param player_move:
            String representing player's input value.
            Value can only be put on blank fileds
    :param player_stamp:
            specific symbol, which representing player's move on
            game board.
    '''
    fields[player_move] = player_stamp


def check_winner(fields: dict, player_stamp: str) -> bool:
    '''
    Check if any of players won (has 3 stamps in a row either
    horizontally, vertically or diagonally.
    :param fields:
            Dictionary representing positions on the game board
            and stored values -> default is blank. Values get modified
            by player move.
    :param player_stamp:
            specific symbol, which representing player's move on
            game board.
    :return:
            True -> player won. Game over.
            False -> player lost.
    '''
    f, ps = fields, player_stamp
    return ((f['1'] == f['2'] == f['3'] == ps) or  # horizontal top
            (f['4'] == f['5'] == f['6'] == ps) or  # horizontal middle
            (f['7'] == f['8'] == f['9'] == ps) or  # horizontal bottom
            (f['1'] == f['4'] == f['7'] == ps) or  # vertical left
            (f['2'] == f['5'] == f['8'] == ps) or  # vertical middle
            (f['3'] == f['6'] == f['9'] == ps) or  # vertical right
            (f['1'] == f['5'] == f['9'] == ps) or  # diagonal \
            (f['3'] == f['5'] == f['7'] == ps))    # diagonal /


def check_if_tie(fields: dict) -> bool:
    '''
    Check if the game finished as a tie.
    :param fields:
            Dictionary representing positions on the game board
            and stored values -> default is blank. Values get modified
            by player move.
    :return:
            True -> game is a tie. Game over.
            False -> game is not a tie.
    '''
    for player_move in all_positions:
        if fields[player_move] == blank_field:
            return False
    return True


def game_run():  
    instructions = ('''
    Welcome to Tic Tac Toe
    ========================================
    GAME RULES:
    Each player can place one mark (or stone)
    per turn on the 3x3 grid. The WINNER is
    the one who succeeds in placing three of
    their marks in a:
    * horizontal,
    * vertical or
    * diagonal row.
    ========================================
    Let's start the game!
    ----------------------------------------''')  
    separator = "-" * 48
    first_player, second_player = "X", "O"  # Players' stamps
    gf = game_fields()

    while True:  # Main loop
        clear_screen()
        print(instructions)  
        print(game_board(gf))
        move = blank_field
        while not valid_move(gf, move):  # Run until valid move
            print(separator)
            move = input(f"Player '{first_player}' | Please, enter your move number: ")
            print(separator)
            if not move.isnumeric():  # Move is not number
                print("Non numeric inputs are not allowed! Try again!")
                continue
            elif move.isnumeric() and move not in all_positions:  # Move is not number between 1 and 9
                print("Use only numbers from 1 to 9!")
                continue
            elif gf[move] != blank_field:  # Move to occupied game field
                print("Selected field is not empty, select another one!")
                continue
        update_game_fields(gf, move, first_player)  # Update game field with player's move

        if check_winner(gf, first_player):  # Check if player won -> Game over
            clear_screen()
            print(instructions)  
            print(game_board(gf))
            print(f"Congratulations, player '{first_player}' WON!")
            break
        elif check_if_tie(gf):  # Check if game is a tie -> Game over
            clear_screen()
            print(instructions)  
            print(game_board(gf))
            print(f"The game is a tie!")
            break
        first_player, second_player = second_player, first_player  # Switch turns between players
    print("Game over!")


if __name__ == "__main__":
    game_run()