#! python3
# connect_4.py

import pprint, re


def is_sequence_present(seq, sublist):
    n = len(sublist)
    return sublist in (seq[i:i+n] for i in range(len(seq) + 1 - n))


def horizontal_four_check(seq, segment):
    return is_sequence_present(seq, segment)


def vertical_four_check(seq, column, col, board):
    column = [row[column] for row in board]
    return is_sequence_present(seq, column)


def negative_diagonal_four_check(board_p, board, sublist_p): # todo: improve argument names
    negative_diagonal = []
    for i in range(-3, 3):
        try:
            negative_diagonal.append(board[board_p + i][sublist_p + i])
        except IndexError:
            pass
    return is_sequence_present(seq, negative_diagonal)


def positive_diagonal_four_check(board_p, board, sublist_p): # todo: improve argument names
    positive_diagonal = []
    for i in range(-3, 3):
        try:
            positive_diagonal.append(board[board_p + i][sublist_p + i])
        except IndexError:
            pass
    return is_sequence_present(seq, positive_diagonal)


def generate_board(size):
    return [['-' for i in range(size)] for j in range(size)]


def get_player_1_token():
    player_1_token = str(input('Please choose your token player 1'))
    print(f'Thanks player 1. Your token is {player_1_token}')


def get_player_2_token():
    player_2_token = str(input('Please choose your token player 2'))
    print(f'Thanks player 2. Your token is {player_2_token}')
    return player_2_token


def show_board(board): # todo: show the board with numbered row and column displays
    pprint.pprint(board)


def choose_position_to_place_counter(player_number):# todo: add regex to allow for less strict user row and col input below
    try:
        command = str(input(
            f"Player {str(player_number)}, " +
            "please state the row and column to place your token. E.g., " +
            "1 3"
        ))
        row, column = command.split()
        return (int(row), int(column))
    except ValueError as e: # todo: manage IndexError where player enter value outside board
        print(f"Please re-enter row and column ({e}")
        choose_position_to_place_counter(player_number)


def place_counter(player_token, row, column):
    board[row][column] = player_token


# Engine
board = generate_board(8)
pprint.pprint(board)
#player_1_token = get_player_1_token()
p1_token = 'X'
p1_win_seq = p1_token * 4
#player_2_token = get_player_2_token()
p2_token = 'O'
while True:
    y, x  = choose_position_to_place_counter(1)
    place_counter(p1_token, x, y)
    show_board(board)
    horizontal_four_check(p1_win_seq, board[x])
    #vertical_four_check(player_1_token * 4, (), sublist, board)
    x, y = choose_position_to_place_counter(2)
    place_counter(p2_token, x, y)
    show_board(board)
#






segment = ['x', 'x']
sequence = ['o', '-', 'x', 'x', 'o']
print(is_sequence_present(sequence, segment))


