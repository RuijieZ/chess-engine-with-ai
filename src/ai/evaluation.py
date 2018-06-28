import chess

BLACK_WIN_SCORE = -1000
WHITE_WIN_SCORE = 1000
DRAW_SCORE = 0

WHITE_TURN = True
BLACK_TURN = False

# help switch the position matrix
# what it does it reverse the sign of the values
# by default, white has positive value and blakc has negative value
# then we control calling whether min_f of max_f for different sides
def colour_switch(matrix):
    return [x * -1.0 for x in matrix]


pawn_eval_white = [
    0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,
    0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5,
    0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5,
    0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0,
    0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5,
    1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0,
    5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,
    0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0
]

pawn_eval_black = colour_switch(pawn_eval_white[::-1])

knight_eval_white = [
    -5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0,
    -4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0,
    -3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0,
    -3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0,
    -3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0,
    -3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0,
    -4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0,
    -5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0
]

knight_eval_black = colour_switch(knight_eval_white[::-1])

bishop_eval_white = [
    -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0,
    -1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0,
    -1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0,
    -1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0,
    -1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0,
    -1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0,
    -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0,
    -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0
]

bishop_eval_black = colour_switch(bishop_eval_white[::-1])

rook_eval_white = [
    0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,
   -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5,
   -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5,
   -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5,
   -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5,
   -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5,
    0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5,
    0.0,   0.0, 0.0,  0.5,  0.5,  0.0,  0.0,  0.0
]

rook_eval_black = colour_switch(rook_eval_white[::-1])

eval_queen_white = [
    -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0,
    -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0,
    -1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0,
    -0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5,
     0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5,
    -1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0,
    -1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0,
    -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0
]

eval_queen_black = colour_switch(eval_queen_white)

king_eval_white = [
     2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0,
     2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0,
    -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0,
    -2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0,
    -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0,
    -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0,
    -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0,
    -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0
]

king_eval_black = colour_switch(king_eval_white[::-1])

VALUES = {
    'N': (30, knight_eval_white),
    'B': (30, bishop_eval_white),
    'R': (50, rook_eval_white),
    'Q': (90, eval_queen_white),
    'P': (10, pawn_eval_white),
    'K': (100, king_eval_white),
    'n': (-30, knight_eval_black),
    'b': (-30, bishop_eval_black),
    'r': (-50, rook_eval_black),
    'q': (-90, eval_queen_black),
    'p': (-10, pawn_eval_black),
    'k': (-100, king_eval_black),
}

print(king_eval_black)


class Evaluation(object):
    """Evaluation object.
    """
    def __init__(self):
        super(Evaluation, self).__init__()

    """ given the fen_str, return an integer that indicate the
    evaluation of the situation.
    """
    def evaluate(self, fen_str):
        pass


class WeightScore(Evaluation):
    """docstring for WeightScore"""
    def __init__(self):
        super(WeightScore, self).__init__()


    def evaluation(self, board):
        pieces = board.piece_map()
        if board.is_checkmate():
            if board.turn == WHITE_TURN:         # the winner is Black
                return BLACK_WIN_SCORE
            else:                                # the winner is White
                return WHITE_WIN_SCORE

        if board.can_claim_draw() or board.is_stalemate():
            return 0

        value = 0
        for index, piece in pieces.items():
            symbol = piece.symbol()
            piece_value, pos_map = VALUES[symbol]
            value = value + piece_value + pos_map[index]

        return value
