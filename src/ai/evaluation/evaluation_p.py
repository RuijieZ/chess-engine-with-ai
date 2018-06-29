import chess

BLACK_WIN_SCORE = -100
WHITE_WIN_SCORE = 100
DRAW_SCORE = 0
WHITE_WINNING_SYMBOL = '1-0'
BLACK_WINNING_SYMBOL = '0-1'

WHITE_TURN = True
BLACK_TURN = False

# help switch the position matrix
# what it does it reverse the sign of the values
# by default, white has positive value and blakc has negative value
# then we control calling whether min_f of max_f for different sides
def colour_switch(matrix):
    return [x * -1 for x in matrix]


pawn_eval_white = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5,  10, 10,  -20, -20,  10,  10,  5,
    5, -5, -10,  0,  0, -10, -5,  5,
    0,  0,  0,  20,  20,  0,  0,  0,
    5,  5,  10,  25,  25,  10,  5,  5,
    10,  10,  20,  30,  30,  20,  10,  10,
    50,  50,  50,  50,  50,  50,  50,  50,
    0,  0,  0,  0,  0,  0,  0,  0
]

pawn_eval_black = colour_switch(pawn_eval_white[::-1])

knight_eval_white = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20,  0,  0,  0,  0, -20, -40,
    -30,  0,  10,  15,  15,  10,  0, -30,
    -30,  5,  15,  20,  20,  15,  5, -30,
    -30,  0,  15,  20,  20,  15,  0, -30,
    -30,  5,  10,  15,  15,  10,  5, -30,
    -40, -20,  0,  5,  5,  0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
]

knight_eval_black = colour_switch(knight_eval_white[::-1])

bishop_eval_white = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10,  5,  0,  0,  0,  0,  5, -10,
    -10,  10,  10,  10,  10,  10,  10, -10,
    -10,  0,  10,  10,  10,  10,  0, -10,
    -10,  5,  5,  10,  10,  5,  5, -10,
    -10,  0,  5,  10,  10,  5,  0, -10,
    -10,  0,  0,  0,  0,  0,  0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
]

bishop_eval_black = colour_switch(bishop_eval_white[::-1])

rook_eval_white = [
    0,  0,  0,  0,  0,  0,  0,  0,
   -5,  0,  0,  0,  0,  0,  0, -5,
   -5,  0,  0,  0,  0,  0,  0, -5,
   -5,  0,  0,  0,  0,  0,  0, -5,
   -5,  0,  0,  0,  0,  0,  0, -5,
   -5,  0,  0,  0,  0,  0,  0, -5,
    5,  10,  10,  10,  10,  10,  10,  5,
    0,   0, 0,  5,  5,  0,  0,  0
]

rook_eval_black = colour_switch(rook_eval_white[::-1])

eval_queen_white = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10,  0,  0,  0,  0,  0,  0, -10,
    -10,  0,  5,  5,  5,  5,  0, -10,
    -5,  0,  5,  5,  5,  5,  0, -5,
    -5,  0,  5,  5,  5,  5,  0, -5,
    -10,  0,  5,  5,  5,  5,  0, -10,
    -10,  0,  0,  0,  0,  0,  0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20
]

eval_queen_black = colour_switch(eval_queen_white)

king_eval_white = [
     20,  30,  10,  0,  0,  10,  30,  20,
     20,  20,  0,  0,  0,  0,  20,  20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30
]

king_eval_black = colour_switch(king_eval_white[::-1])

VALUES = {
    'N': (300, knight_eval_white),
    'B': (300, bishop_eval_white),
    'R': (500, rook_eval_white),
    'Q': (900, eval_queen_white),
    'P': (100, pawn_eval_white),
    'K': (1000, king_eval_white),
    'n': (-300, knight_eval_black),
    'b': (-300, bishop_eval_black),
    'r': (-500, rook_eval_black),
    'q': (-900, eval_queen_black),
    'p': (-100, pawn_eval_black),
    'k': (-1000, king_eval_black),
}

print('KING')
print(king_eval_black)
print('KNIGHT')
print(knight_eval_black)
print('BISHOP')
print(bishop_eval_black)
print('ROOK')
print(rook_eval_black)
print('QUEEN')
print(eval_queen_black)
print('PAWN')
print(pawn_eval_black)


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
            if board.result() == WHITE_WINNING_SYMBOL:      # the winner is WHITE
                return WHITE_WIN_SCORE
            else:                                			# the winner is Black
                return BLACK_WIN_SCORE

        if board.can_claim_draw() or board.is_stalemate():
            return 0

        value = 0
        for index, piece in pieces.items():
            symbol = piece.symbol()
            piece_value, pos_map = VALUES[symbol]
            value = value + piece_value + pos_map[index]

        return value
