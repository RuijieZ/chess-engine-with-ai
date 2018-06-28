import chess
from chess import Board
import copy

from ai.evaluation import WeightScore

w = WeightScore()

def min_f(board, alpha, beta, c_depth, depth, table, top_level_move=None):
	# used stored search result to help speed up the search
	fen = board.fen()
	if fen in table:
		return table[fen]

	if board.is_game_over() or c_depth == 0:
		# store the result to help better the search next time
		table[fen] = (w.evaluation(board), top_level_move)
		return table[fen]
	else:
		cur_move_pair = (1001, None)
		for move in board.legal_moves:
			board.push(move)	# make that move to make a new board
			if c_depth != depth:
				m = top_level_move
			else:
				m = move
			v = max_f(board, alpha, beta, c_depth-1, depth, table, m)
			board.pop() 		# unmake that move

			if v[0] < cur_move_pair[0]:
				cur_move_pair = v
			if v[0] < beta:
				beta = v[0]
			if alpha >= beta:
				break

	return cur_move_pair

# c_depth is the current depth
# depth is the search tree depth
def max_f(board, alpha, beta, c_depth, depth, table, top_level_move=None):
	# used stored search result to help speed up the search
	fen = board.fen()
	if fen in table:
		return table[fen]

	if board.is_game_over() or c_depth == 0:
		# store the result to help better the search next time
		table[fen] = (w.evaluation(board), top_level_move)
		return table[fen]
	else:
		cur_move_pair = (-1001, None)
		for move in board.legal_moves:
			board.push(move)	# make that move to create a new board
			if c_depth != depth:
				m = top_level_move
			else:
				m = move
			v = min_f(board, alpha, beta, c_depth-1, depth, table, m)
			board.pop()			# unmake that move

			if v[0] > cur_move_pair[0]:
				cur_move_pair = v
			if v[0] > alpha:
				alpha = v[0]
			if beta <= alpha:
				break

	return cur_move_pair


if __name__ == '__main__':
	board = Board('rnb1kbnr/ppp2ppp/8/3P4/4p3/5P2/PPPQ2PP/RNB1KB1R b KQkq - 0 6')
	print(max_f(board, 5, 5))
	print(min_f(board, 2, 2))

