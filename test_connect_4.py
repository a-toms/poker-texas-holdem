import connect_4
import random


def test_board_creation():
    n = random.randint(0, 30)
    board = connect_4.generate_board(n)
    assert len(board) == n
    assert len(board[0]) == n


def test_horizontal_check():
    test_board = connect_4.generate_board(8)
    test_token = 'T'
    test_win_sequence = [test_token, test_token, test_token, test_token]
    for i in range(4):
        connect_4.place_counter(test_token, i, 0)
    assert connect_4.horizontal_four_check(test_win_sequence,test_board[0]) == True



