#! python3
# connect_4.py

import pprint
import logging
logging.basicConfig(level=logging.INFO)

BLANK_BOARD_VALUE = '-'


def is_sublist_in_sequence(seq, sublist):
    n = len(sublist)
    return sublist in (seq[i:i+n] for i in range(len(seq) + 1 - n))


def horizontal_four_check(seq, segment):
    return is_sublist_in_sequence(seq, segment)


def vertical_four_check(seq, column, board):
    column = [row[column] for row in board]
    return is_sublist_in_sequence(seq, column)


def negative_diagonal_four_check(row, column, board, win_sequence):
    negative_diagonal = []
    for i in range(-3, 4):
        position = board[row + i][column + i]
        logging.info('Cell position = %s' % position)
        try:
            negative_diagonal.append((position))
        except IndexError:
            pass
    logging.info('negative_diagonal = %s' % negative_diagonal)
    return is_sublist_in_sequence(negative_diagonal, win_sequence)


def positive_diagonal_four_check(board_p, board, sublist_p): # todo: improve argument names
    positive_diagonal = []
    for i in range(-3, 4):
        try:
            positive_diagonal.append(board[board_p + i][sublist_p + i])
        except IndexError:
            pass
    return is_sublist_in_sequence(positive_diagonal, win_sequence)


def generate_board(size):
    return [['-' for i in range(size)] for j in range(size)]


def get_player_1_token():
    player_1_token = str(input('Please choose your token player 1'))
    player_1_token = 'X'
    print(f'Thanks player 1. Your token is {player_1_token}')


def get_player_2_token():
    player_2_token = str(input('Please choose your token player 2'))
    print(f'Thanks player 2. Your token is {player_2_token}')
    return player_2_token


def show_board(board): # todo: show the board with numbered row and column displays
    pprint.pprint(board)


def choose_position_to_place_counter(player_number, board):
    while True:
        command = str(input(
            f"Player {str(player_number)}, please state the row and column" +
            "to place your token"))
        row, column = map(int, command.split())
        try:
            if board[row][column] != BLANK_BOARD_VALUE:
                print("That position is occupied. " +
                      "Please enter a different row and column")
                continue
            else:
                return (int(row), int(column))
        except (ValueError, IndexError) as e:
            print(f"The program suffered an error: {e}. " +
                  f"Please re-enter the row and column")


def place_counter(board, player_token, row, column):
    board[row][column] = player_token



def engine():
    board = generate_board(8)
    pprint.pprint(board)
    #player_1_token = get_player_1_token()
    p1_token = 'X'
    p1_win_seq = [p1_token for i in range(4)]
    #player_2_token = get_player_2_token()
    p2_token = 'O'
    is_game_complete = False
    while is_game_complete == False:
        x, y = choose_position_to_place_counter(1, board)
        place_counter(board, p1_token, x, y)
        show_board(board)
        is_game_complete = horizontal_four_check(board[x], p1_win_seq)
        is_game_complete = negative_diagonal_four_check(x, y, board, p1_win_seq)
        print(board[x])
        #vertical_four_check(player_1_token * 4, (), sublist, board)
        #x, y = choose_position_to_place_counter(2)
        #place_counter(p2_token, x, y)
        #how_board(board)
    print('Player won')

    segment = ['x', 'x']
    sequence = ['o', '-', 'x', 'x', 'o']
    print(is_sublist_in_sequence(sequence, segment))


# engine()


# After MVP, consider how to use classes to greater effect to run the game.