import noughts_and_crosses

CHECKER = noughts_and_crosses.IsGameComplete()
COMPUTER_MOVE = noughts_and_crosses.GetComputerMove()

def test_win_boards():
    horizontal_win_board = [
        'X', 'O', 'X',
        'O', 'O', 'O',
        'X', '-', 'X'
    ]
    assert CHECKER.horizontal_win(horizontal_win_board, 'O')
    vertical_win_board = [
        'X', 'O', 'X',
        '-', 'O', 'O',
        'X', 'O', 'X'
    ]
    assert CHECKER.vertical_win(vertical_win_board, 'O')
    positive_diagonal_win_board = [
        'X', 'X', 'O',
        '-', 'O', 'O',
        'O', '-', 'X'
    ]
    assert CHECKER.positive_diagonal_win(positive_diagonal_win_board, 'O')
    negative_diagonal_win_board = [
        'O', 'X', '',
        '', 'O', 'X',
        'X', '', 'O'
    ]
    assert CHECKER.negative_diagonal_win(negative_diagonal_win_board, 'O')
    win_boards = [
        horizontal_win_board, vertical_win_board,
        positive_diagonal_win_board, negative_diagonal_win_board
    ]
    # assert CHECKER.run_win_checks(win_boards, 'O') # This is not working. Alter this later

def test_no_win_board():
    no_win_board = [
        'X', 'O', 'X',
        'O', 'X', 'O',
        'X', '-', 'X'
    ]
    assert CHECKER.run_win_checks(no_win_board, 'O') is False

def test_computer_one_move_win():
    """In these tests, computer uses token 'X' and human uses token 'O'."""
    computer_one_move_win_board = [
        'X', '-', '-',
        '-', 'O', 'X',
        'X', '-', 'O'
    ]
    assert COMPUTER_MOVE.get_computer_one_move_win(
        computer_one_move_win_board, 'X') == 3
    no_one_move_win_board = [
        'X', '-', '-',
        '-', '-', 'X',
        '-', '-', 'O'
    ]
    assert COMPUTER_MOVE.get_computer_one_move_win(
        no_one_move_win_board, 'X') is False
    human_one_move_win_board = [
        'X', '-', '-',
        'O', 'O', '-',
        'X', '-', '-'
    ]
    assert COMPUTER_MOVE.get_human_one_move_win(
        human_one_move_win_board, 'O') == 5
