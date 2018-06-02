from functools import reduce

class Board(object):
	"""Internal representation of a board
	"""
	def __init__(self):
		super(Board, self).__init__()
		self._board = [[None for i in range(8)] for _ in range(8)]


	def board_is_valid(self):
		return len(self._board) == 8 and reduce(lambda acc, x: acc and len(x) == 8, self._board, True)


	def get_piece(self, x, y):
		return self._board[x][y]


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
		if target_piece is not None and target_piece.colour = cur_piece.colour:
			return False

		cors_in_path = cur_piece.cors_in_path(c_x, c_y, t_x, t_y)



	def remove_piece(self, x, y):
		self._board[x][y] = None


	def drop_piece(self, x, y, Piece):
		self._board[x][y] = Piece



if __name__ == "__main__":
	b = Board()
	assert(b.board_is_valid())