import chess
from chess import Board
import copy

from ai.evaluation import WeightScore

w = WeightScore()

def min_f_root(board, alpha, beta, depth, table):
	cur_move_pair = (1001, None)
	for move in board.legal_moves:
		board.push(move)	# make that move to make a new board
		v = max_f(board, alpha, beta, depth-1, table)
		board.pop()
		if v < cur_move_pair[0]:
			cur_move_pair = (v, move)
		if v < beta:
			beta = v
		if alpha >= beta:		# the max player would not choose this path
			break
	return cur_move_pair

def max_f_root(board, alpha, beta, depth, table):
	cur_move_pair = (-1001, None)
	for move in board.legal_moves:
		board.push(move)	# make that move to make a new board
		v = min_f(board, alpha, beta, depth-1, table)
		board.pop()
		if v > cur_move_pair[0]:
			cur_move_pair = (v, move)
		if v > alpha:
			alpha = v
		if beta <= alpha:
			break
	return cur_move_pair

def min_f(board, alpha, beta, depth, table):
	# used stored search result to help speed up the search
	fen = board.fen()
	if fen in table:
		return table[fen]

	if board.is_game_over() or depth == 0:
		# store the result to help better the search next time
		table[fen] = w.evaluation(board)
		return table[fen]
	else:
		best_value = 1001
		for move in board.legal_moves:
			board.push(move)	# make that move to make a new board
			v = max_f(board, alpha, beta, depth-1, table)
			board.pop() 		# unmake that move

			if v < best_value:
				best_value = v
			if v < beta:
				beta = v
			if alpha >= beta:		# the max player would not choose this path
				break

	return best_value

# c_depth is the current depth
# depth is the search tree depth
def max_f(board, alpha, beta, depth, table):
	# used stored search result to help speed up the search
	fen = board.fen()
	if fen in table:
		return table[fen]

	if board.is_game_over() or depth == 0:
		# store the result to help better the search next time
		table[fen] = w.evaluation(board)
		return table[fen]
	else:
		best_value = -1001
		for move in board.legal_moves:
			board.push(move)	# make that move to create a new board
			v = min_f(board, alpha, beta, depth-1, table)
			board.pop()			# unmake that move

			if v > best_value:
				best_value = v
			if v > alpha:
				alpha = v
			if beta <= alpha:
				break

	return best_value


if __name__ == '__main__':
	board = Board('rnb1kbnr/ppp2ppp/8/3P4/4p3/5P2/PPPQ2PP/RNB1KB1R b KQkq - 0 6')
	print(max_f(board, 5, 5))
	print(min_f(board, 2, 2))

