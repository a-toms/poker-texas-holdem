import unittest
import connect_4
import logging
logging.basicConfig(level=logging.INFO)


class TestSetup(unittest.TestCase):

    test_board = connect_4.generate_board(8)
    test_token = 'T'

    def generate_win_sequence(self):
        return [self.test_token for i in range(4)]

    def test_board_creation(self):
        n = 10
        board = connect_4.generate_board(n)
        self.assertEqual(len(board), n)
        self.assertEqual(len(board[0]), n)


class TestHorizontalAndVerticalGameSuccess(TestSetup):

    def test_horizontal_check(self):
        test_win_sequence = self.generate_win_sequence()
        row = 5
        for i in range(4):
            connect_4.place_counter(self.test_board, self.test_token, row, i)
        self.assertTrue(
            connect_4.horizontal_four_check(
                test_win_sequence, self.test_board[row]))

    def test_vertical_check(self):
        test_win_sequence = self.generate_win_sequence()
        column = 6
        for i in range(4):
            connect_4.place_counter(
                self.test_board, self.test_token, i, column)
        self.assertTrue(
            connect_4.vertical_four_check(
                self.test_board, column, test_win_sequence))


class TestNegativeDiagonalGameSuccess(TestSetup):

    def test_negative_diagonal_check(self):
        for i in range(-4, 2):
            connect_4.place_counter(self.test_board, self.test_token, i, i)
        test_win_sequence = self.generate_win_sequence()
        self.assertTrue(connect_4.negative_diagonal_four_check(
            4, 4, self.test_board, test_win_sequence))


class TestPositiveDiagonalGameSuccess(unittest.TestCase):
    def generate_win_sequence(self):
        return [self.test_token for i in range(4)]
    test_board = connect_4.generate_board(8)
    test_token = 'T'
    def test_positive_diagonal_check(self):
        connect_4.place_counter(self.test_board, 'T', 3, 0)
        connect_4.place_counter(self.test_board, 'T', 2, 1)
        connect_4.place_counter(self.test_board, 'T', 1, 2)
        connect_4.place_counter(self.test_board, 'T', 0, 3)
        self.assertTrue(connect_4.positive_diagonal_four_check(
            2, 1, self.test_board, self.generate_win_sequence()))




