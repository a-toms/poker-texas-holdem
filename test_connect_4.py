import unittest
import connect_4
import pprint
import logging
logging.basicConfig(level=logging.INFO)

class SimpleTest(unittest.TestCase):

    test_board = connect_4.generate_board(8)
    test_token = 'T'

    def return_win_sequence(self):
        return [self.test_token for i in range(4)]

    def test_board_creation(self):
        n = 10
        board = connect_4.generate_board(n)
        self.assertEqual(len(board), n)
        self.assertEqual(len(board[0]), n)

    def test_horizontal_check(self):
        test_win_sequence = self.return_win_sequence()
        for i in range(4):
            connect_4.place_counter(self.test_board, self.test_token, 0, i)
        self.assertTrue(
            connect_4.horizontal_four_check(
                self.test_board[0], test_win_sequence
            ))

    def test_negative_diagonal_check(self):
        for i in range(-4, 2):
            connect_4.place_counter(self.test_board, self.test_token, i, i)
        pprint.pprint(self.test_board)
        test_win_sequence = self.return_win_sequence()
        self.assertTrue(connect_4.negative_diagonal_four_check(
            4, 4, self.test_board, test_win_sequence))


# todo: write tests for the positive diagonal check and the vertical check







