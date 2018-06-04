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



    def get_all_threatened_cors(self, colour):
        piece_lst = self.get_piece_by_colour(colour)
        for c_x, c_y, piece in piece_lst:
            move_cors = piece.get_all_valid_moves(r_x, c)
            cors_in_path = piece.cors_in_path()



    # check move is valid in the given board situation
    # first, call the api on the piece level, check if move is valid on the piece level
    # then, check the board situation and determine whehter move is valid
    def is_valid_move(self, c_x, c_y, t_x, t_y):
        cur_piece = self.get_piece(c_x, c_y)

        for cord in [c_x, c_y, t_x, t_y]:
            if cord < 0 or cord > 7:
                return False

        if not piece.is_valid_move(c_x, c_y, t_x, t_y):
            return False

        # board situation check if move is good
        target_piece = self.get_piece(t_x, t_y)

        # cannot move into your own piece
        if target_piece is not None and target_piece.colour == cur_piece.colour:
            return False

        # cannot move if there is a piece block the piece for moving
        cors_in_path = cur_piece.cors_in_path(c_x, c_y, t_x, t_y)
        for x, y in cors_in_path:
            if self.get_piece(x, y) is not None:
                return False

        # specail rules for king
        # if cur_piece is King
        if cur_piece is King:
            opponent_colour = W if selfd.cur_turn == B else B
            attacked_cors = self.get_all_moves_cors(opponent_colour)
            if (t_x, t_y) in attacked_cors:
                return False



    def remove_piece(self, x, y):
        self._board[x][y] = None


    def drop_piece(self, x, y, Piece):
        self._board[x][y] = Piece



if __name__ == "__main__":
    b = Board()
    assert(b.board_is_valid())