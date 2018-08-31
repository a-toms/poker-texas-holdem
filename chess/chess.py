

board = {
    '1': {'A': 'w rook', 'B': 'w knight', 'C': 'w bishop', 'D': 'w queen',
          'E': 'w king', 'F': 'w bishop', 'G': 'w knight', 'H': 'w rook'},
    '2': {'A': 'w pawn', 'B': 'w pawn', 'C': 'w pawn', 'D': 'w pawn',
          'E': 'w pawn', 'F': 'w pawn', 'G': 'w pawn', 'H': 'w pawn'},
    '3': {'A': '-', 'B': '-', 'C': '-', 'D': '-',
          'E': '-', 'F': '-', 'G': '-', 'H': '-'},
    '4': {'A': '-', 'B': '-', 'C': '-', 'D': '-',
          'E': '-', 'F': '-', 'G': '-', 'H': '-'},
    '5': {'A': '-', 'B': '-', 'C': '-', 'D': '-', 'E': '-', 'F': '-', 'G': '-',
          'H': '-'},
    '6': {'A': '-', 'B': '-', 'C': '-', 'D': '-', 'E': '-', 'F': '-', 'G': '-',
          'H': '-'},
    '7': {'A': 'b pawn', 'B': 'b pawn', 'C': 'b pawn', 'D': 'b pawn',
          'E': 'b pawn', 'F': 'b pawn', 'G': 'b pawn', 'H': 'b pawn'},
    '8': {'A': 'b rook', 'B': 'b knight', 'C': 'b bishop', 'D': 'b queen',
          'E': 'b king', 'F': 'b bishop', 'G': 'b knight', 'H': 'b rook'},
}



def main(): # todo: write the below functions
    game_status = 'incomplete'
    while game_status is 'incomplete':
        for player in players:
            show_board(board)
            move = get_player_move()
            is_move_valid = check_move(move)
            if is_move_valid is False:
                continue
            update_board(move)
            check_game_status(board)