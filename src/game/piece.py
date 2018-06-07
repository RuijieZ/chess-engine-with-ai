import board

DEBUG = True

W = 'WHITE'
B = 'BLACK'

L = 'LEFT'
R = 'RIGTH'
U = 'UP'
D = 'DOWN'
UL = 'UP_LEFT'
UR = 'UP_RIGHT'
DL = 'DOWN_LEFT'
DR = 'DOWN_RIGHT'

class PieceException(StandardError):
	pass

class Piece(object):
	"""Master class of different chess pieces
	"""
	def __init__(self, colour, board):
		super(Piece, self).__init__()
		self.colour = colour
		self.board = board
		self.has_moved = False

	# this function implements a piece level is valid move check
	# it checks whether the move is valid given the board situation
	def is_valid_move(self, c_x, c_y, t_x, t_y):
		return (t_x, t_y) in self.valid_moves(c_x, c_y)


	# this function returns the range of the given piece.
	# that is, given no other pieces in the board, what is this piece can reach
	# given the current position of the piece
	# moves generate here may not be valid given the board situation
	def range(self, c_x, c_y):
		pass


	# this function returns the cors that this piece is threatening,
	# including the cors of the friendly pieces
	# if a piece of another colour takes in this cors,
	# then this piece can take away that piece
	def threaten_cors(self, c_x, c_y):
		return self.range(c_x, c_y)


	# this function returns the cors that this piece can move to
	def valid_moves(self, c_x, c_y):
		t_cors = self.threaten_cors(c_x, c_y)
		return self.remove_cors_occupied_by_friendly_piece(t_cors)


	# remove duplicates in the cors
	def remove_duplicates(self, list_of_cor):
		return list(set(list_of_cor))


	# return true if the c is within bound
	def is_within_bound(self, c):
		return 0 <= c[0] <= 7 and 0 <= c[1] <= 7


	# filter out OUT-OF-BOUNDARY cors.
	def filter_out_of_bound_cors(self, list_of_cor, c_x, c_y):
		return [c for c in list_of_cor if self.is_within_bound(c) and c != (c_x, c_y)]


	# given a coordinate, determine whether on that place is a friendly piece
	def is_friendly_piece(self, c):
		piece = self.board.get_piece(c[0], c[1])
		return piece is not None and piece.colour == self.colour


	def _threaten_cors_to_valid_moves(self, list_of_cor):
		return [cor for cor in list_of_cor if not self.is_friendly_piece(cor)]


	# including the closest_piece itself
	def _cors_to_the_closest_piece(self, c_x, c_y, direction):
		cors = []
		if direction == L:
			for i in range(c_y-1, -1, -1):
				cors.append((c_x, i))
				if self.board.get_piece(c_x, i) is not None:
					break

		elif direction == R:
			for i in range(c_y+1, 8, 1):
				cors.append((c_x, i))
				if self.board.get_piece(c_x, i) is not None:
					break

		elif direction == U:
			for i in range(c_x-1, -1, -1):
				cors.append((i, c_y))
				if self.board.get_piece(i, c_y) is not None:
					break

		elif direction == D:
			for i in range(c_x+1, 8, 1):
				cors.append((i, c_y))
				if self.board.get_piece(i, c_y) is not None:
					break

		elif direction == UL:
			for i in range(1, 8, 1):
				c = (c_x - i, c_y - i)
				if not self.is_within_bound(c):
					break
				cors.append(c)
				if self.board.get_piece(c[0], c[1]) is not None:
					break

		elif direction == UR:
			for i in range(1, 8, 1):
				c = (c_x - i, c_y + i)
				if not self.is_within_bound(c):
					break
				cors.append(c)
				if self.board.get_piece(c[0], c[1]) is not None:
					break

		elif direction == DL:
			for i in range(1, 8, 1):
				c = (c_x + i, c_y - i)
				if not self.is_within_bound(c):
					break
				cors.append(c)
				if self.board.get_piece(c[0], c[1]) is not None:
					break

		elif direction == DR:
			for i in range(1, 8, 1):
				c = (c_x + i, c_y + i)
				if not self.is_within_bound(c):
					break
				cors.append(c)
				if self.board.get_piece(c[0], c[1]) is not None:
					break

		else:
			raise PieceException("Invalid direction passed to _cors_to_the_closest_piece!")

		return cors


class Knight(Piece):
	"""Knight"""
	def __init__(self, colour, board):
		super(Knight, self).__init__(colour, board)


	def range(self, c_x, c_y):
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
		return self.filter_out_of_bound_cors(cors, c_x, c_y)


class Rook(Piece):
	"""docstring for Rook"""
	def __init__(self, colour, board):
		super(Rook, self).__init__(colour, board)


	def range(self, c_x, c_y):
		x_change = [(c_x + k, c_y) for k in range(-7, 8)]
		y_change = [(c_x, c_y + k) for k in range(-7, 8)]
		cors = self.remove_duplicates(x_change + y_change)
		return self.filter_out_of_bound_cors(cors, c_x, c_y)


	def threaten_cors(self, c_x, c_y):
		left = self._cors_to_the_closest_piece(c_x, c_y, L)
		right = self._cors_to_the_closest_piece(c_x, c_y, R)
		up = self._cors_to_the_closest_piece(c_x, c_y, U)
		down = self._cors_to_the_closest_piece(c_x, c_y, D)
		return left + right + up + down


class Bishop(Piece):
	"""docstring for Bishop"""
	def __init__(self, colour, board):
		super(Bishop, self).__init__(colour, board)


	def range(self, c_x, c_y):
		c1 = [(c_x + k, c_y + k) for k in range(-7, 8)]
		c2 = [(c_x + k, c_y - k) for k in range(-7, 8)]
		c3 = [(c_x - k, c_y + k) for k in range(-7, 8)]
		c4 = [(c_x - k, c_y - k) for k in range(-7, 8)]
		cors = self.remove_duplicates(c1 + c2 + c3 + c4)
		return self.filter_out_of_bound_cors(cors, c_x, c_y)


	def threaten_cors(self, c_x, c_y):
		up_left = self._cors_to_the_closest_piece(c_x, c_y, UL)
		up_right = self._cors_to_the_closest_piece(c_x, c_y, UR)
		down_left = self._cors_to_the_closest_piece(c_x, c_y, DL)
		down_right = self._cors_to_the_closest_piece(c_x, c_y, DR)
		return up_left + up_right + down_left + down_right


class Queen(Piece):
	"""dtring for Queen"""
	def __init__(self, colour, board):
		super(Queen, self).__init__(colour, board)


	def range(self, c_x, c_y):
		c1 = [(c_x + k, c_y + k) for k in range(-7, 8)]
		c2 = [(c_x + k, c_y - k) for k in range(-7, 8)]
		c3 = [(c_x - k, c_y + k) for k in range(-7, 8)]
		c4 = [(c_x - k, c_y - k) for k in range(-7, 8)]
		c5 = [(c_x + k, c_y) for k in range(-7, 8)]
		c6 = [(c_x, c_y + k) for k in range(-7, 8)]
		cors = self.remove_duplicates(c1 + c2 + c3 + c4 + c5 + c6)
		return self.filter_out_of_bound_cors(cors, c_x, c_y)


	def threaten_cors(self, c_x, c_y):
		left = self._cors_to_the_closest_piece(c_x, c_y, L)
		right = self._cors_to_the_closest_piece(c_x, c_y, R)
		up = self._cors_to_the_closest_piece(c_x, c_y, U)
		down = self._cors_to_the_closest_piece(c_x, c_y, D)

		up_left = self._cors_to_the_closest_piece(c_x, c_y, UL)
		up_right = self._cors_to_the_closest_piece(c_x, c_y, UR)
		down_left = self._cors_to_the_closest_piece(c_x, c_y, DL)
		down_right = self._cors_to_the_closest_piece(c_x, c_y, DR)

		return left + right + up + down + up_left + up_right + down_left + down_right


class Pawn(Piece):
	def __init__(self, colour, board):
		super(Pawn, self).__init__(colour, board)


	def range(self, c_x, c_y):
		cur_direction = self.board.w_direction if self.colour == WHITE else self.board.b_direction
		cors = []
		if cur_direction is UP:
			cors = [(c_x - 1, c_y + k) for k in range(-1,2)]
			if not self.has_moved:
				cors.append((c_x - 2, c_y))

		else:
			cors = [(c_x + 1, c_y + k) for k in range(-1,2)]
			if not self.has_moved:
				cors.append((c_x - 2, c_y))

		return self.filter_out_of_bound_cors(cors, c_x, c_y)


	def threaten_cors(self, c_x, c_y):
		return [c for c in self.range(c_x, c_y) if c[1] != c_y]


	def valid_moves(self, c_x, c_y):
		t_cors = self.threaten_cors(c_x, c_y)
		t_cors = self.remove_cors_occupied_by_friendly_piece(t_cors)
		r_cors = self.range(c_x, c_y)
		push_one = [c for c in r_cors if c[0] == c_x and (c[1] == c_y - 1 or c[1] == c_y + 1) and (self.board.get_piece(c[0], c[1]) is None)]
		push_two = [c for c in r_cors if c[0] == c_x and (c[1] == c_y - 2 or c[1] == c_y + 2) and (self.board.get_piece(c[0], c[1]) is None)]

		result = [c for c in t_cors if self.baord.get_piece(c[0], c[1]).colour != self.colour]
		if len(push_one) == 0:	# the one push is blocked, so will two push be
			return result
		else:
			return result + push_one + push_two




class King(Piece):
	"""docstring for King"""
	def __init__(self, colour, board):
		super(King, self).__init__(colour, board)


	def range(self, c_x, c_y):
		c1 = [(c_x - 1, c_y + k) for k in range(-1,2)]
		c2 = [(c_x + 1, c_y + k) for k in range(-1,2)]
		c3 = [(c_x, c_y + k) for k in (-1, 1)]
		cors = c1 + c2 + c3
		return self.filter_out_of_bound_cors(cors, c_x, c_y)

	def valid_moves(self, c_x, c_y):
		opponent_colour = W if self.board.cur_turn == B else B  							# determine the oppo colour
		threaten_cors_by_opponent = self.board.get_all_threatened_cors(opponent_colour)  	# get all cors are threatened by oppo
		cors = self.remove_cors_occupied_by_friendly_piece(self.range(c_x, c_y))			# remove the cors that are ocupited by freindly piece
		return [c for c in cors if c not in threaten_cors_by_opponent]


if __name__ == "__main__":
	kn = Knight('WHITE', board.Board())
	r = Rook('WHITE', board.Board())
	q = Queen('WHITE', board.Board())
	b = Bishop('WHITE', board.Board())
	k = King('WHITE', board.Board())
	p = Pawn('WHITE', board.Board())

	# valid moves check
	assert(sorted(kn.range(1,2)) == [(0, 0), (0, 4), (2, 0), (2, 4), (3, 1), (3, 3)])
	assert(sorted(r.range(1,2)) == [(0, 2), (1, 0), (1, 1), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2)])
	assert(sorted(q.range(1,2)) == [(0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (2, 1), (2, 2), (2, 3), (3, 0), (3, 2), (3, 4), (4, 2), (4, 5), (5, 2), (5, 6), (6, 2), (6, 7), (7, 2)])
	assert(sorted(b.range(1,2)) == [(0, 1), (0, 3), (2, 1), (2, 3), (3, 0), (3, 4), (4, 5), (5, 6), (6, 7)])
	assert(sorted(k.range(1,2)) == [(0, 1), (0, 2), (0, 3), (1, 1), (1, 3), (2, 1), (2, 2), (2, 3)])
	assert(sorted(p.range(1,2)) == [(0, 1), (0, 2), (0, 3), (2, 1), (2, 2), (2, 3), (3, 2)])

	# closest piece tests
	assert(sorted(kn._cors_to_the_closest_piece(1,2, L)) == [(1,0), (1,1)])
	assert(sorted(kn._cors_to_the_closest_piece(1,2, R)) == [(1,3), (1,4), (1,5), (1,6), (1,7)])
	assert(sorted(kn._cors_to_the_closest_piece(1,2, U)) == [(0,2)])
	assert(sorted(kn._cors_to_the_closest_piece(1,2, D)) == [(2,2), (3,2), (4,2), (5,2), (6,2), (7,2)])
	assert(sorted(kn._cors_to_the_closest_piece(1,2, UL)) == [(0,1)])
	assert(sorted(kn._cors_to_the_closest_piece(1,2, UR)) == [(0,3)])
	assert(sorted(kn._cors_to_the_closest_piece(1,2, DL)) == [(2,1), (3,0)])
	assert(sorted(kn._cors_to_the_closest_piece(1,2, DR)) == [(2,3), (3,4), (4,5), (5,6), (6,7)])

