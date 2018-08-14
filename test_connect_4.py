import unittest
import connect_4



class SimpleTest(unittest.TestCase):
    def test_board_creation(self):
        n = 10
        board = connect_4.generate_board(n)
        self.assertEqual(len(board), n)
        self.assertEqual(len(board[0]), n)


    def test_horizontal_check(self):
        test_board = connect_4.generate_board(8)
        test_token = 'T'
        test_win_sequence = [test_token, test_token, test_token, test_token]
        for i in range(4):
            connect_4.place_counter(test_board, test_token, 0, i)
        print(test_win_sequence)
        print(test_board[0])
        self.assertTrue(
            connect_4.horizontal_four_check(test_win_sequence, test_board[0]))
            # todo: use this test to find the bug






