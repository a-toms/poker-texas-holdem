#! python3
# connect_4.py

import logging
logging.basicConfig(
    filename='connect_4.log', format='%(asctime)s %(message)s',
    level=logging.WARNING, filemode='w'
)


def is_shorter_sequence_in_longer_sequence(shorter_sequence, longer_sequence):
    """Check if shorter sequence is in a longer sequence."""
    n = len(shorter_sequence)
    return shorter_sequence in (
        longer_sequence[i:i+n] for i in range(len(longer_sequence) + 1 - n))


def generate_board(size):
    """Generate board."""
    board = []
    for i in range(size):
        board.append([])
    return board


def show_board(board):
    """Show board to user."""
    for i in range(len(board)):
        for j in range(len(board)):
            try:
                print("|" + board[j][len(board) - 1 - i], end='| ')
            except IndexError:
                print("|" + "*", end='| ')
        print()


def choose_position_to_place_counter(player, board):
    """Get player integer input that fits on the board."""
    input_error_message = "The position is out of the games's bounds. "
    while True:
        column = input(
            f"{player}, please state the column to place your token\n")
        if column.isdigit() is False:
            print(input_error_message)
        elif int(column) > (len(board) - 1):
            print(input_error_message)
        else:
            return int(column)


def place_counter(board, player_token, column):
    board[column].append(player_token)


def check_for_winner(x, board, player):
    """Run the checks to determine if a player has won the game."""
    if vertical_check(board[x], player['win_seq']) is True:
        logging.info('vertical win')
        return player
    if horizontal_check(board, player['win_seq']) is True:
        logging.info('horizontal win')
        return player
    if negative_diagonal_check(board, player['win_seq']) is True:
        logging.info('negative diagonal win')
        return player
    if positive_diagonal_check(board, player['win_seq']) is True:
        logging.info('positive diagonal win')
        return player
    else:
        return False


def vertical_check(longer_sequence, win_sequence):
    """Check vertical board values for four consecutive player tokens."""
    logging.info(f'{longer_sequence} entered vertical four check')
    return is_shorter_sequence_in_longer_sequence(
        win_sequence, longer_sequence)


def horizontal_check(board, win_sequence):
    """Check horizontal board values for four consecutive player tokens."""
    for i in range(len(board)):
        horizontal_values = []
        for j in range(len(board)):
            try:
                horizontal_values.append(board[j][i])
            except IndexError:
                pass
        logging.info(f'horizontal row values = {horizontal_values}')
        if is_shorter_sequence_in_longer_sequence(
                win_sequence, horizontal_values):
            return True


def positive_diagonal_check(board, win_sequence):
    """Check positive diagonal board values for four consecutive player tokens.
    Each start position shows the x and y board starting position of the
    diagonal line to check for consecutive player tokens."""
    start_positions = [
        [0, 4], [0, 3], [0, 2], [0, 1], [0, 0], [1, 0], [2, 0], [3, 0], [4, 0]
    ]
    for start_position in start_positions:
        positive_diagonal = []
        for i in range(len(board)):
            board_x, board_y = start_position
            try:
                positive_diagonal.append(board[board_x + i][board_y + i])
                logging.info(f'Positive diagonal = {positive_diagonal}. ' +
                             f'The token {board[board_x + i][board_y + i]} ' +
                             f'is from from x = {board_x + i} y = {board_y + i}'
                             )
            except IndexError:
                positive_diagonal.append('Blank')
            if is_shorter_sequence_in_longer_sequence(
                    win_sequence, positive_diagonal) is True:
                return True


def negative_diagonal_check(board, win_sequence):
    """Check negative diagonal board values for four consecutive player tokens.
    Each start position shows the x and y board starting position of the
    diagonal line to check for consecutive player tokens."""
    start_positions = [
        [0, 3], [0, 4], [0, 5], [0, 6], [0, 7], [1, 7], [2, 7], [3, 7], [4, 7]
    ]
    for start_position in start_positions:
        negative_diagonal = []
        for i in range(len(board)):
            board_x, board_y = start_position
            try:
                negative_diagonal.append(board[board_x + i][board_y - i])
                logging.info(f'Negative diagonal = {negative_diagonal}. ' +
                             f'The token {board[board_x + i][board_y - i]} ' +
                             f'is from from x = {board_x + i} y = {board_y - i}'
                             )
            except IndexError:
                negative_diagonal.append('-')
            if is_shorter_sequence_in_longer_sequence(
                    win_sequence, negative_diagonal) is True:
                return True


def game_loop(players, board):
    """Run the game until a player wins the game."""
    winning_player = False
    while winning_player is False:
        for player in players:
            x = choose_position_to_place_counter(player['name'], board)
            place_counter(board, player['token'], x)
            show_board(board)
            winning_player = check_for_winner(x, board, player)
            if winning_player is not False:
                logging.info(f'winning player = {winning_player}')
                return winning_player


def engine():
    board = generate_board(8)
    show_board(board)
    p1_token = 'X'
    p1_win_seq = [p1_token] * 4
    p2_token = 'O'
    p2_win_seq = [p2_token] * 4
    players = [
        {'name': 'Player 1', 'token': p1_token, 'win_seq': p1_win_seq},
        {'name': 'Player 2', 'token': p2_token, 'win_seq': p2_win_seq}
    ]
    winning_player = game_loop(players, board)
    print()
    print(f"{winning_player['name']} won the game!")


engine()
