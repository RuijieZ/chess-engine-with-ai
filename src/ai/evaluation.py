import chess

LOSS_SCORE = -1000
WINNING_SCORE = 1000
DRAW_SCORE = 0

WHITE_TURN = True
BLACK_TURN = False

W_VALUES = {
	'N': 3,
	'B': 3,
	'R': 5,
	'Q': 9,
	'P': 1,
}

B_VALUES = {
	'n': 3,
	'b': 3,
	'r': 5,
	'q': 9,
	'p': 1,
}



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
		if board.is_checkmate() or board.is_stalemate():
			if query_side == board.turn:		# the query side has lost
				return LOSS_SCORE
			else:								# the query side has won
				return WINNING_SCORE

		if board.can_claim_draw():
			return 0

		b_value = 0
		w_value = 0
		for index, piece in pieces.items():
			symbol = piece.symbol()
			if symbol in W_VALUES:
				w_value += W_VALUES[symbol]
			elif symbol in B_VALUES:
				b_value += B_VALUES[symbol]

		return w_value - b_value if query_side == WHITE_TURN else b_value - w_value
