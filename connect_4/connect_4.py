#! python3
# connect_4.py

import pprint
from collections import deque
import logging
logging.basicConfig(level=logging.WARNING)

BLANK_BOARD_VALUE = '-'


def is_shorter_sequence_in_longer_sequence(shorter_sequence, longer_sequence):
    """Check if shorter sequence is in a longer sequence"""
    n = len(shorter_sequence)
    return shorter_sequence in (
        longer_sequence[i:i+n] for i in range(len(longer_sequence) + 1 - n)
    )

#suitable
def vertical_four_check(win_sequence, full_sequence):
    """Check row for four consecutive player tokens"""
    return is_shorter_sequence_in_longer_sequence(win_sequence, full_sequence)


def horizontal_four_check(board, column, win_sequence):
    """Check column in the board for four consecutive player tokens. """
    horizontal_values = []
    for i in range(len(board)):
        horizontal_values.append(board[i][board.index(column)])
    logging.info(f"horizontal values = {horizontal_values}")
    return is_shorter_sequence_in_longer_sequence(
        win_sequence, horizontal_values
    )

# todo: Rework
# def negative_diagonal_four_check(row, column, board, win_sequence):
#     """Check negative diagonal lines for four consecutive player tokens"""
#     negative_diagonal = []
#     for i in range(-3, 4):
#         try:
#             position = board[row + i][column + i]  # todo: Consider using the suppress module here
#             negative_diagonal.append(position)
#         except IndexError:
#             pass
#     logging.info(f"negative diagonal values = {negative_diagonal}")
#     return is_shorter_sequence_in_longer_sequence(win_sequence, negative_diagonal)

# todo: Rework
# def positive_diagonal_four_check(row, column, board, win_sequence):
#     """Check positive diagonal lines for four consecutive player tokens"""
#     positive_diagonal = []
#     for i in range(3, -4, -1):
#         try:
#             position = board[row - i][column + i]
#             positive_diagonal.append(position)
#         except IndexError:
#             pass
#     logging.info(f"positive_diagonal = {positive_diagonal}")
#     return is_shorter_sequence_in_longer_sequence(win_sequence, positive_diagonal)


def generate_board(size):
    """Generate board"""
    board = []
    for i in range(size):
        board.append([])
    return board


def get_player_1_token():
    """Assign player 1 game token"""
    player_1_token = str(input('Please enter one character to be your token player 1'))
    print(f'Thanks player 1. Your token is {player_1_token}')
    return player_1_token


def get_player_2_token():  # Todo: restrict token to being one character
    """Assign player 2 game token."""
    player_2_token = str(input('Please choose one character to be your token player 2'))
    print(f'Thanks player 2. Your token is {player_2_token}')
    return player_2_token



def show_board(board):
    """Show board to user."""
    for i in range(len(board)):
        for j in range(len(board)):
            try:
                print("|" + board[j][len(board) - 1 - i], end='| ')
            except IndexError:
                print("|" + "*", end='| ')
        print()


test_board = [
    ['1', 'o', '-', '-', '-'],
    ['x', 'o', '-', '-', 'o', 'X','o', '-'],
    ['x', 'o', '-', '-', '-', '-', '-', 'x'],
    ['x', 'o', '-', '2', '-', '-', '-', 'o'],
    ['x', 'o', '-', '-', '-', 'x','o', '-'],
    ['x', 'o', '-', '-', '-', '-', '-', 'x'],
    ['x', 'o', '-', '-', '-', '-', '-', 'o'],
    ['x', 'o', '-', '-', 'o', 'x','o', '3']
]


def choose_position_to_place_counter(player, board):
    """Get player integer input that fits on the board."""
    input_error_message = "The positions is out of the games's bounds. "
    while True:
        column = input(
            f"{player}, please state the column to place your token\n")
        if column.isdigit() is False:
            print(input_error_message)
        elif int(column) > (len(board) - 1):
            print(input_error_message)
        else:
            return int(column)



def place_counter(board, player_token, column):
    board[column].append(player_token)
    show_board(board)


def check_for_winner(x, board, player):
    """Combines the checks to determine if a player has won the game"""
    if horizontal_four_check(player['win_seq'], board[x]) is True:
        return player
    if vertical_four_check(board, y, player['win_seq']) is True:
        return player
    # if negative_diagonal_four_check(x, y, board, player['win_seq']) is True:
    #     return player
    # if positive_diagonal_four_check(x, y, board, player['win_seq']) is True:
    #     return player
    else:
        return False


def game_loop(players, board):
    """Run the game until a player wins the game."""
    winning_player = False
    while winning_player is False:
        for player in players:
            column = choose_position_to_place_counter(player['name'], board)
            place_counter(board, player['token'], column)
            winning_player = check_for_winner(column, board, player)
            if winning_player is not False:
                return winning_player


def engine():
    board = generate_board(8)
    show_board(board)
    #p1_token = get_player_1_token()
    p1_token = 'X'
    p1_win_seq = [p1_token] * 4
    #p2_token = get_player_2_token()
    p2_token = 'O'
    p2_win_seq = [p2_token] * 4
    players = [
        {'name':'player 1', 'token': p1_token, 'win_seq': p1_win_seq},
        {'name': 'player 2', 'token': p2_token, 'win_seq': p2_win_seq}
    ]
    winning_player = game_loop(players, board)
    print(f"{winning_player[name]} won the game!")


engine()

