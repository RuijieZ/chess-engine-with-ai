import chess

LOSS_SCORE = -1000
WINNING_SCORE = 1000
DRAW_SCORE = 0

WHITE_TURN = True
BLACK_TURN = False


pawn_eval_white = [
    0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,
    5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,
    1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0,
    0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5,
    0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0,  0.0,
    0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5,  0.5,
    0.5,  1.0, 1.0,  -2.0, -2.0,  1.0,  1.0,  0.5,
    0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0
]

pawn_eval_black = pawn_eval_white

knight_eval = [
    -5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0,
    -4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0,
    -3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0,
    -3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0,
    -3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0,
    -3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0,
    -4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0,
    -5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0
]

bishop_eval_white = [
    -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0,
    -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0,
    -1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0,
    -1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0,
    -1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0,
    -1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0,
    -1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0,
    -2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0
]

bishop_eval_black = bishop_eval_white

rook_eval_white = [
    0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,
    0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5,
   -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5,
   -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5,
   -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5,
   -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5,
   -0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5,
    0.0,   0.0, 0.0,  0.5,  0.5,  0.0,  0.0,  0.0
]

rook_eval_black = rook_eval_white

eval_queen = [
    -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0,
    -1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0,
    -1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0,
    -0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5,
     0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5,
    -1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0,
    -1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0,
    -2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0
]

king_eval_white = [
    -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0,
    -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0,
    -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0,
    -3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0,
    -2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0,
    -1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0,
     2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0,
     2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0
]

king_eval_black = king_eval_white

W_VALUES = {
    'N': (30, knight_eval),
    'B': (30, bishop_eval_white),
    'R': (50, rook_eval_white),
    'Q': (90, eval_queen),
    'P': (10, pawn_eval_white),
    'K': (100, king_eval_white),
}

B_VALUES = {
    'n': (30, knight_eval),
    'b': (30, bishop_eval_black),
    'r': (50, rook_eval_black),
    'q': (90, eval_queen),
    'p': (10, pawn_eval_black),
    'k': (100, king_eval_black),
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


    def evaluation(self, board, query_side):
        pieces = board.piece_map()
        if board.is_checkmate():
            if query_side == board.turn:        # the query side has lost
                return LOSS_SCORE
            else:                                # the query side has won
                return WINNING_SCORE

        if board.can_claim_draw() or board.is_stalemate():
            return 0

        b_value = 0
        w_value = 0
        for index, piece in pieces.items():
            symbol = piece.symbol()
            if symbol in W_VALUES:
                piece_value, pos_map = W_VALUES[symbol]
                w_value = w_value + piece_value + pos_map[index]
            elif symbol in B_VALUES:
                piece_value, pos_map = B_VALUES[symbol]
                b_value = b_value + piece_value + pos_map[index]

        return w_value - b_value if query_side == WHITE_TURN else b_value - w_value
