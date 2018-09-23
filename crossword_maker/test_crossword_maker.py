import crossword_maker

def test_create_blank_board():
    board = crossword_maker.create_board(50, 50)
    assert type(board) is list
    for i in range(50**2):
        assert type(board[i]) is type(dict())
