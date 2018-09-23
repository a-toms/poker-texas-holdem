
# Continue building class structure
import copy
import logging
logging.basicConfig(level=logging.DEBUG)

class Board:
    def create_empty_board(self):
        board = ['' for i in range(9)]
        return board


class IsGameComplete:
    def horizontal_win(self, board, game_token):
        for i in range(0, 9, 3):
            if list(game_token * 3) == board[i:i+3]:
                return True

    def vertical_win(self, board, game_token):
        for i in range(3):
            if game_token * 3 == (board[i] + board[i+3] + board[i+6]):
                return True

    def positive_diagonal_win(self, board, game_token):
        if game_token * 3 == (board[6] + board[4] + board[2]):
            return True

    def negative_diagonal_win(self, board, game_token):
        if game_token * 3 == (board[0] + board[4] + board[8]):
            return True

    def run_win_checks(self, board, game_token):
        win_checks = (
            self.horizontal_win, self.vertical_win,
            self.positive_diagonal_win, self.negative_diagonal_win
        )
        for win_check in win_checks:
            if win_check(board, game_token) is True:
                return True
        else:
            return False


WIN_CHECKER = IsGameComplete()


class GetComputerMove:
    def place_token_if_no_token_present(self, board, position, token):
        if board[position] == '-':
            board[position] = token
        return board

    def look_for_computer_one_move_win(self, board, computer_token):
        """TODO: Refactor the repetition in these moves,
        e.g., 'for position in range(9) is repeated."""
        for position in range(9):
            duplicate_board = copy.deepcopy(board)
            duplicate_board = self.place_token_if_no_token_present(
                duplicate_board, position, computer_token)
            if WIN_CHECKER.run_win_checks(duplicate_board, computer_token):
                return position
        else:
            return False

    def look_for_move_to_block_human_win(self, board, human_token):
        for position in range(9):
            duplicate_board = copy.deepcopy(board)
            duplicate_board = self.place_token_if_no_token_present(
                duplicate_board, position, human_token)
            if WIN_CHECKER.run_win_checks(duplicate_board, human_token):
                return position
        else:
            return False

    def look_for_computer_fork_move(self, board, computer_token):
        """Test if a move would give two ways of winning."""
        """Todo: refactoring is necessary. 
        THis is becoming too complex. Refactoring is necessary
        Restructure game in accordance with the guide in https://mblogscode.wordpress.com/2016/06/03/python-naughts-crossestic-tac-toe-coding-unbeatable-ai/"""
        for i in range(9):
            duplicate_board = copy.deepcopy(board)
            if duplicate_board[i] == '-':
                duplicate_board[i] = computer_token
            winning_moves = 0
            for j in range(9):
                duplicate_board2 = copy.deepcopy(duplicate_board)
                if duplicate_board2[j] == '-':
                    duplicate_board2[j] = computer_token
                if WIN_CHECKER.run_win_checks(duplicate_board2, computer_token):
                    winning_moves += 1
                print(duplicate_board2)
            return winning_moves >= 2





class GetHumanMove:
    pass



class MainGameLoop:
    pass


game_board = Board()
print(game_board.create_empty_board())
