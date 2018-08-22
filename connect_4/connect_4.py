#! python3
# connect_4.py

import pprint
import logging
logging.basicConfig(level=logging.DEBUG)

BLANK_BOARD_VALUE = '-'


def is_shorter_sequence_in_longer_sequence(shorter_sequence, longer_sequence):
    n = len(shorter_sequence)
    return shorter_sequence in (
        longer_sequence[i:i+n] for i in range(len(longer_sequence) + 1 - n))


def horizontal_four_check(win_sequence, full_sequence):
    return is_shorter_sequence_in_longer_sequence(win_sequence, full_sequence)


def vertical_four_check(board, column, win_sequence):
    column_values = []
    for row in board:
        column_values.append(row[column])
    logging.info(f"vertical column_values = {column_values}")
    return is_shorter_sequence_in_longer_sequence(win_sequence, column_values)


def negative_diagonal_four_check(row, column, board, win_sequence):
    negative_diagonal = []
    for i in range(-3, 4):
        try:
            position = board[row + i][column + i]  # todo: Consider using the suppress module here
            negative_diagonal.append(position)
        except IndexError:
            pass
    logging.info(f"negative diagonal values = {negative_diagonal}")
    return is_shorter_sequence_in_longer_sequence(win_sequence, negative_diagonal)


def positive_diagonal_four_check(row, column, board, win_sequence):
    positive_diagonal = []
    for i in range(3, -4, -1):
        try:
            position = board[row - i][column + i]
            positive_diagonal.append(position)
        except IndexError:
            pass
    logging.info(f"positive_diagonal = {positive_diagonal}")
    return is_shorter_sequence_in_longer_sequence(win_sequence, positive_diagonal)


def generate_board(size):
    return [['-' for i in range(size)] for j in range(size)]


def get_player_1_token():
    player_1_token = str(input('Please choose your token player 1'))
    print(f'Thanks player 1. Your token is {player_1_token}')
    return player_1_token

def get_player_2_token():
    player_2_token = str(input('Please choose your token player 2'))
    print(f'Thanks player 2. Your token is {player_2_token}')
    return player_2_token


def show_board(board):  # todo: show the board with numbered row and column displays
    pprint.pprint(board)


def choose_position_to_place_counter(player, board):
    while True:
        try:
            command = str(input(
                f"{player}, please state the row and column " +
                "to place your token"))
            row, column = map(int, command.split())
            if board[row][column] != BLANK_BOARD_VALUE:
                print("That position is occupied. " +
                      "Please enter a different row and column")
                continue
            else:
                return row, column
        except (ValueError, IndexError) as e:
            print(f"The program suffered an error: {e}. " +
                  f"Please re-enter the row and column")


def place_counter(board, player_token, row, column):
    board[row][column] = player_token


def check_for_winner(x, y, board, player):
    if horizontal_four_check(player['win_seq'], board[x]) is True:
        return player
    if negative_diagonal_four_check(x, y, board, player['win_seq']) is True:
        return player
    if vertical_four_check(board, y, player['win_seq']) is True:
        return player
    if positive_diagonal_four_check(x, y, board, player['win_seq']) is True:
        return player
    else:
        return False


def game_loop(players, board):
    winning_player = False
    while winning_player is False:
        for player in players:
            x, y = choose_position_to_place_counter(player['name'], board)
            place_counter(board, player['token'], x, y)
            show_board(board)
            winning_player = check_for_winner(x, y, board, player)
    return winning_player


def engine():  # todo: simplify this
    board = generate_board(8)
    show_board(board)
    p1_token = get_player_1_token()
    p1_win_seq = [p1_token] * 4
    logging.info(p1_win_seq)
    p2_token = get_player_2_token()
    p2_win_seq = [p2_token] * 4
    logging.info(p2_win_seq)
    players = [
        {'name':'player 1', 'token': p1_token, 'win_seq': p1_win_seq},
        {'name': 'player 2', 'token': p2_token, 'win_seq': p2_win_seq}
    ]
    winning_player = game_loop(players, board)
    print(f'{winning_player} won')


engine()

# todo: consider refactoring the program to use classes
