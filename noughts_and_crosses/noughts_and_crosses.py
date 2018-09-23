
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
            logging.info(f'win_check = {win_check}')
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

    def get_computer_one_move_win(self, board, computer_token):
        for position in range(8):
            duplicate_board = copy.deepcopy(board)
            duplicate_board = self.place_token_if_no_token_present(
                duplicate_board, position, computer_token)
            if WIN_CHECKER.run_win_checks(duplicate_board, computer_token):
                return position
        else:
            return False

    def get_human_one_move_win(self, board, human_token):
        for position in range(8):
            duplicate_board = copy.deepcopy(board)
            duplicate_board = self.place_token_if_no_token_present(
                duplicate_board, position, human_token)
            if WIN_CHECKER.run_win_checks(duplicate_board, human_token):
                return position
        else:
            return False







class GetHumanMove:
    pass



class MainGameLoop:
    pass


game_board = Board()
print(game_board.create_empty_board())
