import chess
from chess import Board
import copy

from ai.evaluation import WeightScore

w = WeightScore()

def create_new_board_with_move(board, move):
	board_cpy = board.copy()		# make a copy of the orginal board
	board_cpy.push(move)					# make that move
	return board_cpy


def min_f(board, alpha, beta, c_depth, depth, query_side, top_level_move=None):
	if board.is_game_over() or c_depth == 0:
		return w.evaluation(board, query_side), top_level_move
	else:
		boards = [(create_new_board_with_move(board, move), move) for move in board.legal_moves]
		cur_move_pair = (1001, None)
		for b, m in boards:
			if c_depth != depth:
				m = top_level_move

			v = max_f(b, alpha, beta, c_depth-1, depth, query_side, m)

			if v[0] < cur_move_pair[0]:
				cur_move_pair = v
			if v[0] < beta:
				beta = v[0]
			if alpha >= beta:
				break

	return cur_move_pair

# c_depth is the current depth
# depth is the search tree depth
def max_f(board, alpha, beta, c_depth, depth, query_side, top_level_move=None):
	if board.is_game_over() or c_depth == 0:
		return w.evaluation(board, query_side), top_level_move
	else:
		boards = [(create_new_board_with_move(board, move), move) for move in board.legal_moves]
		cur_move_pair = (-1001, None)
		for b, m in boards:
			if c_depth != depth:
				m = top_level_move

			v = min_f(b, alpha, beta, c_depth-1, depth, query_side, m)

			if v[0] > cur_move_pair[0]:
				cur_move_pair = v
			if v[0] > alpha:
				alpha = v[0]
			if beta <= alpha:
				break

	return cur_move_pair


if __name__ == '__main__':
	board = Board('rnb1kbnr/ppp2ppp/8/3P4/4p3/5P2/PPPQ2PP/RNB1KB1R b KQkq - 0 6')
	print(max_f(board, 5, 5, 'w'))
	print(min_f(board, 2, 2, 'w'))

