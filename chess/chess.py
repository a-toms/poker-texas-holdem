

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


#V1 moving pawns that players can take. Being with UI




class Piece:

    def __init__(name, color, position):
        self.name = name
        self.color = color
        self.position = position


class Board(Piece):

    #def show_board(self):


    def



    pass




class PlayGame(Board):
    pass



if __name__ == '__main__':
    print(1)


