DEBUG = True

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
	# or a friendly piece is in the target position
	def is_valid_move(self, c_x, c_y, t_x, t_y):
		return (t_x, t_y) in self.all_valid_moves(c_x, c_y)

	# Again, this is a piece level valid moves
	# moves generate here may not be valid given the board situation
	# the board level code will filter out more invalid moves
	def all_valid_moves(self, c_x, c_y):
		pass

	# remove duplicates in the cors
	def remove_duplicates(self, list_of_cor):
		return list(set(list_of_cor))

	# filter out invalid cors
	# here, it only filter out duplicate cors
	# and OUT-OF-BOUNDARY cors.
	# it DOES NOT filter out moves based on the board position
	def filter_invalid_cors(self, list_of_cor, c_x, c_y):
		list_of_cor = self.remove_duplicates(list_of_cor)
		return list(filter(lambda c: 0 <= c[0] <= 7 and 0 <= c[1] <= 7 and c != (c_x, c_y), list_of_cor))

	# this function give a list cordinates that will be in the "path" the movement
	# the purpose of this function is to help the board chek whether there is a piece BLOCKING the move
	# if there is a piece in the returned coordinates, then the move is invalid(blocked)
	def cors_in_path(self, c_x, c_y, t_x, t_y):
		return []



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
		return self.filter_invalid_cors(cors, c_x, c_y)


class Rook(Piece):
	"""docstring for Rook"""
	def __init__(self, board, colour):
		super(Rook, self).__init__(board, colour)


	def all_valid_moves(self, c_x, c_y):
		x_change = [(c_x + k, c_y) for k in range(-7, 8)]
		y_change = [(c_x, c_y + k) for k in range(-7, 8)]
		cors = x_change + y_change
		return self.filter_invalid_cors(cors, c_x, c_y)

	def cors_in_path(self, c_x, c_y, t_x, t_y):
		if DEBUG:
			assert(self.is_valid_move(c_x, c_y, t_x, t_y))

		if c_x == t_x:
			return [(c_x, k) for k in range(min(c_y, t_y) + 1, max(c_y, t_y))]

		else:
			return [(k, c_y) for k in range(min(c_x, t_x) + 1, max(c_x, t_x))]



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
		return self.filter_invalid_cors(cors, c_x, c_y)

	def cors_in_path(self, c_x, c_y, t_x, t_y):
		if DEBUG:
			assert(self.is_valid_move(c_x, c_y, t_x, t_y))

		x_lst = range(min(c_x, t_x) + 1, max(c_x, t_x))
		y_lst = range(min(c_y, t_y) + 1, max(c_y, t_y))
		return list(zip(x_lst, y_lst))


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
		cors = c1 + c2 + c3 + c4 + c5 + c6
		return self.filter_invalid_cors(cors, c_x, c_y)


	def cors_in_path(self, c_x, c_y, t_x, t_y):
		if DEBUG:
			assert(self.is_valid_move(c_x, c_y, t_x, t_y))

		if c_x == t_x:
			return [(c_x, k) for k in range(min(c_y, t_y) + 1, max(c_y, t_y))]

		elif c_y == t_y:
			return [(k, c_y) for k in range(min(c_x, t_x) + 1, max(c_x, t_x))]

		x_lst = range(min(c_x, t_x) + 1, max(c_x, t_x))
		y_lst = range(min(c_y, t_y) + 1, max(c_y, t_y))
		return list(zip(x_lst, y_lst))


class Pawn(Piece):
	def __init__(self, board, colour):
		super(Pawn, self).__init__(board, colour)


	def all_valid_moves(self, c_x, c_y):
		c1 = [(c_x - 1, c_y + k) for k in range(-1,2)]
		c2 = [(c_x + 1, c_y + k) for k in range(-1,2)]
		c3 = [(c_x + k, c_y) for k in (-2, 2)]
		cors = c1 + c2 + c3
		return self.filter_invalid_cors(cors, c_x, c_y)


	def cors_in_path(self, c_x, c_y, t_x, t_y):
		if DEBUG:
			assert(self.is_valid_move(c_x, c_y, t_x, t_y))

		if c_x == t_x:
			return [(c_x, k) for k in range(min(c_y, t_y) + 1, max(c_y, t_y))]

		else:
			return [(k, c_y) for k in range(min(c_x, t_x) + 1, max(c_x, t_x))]


class King(Piece):
	"""docstring for King"""
	def __init__(self, board, colour):
		super(King, self).__init__(board, colour)


	def all_valid_moves(self, c_x, c_y):
		c1 = [(c_x - 1, c_y + k) for k in range(-1,2)]
		c2 = [(c_x + 1, c_y + k) for k in range(-1,2)]
		c3 = [(c_x, c_y + k) for k in (-1, 1)]
		cors = c1 + c2 + c3
		return self.filter_invalid_cors(cors, c_x, c_y)


if __name__ == "__main__":
	kn = Knight([],'WHITE')
	r = Rook([],'WHITE')
	q = Queen([],'WHITE')
	b = Bishop([],'WHITE')
	k = King([], 'WHITE')
	p = Pawn([], 'WHITE')

	# valid moves check
	assert(sorted(kn.all_valid_moves(1,2)) == [(0, 0), (0, 4), (2, 0), (2, 4), (3, 1), (3, 3)])
	assert(sorted(r.all_valid_moves(1,2)) == [(0, 2), (1, 0), (1, 1), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2)])
	assert(sorted(q.all_valid_moves(1,2)) == [(0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (2, 1), (2, 2), (2, 3), (3, 0), (3, 2), (3, 4), (4, 2), (4, 5), (5, 2), (5, 6), (6, 2), (6, 7), (7, 2)])
	assert(sorted(b.all_valid_moves(1,2)) == [(0, 1), (0, 3), (2, 1), (2, 3), (3, 0), (3, 4), (4, 5), (5, 6), (6, 7)])
	assert(sorted(k.all_valid_moves(1,2)) == [(0, 1), (0, 2), (0, 3), (1, 1), (1, 3), (2, 1), (2, 2), (2, 3)])
	assert(sorted(p.all_valid_moves(1,2)) == [(0, 1), (0, 2), (0, 3), (2, 1), (2, 2), (2, 3), (3, 2)])

	# cors in the path
	assert(r.cors_in_path(1, 4, 1, 1) == [(1, 2), (1, 3)])
	assert(b.cors_in_path(4, 6, 1, 3) == [(2, 4), (3, 5)])
	assert(q.cors_in_path(4, 6, 4, 3) == [(4, 4), (4, 5)])
	assert(p.cors_in_path(6, 6, 4, 6) == [(5,6)])




