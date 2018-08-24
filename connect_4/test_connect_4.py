import unittest
import connect_4
import logging
logging.basicConfig(level=logging.INFO)


class TestSetup(unittest.TestCase):

    test_board = connect_4.generate_board(8)
    test_token = 'T'

    def generate_win_sequence(self):
        return [self.test_token] * 4


test_board = [
    ['o', 'o', '-', '-', '-'],
    ['x', 'x', '-', '-', 'o', 'X','o', '-'],
    ['x', 'o', 'x', 'o', '-', '-', '-', 'x'],
    ['x', 'o', '-', 'x', '1', '-', '-', 'o'],
    ['x', 'x', 'u', '1', '*', 'o','o', '-'],
    ['x', 'o', '1', 'o', '-', 'o', 'o', 'x'],
    ['x', '1', '-', '*', 'o', '-', '-', 'o'],
    ['x', 'o', '-', '-', '*', 'x','o', '3']
]

class TestHorizontalAndVerticalGameSuccess(TestSetup):

    def test_horizontal_check(self):
        test_win_sequence = self.generate_win_sequence()
        row = 5
        for i in range(4):
            connect_4.place_counter(self.test_board, self.test_token, row, i)
        self.assertTrue(
            connect_4.horizontal_focheck(
                test_win_sequence, self.test_board[row])
        )

    def test_vertical_check(self):
        test_win_sequence = self.generate_win_sequence()
        column = 6
        for i in range(4):
            connect_4.place_counter(
                self.test_board, self.test_token, i, column)
        self.assertTrue(
            connect_4.vertical_four_check(
                self.test_board, column, test_win_sequence)
        )


class TestNegativeDiagonalGameSuccess(TestSetup):

    def test_negative_diagonal_check(self):
        for i in range(-4, 2):
            connect_4.place_counter(self.test_board, self.test_token, i, i)
        test_win_sequence = self.generate_win_sequence()
        self.assertTrue(connect_4.negative_diagonal_four_check(
            4, 4, self.test_board, test_win_sequence))


class TestPositiveDiagonalGameSuccess(unittest.TestCase):
    def generate_win_sequence(self):
        return [self.test_token] * 4
    test_board = connect_4.generate_board(8)
    test_token = 'T'
    def test_positive_diagonal_check(self):
        connect_4.place_counter(self.test_board, 'T', 3, 0)
        connect_4.place_counter(self.test_board, 'T', 2, 1)
        connect_4.place_counter(self.test_board, 'T', 1, 2)
        connect_4.place_counter(self.test_board, 'T', 0, 3)
        self.assertTrue(connect_4.positive_diagonal_four_check(
            2, 1, self.test_board, self.generate_win_sequence()))




