import chess
from chess import Board

from evaluation import evaluation

moves_pickle = '/Users/ruijiezhang/Desktop/projects/chess/src/ai/moves_pickle'

def move_ordering(board, is_max):
	moves = list(board.legal_moves)
	for idx, move in enumerate(moves):
		board.push(move)
		board_fen = board.board_fen()
		result = board.result()
		value = evaluation(result, board_fen, len(board_fen))
		board.pop()
		moves[idx] = (value, move)
	moves.sort(key=lambda x: x[0], reverse=is_max)
	return moves

def min_f_root(board, alpha, beta, depth, moves):
	result = []
	for value, move in moves:
		board.push(move)	# make that move to make a new board
		v = max_f(board, alpha, beta, depth-1, value)
		result.append((v, move))
		board.pop()
		if v < beta:
			beta = v

	return result

def max_f_root(board, alpha, beta, depth, moves):
	result = []
	for value, move in moves:
		board.push(move)	# make that move to make a new board
		v = min_f(board, alpha, beta, depth-1, value)
		result.append((v, move))
		board.pop()
		if v > alpha:
			alpha = v

	return result

def min_f(board, alpha, beta, depth, value):
	if board.is_game_over() or depth == 0:
		return value
	else:
		best_value = 10001
		moves = move_ordering(board, False)
		for value, move in moves:
			board.push(move)	# make that move to make a new board
			v = max_f(board, alpha, beta, depth-1, value)
			board.pop() 		# unmake that move

			best_value = min(best_value, v)
			beta = min(beta, v)
			if alpha >= beta:		# the max player would not choose this path
				break
	return best_value


def max_f(board, alpha, beta, depth, value):
	if board.is_game_over() or depth == 0:
		return value
	else:
		best_value = -10001
		moves = move_ordering(board, True)
		for value, move in moves:
			board.push(move)	# make that move to create a new board
			v = min_f(board, alpha, beta, depth-1, value)
			board.pop()			# unmake that move
			best_value = max(best_value, v)
			alpha = max(alpha, v)
			if beta <= alpha:
				break
	return best_value


def iterative_deepening(board, alpha, beta, depth, is_max):
	legal_moves = move_ordering(board, is_max)
	for d in range(1, depth+1):
		if d == 1:
			r = min_f_root(board, alpha, beta, d, legal_moves)
		else:
			r = min_f_root(board, alpha, beta, d, r)
		r.sort(key=lambda x: x[0], reverse=is_max)
		# is_max = not is_max
		# print(r[0])



if __name__ == '__main__':
	board = Board('rnb1kbnr/ppp2ppp/8/3P4/4p3/5P2/PPPQ2PP/RNB1KB1R b KQkq - 0 6')
	legal_moves = move_ordering(board, False)
	print(min_f_root(board, -10001, 10001, 5, legal_moves))
	# print(iterative_deepening(board, -10001, 10001, 5 ,False))
	# print(min_f(board, 2, 2))

