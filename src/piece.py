class Piece(object):
	"""Master class of different chess pieces
	"""
	def __init__(self, board, colour):
		super(Piece, self).__init__()
		self.board = board
		self.colour = colour
		self.has_moved = False

	# this function implements a piece level is valid move check
	# Note: a piece level valid move may not be a valid move on the board level
	# since some pieces can block u in the board
	def is_valid_move(self, c_x, c_y, t_x, t_y):
		return (t_x, t_y) in self.all_valid_moves()

	# Again, this is a piece level valid moves
	# moves generate here may not be valid given the board situation
	# the board level code will filter out more invalid moves
	def all_valid_moves(self, c_x, c_y):
		pass


	def filter_invalid_cors(self, list_of_cor):
		return list(filter(lambda x, y: 0 <= x <= 7 and 0 <= y <= 7, list_of_cor))


class Knight(Piece):
	"""Knight"""
	def __init__(self, board, colour):
		super(Knight, self).__init__(board, colour)

	def all_valid_moves(self, c_x, c_y):
		cors = [
			(c_x - 1, c_y + 2),
			(c_x - 1, c_y - 2),
			(c_x + 1, c_y + 2),
			(c_x + 1, c_y - 2),
			(c_x + 2, c_y + 1),
			(c_x + 2, c_y - 1),
			(c_x - 2, c_y + 1),
			(c_x - 2, c_y - 1),
		]
		return self.filter_invalid_cors(cors)


class Rook(Piece):
	"""docstring for Rook"""
	def __init__(self, board, colour):
		super(Rook, self).__init__(board, colour)
		self.arg = arg


	def all_valid_moves(self, c_x, c_y):
		x_change = [(c_x + k, c_y) for k in range(-7, 8)]
		y_change = [(c_x, c_y + k) for k in range(-7, 8)]
		cors = x_change.extend(y_change)
		return self.filter_invalid_cors(cors)


class Bishop(Piece):
	"""docstring for Bishop"""
	def __init__(self, board, colour):
		super(Bishop, self).__init__(board, colour)


	def all_valid_moves(self, c_x, c_y):
		c1 = [(c_x + k, c_y + k) for k in range(-7, 8)]
		c2 = [(c_x + k, c_y - k) for k in range(-7, 8)]
		c3 = [(c_x - k, c_y + k) for k in range(-7, 8)]
		c4 = [(c_x - k, c_y - k) for k in range(-7, 8)]
		cors = c1 + c2 + c3 + c4
		return self.filter_invalid_cors(cors)


class Queen(Piece):
	"""dtring for Queen"""
	def __init__(self, board, colour):
		super(Queen, self).__init__(board, colour)


	def all_valid_moves(self, c_x, c_y):
		c1 = [(c_x + k, c_y + k) for k in range(-7, 8)]
		c2 = [(c_x + k, c_y - k) for k in range(-7, 8)]
		c3 = [(c_x - k, c_y + k) for k in range(-7, 8)]
		c4 = [(c_x - k, c_y - k) for k in range(-7, 8)]
		c5 = [(c_x + k, c_y) for k in range(-7, 8)]
		c6 = [(c_x, c_y + k) for k in range(-7, 8)]
		return self.filter_invalid_cors(cors)

class King(Piece):
	"""docstring for King"""
	def __init__(self, board, colour):
		super(King, self).__init__(board, colour)


	def all_valid_moves(self, c_x, c_y):
		c1 = [(c_x - 1, c_y + k) for k in range(-1,2)]
		c2 = [(c_x + 1, c_y + k) for k in range(-1,2)]
		c3 = [(c_x, c_y + k) for k in (-1, 1)]
		return self.filter_invalid_cors(cors)




