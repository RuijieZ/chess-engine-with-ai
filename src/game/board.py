from functools import reduce
from piece import King, Queen, Pawn, Knight, Rook, Bishop

W = 'WHITE'
B = 'BLACK'

U = 'UP'
D = 'Down'

class Board(object):
    """Internal representation of a board
    """
    def __init__(self):
        super(Board, self).__init__()
        self._board = [[None for i in range(8)] for _ in range(8)]
        self.cur_turn = W
        self.w_direction = U
        self.b_dicretion = D


    # check if the board shape is not damaged by some bug in the code
    def board_is_valid(self):
        return len(self._board) == 8 and reduce(lambda acc, x: acc and len(x) == 8, self._board, True)


    # get a piece by coordinate
    def get_piece(self, x, y):
        return self._board[x][y]


    # get all pieces and coordinates of a ceratin colour
    def get_pieces_by_colour(self, colour):
        piece_lst = []
        for row_num, r_lst in enumerate(self._board):
            for col_num, piece in enumerate(r_lst):
                if piece.colour == colour:
                    piece_lst.append((row_num, col_num, piece))

        return piece_lst


    # get all pieces and threatened cors of a certian colour
    def get_all_threatened_cors(self, colour):
        piece_lst = self.get_piece_by_colour(colour)
        result = set()
        for c_x, c_y, piece in piece_lst:
            threaten_cors = piece.threaten_cors(c_x, c_y)
            result.update(threaten_cors)

        return list(result)


    # check move is valid in the given board situation
    # first, call the api on the piece level, check if move is valid on the piece level
    # then, check the board situation and determine whehter move is valid
    def is_valid_move(self, c_x, c_y, t_x, t_y):
        return (t_x, t_y) in self.get_piece(c_x, c_y).valid_moves()


    def remove_piece(self, x, y):
        self._board[x][y] = None


    def drop_piece(self, x, y, Piece):
        self._board[x][y] = Piece



if __name__ == "__main__":
    b = Board()
    assert(b.board_is_valid())