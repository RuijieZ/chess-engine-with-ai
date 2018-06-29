import chess
from chess import Board

from ai.evaluation import WeightScore

w = WeightScore()

def move_ordering(board, is_max):
	moves = list(board.legal_moves)
	for idx, move in enumerate(moves):
		board.push(move)
		value = w.evaluation(board)
		board.pop()
		moves[idx] = (value, move)
	moves.sort(key=lambda x: x[0], reverse=is_max)
	return moves

def min_f_root(board, alpha, beta, depth):
	cur_move_pair = (1001, None)
	value_move_list = move_ordering(board, False)

	for value, move in value_move_list:
		board.push(move)	# make that move to make a new board
		v = max_f(board, value, alpha, beta, depth-1)
		board.pop()
		if v < cur_move_pair[0]:
			cur_move_pair = (v, move)
		if v < beta:
			beta = v
		if alpha >= beta:		# the max player would not choose this path
			break

	return cur_move_pair

def max_f_root(board, alpha, beta, depth):
	cur_move_pair = (-1001, None)
	value_move_list = move_ordering(board, True)

	for value, move in move_ordering(value_move_list):
		board.push(move)	# make that move to make a new board
		v = min_f(board, value, alpha, beta, depth-1)
		board.pop()
		if v > cur_move_pair[0]:
			cur_move_pair = (v, move)
		if v > alpha:
			alpha = v
		if beta <= alpha:
			break

	return cur_move_pair

def min_f(board, value, alpha, beta, depth):
	if board.is_game_over() or depth == 0:
		return value
	else:
		best_value = 1001
		value_move_list = move_ordering(board, False)

		for value, move in value_move_list:
			board.push(move)	# make that move to make a new board
			v = max_f(board, value, alpha, beta, depth-1)
			board.pop() 		# unmake that move

			best_value = min(best_value, v)
			beta = min(beta, v)
			if alpha >= beta:		# the max player would not choose this path
				break
	return best_value


def max_f(board, value, alpha, beta, depth):
	if board.is_game_over() or depth == 0:
		return value
	else:
		best_value = -1001
		value_move_list = move_ordering(board, True)

		for value, move in value_move_list:
			board.push(move)	# make that move to create a new board
			v = min_f(board, value, alpha, beta, depth-1)
			board.pop()			# unmake that move

			best_value = max(best_value, v)
			alpha = max(alpha, v)
			if beta <= alpha:
				break
	return best_value


if __name__ == '__main__':
	board = Board('rnb1kbnr/ppp2ppp/8/3P4/4p3/5P2/PPPQ2PP/RNB1KB1R b KQkq - 0 6')
	print(max_f(board, 5, 5))
	print(min_f(board, 2, 2))

