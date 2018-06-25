import chess
from chess import Board
import copy

from ai.evaluation import WeightScore


w = WeightScore()

def create_new_board_with_move(board, move):
	board_cpy = copy.deepcopy(board)		# make a copy of the orginal board
	board_cpy.push(move)					# make that move
	return board_cpy


def min_f(board, c_depth, depth, query_side, top_level_move=None):
	if board.is_game_over() or c_depth == 0:
		return w.evaluation(board, query_side), top_level_move
	elif c_depth == depth:	# first call
		boards = [(create_new_board_with_move(board, move), move) for move in board.legal_moves]
		result = [max_f(b, c_depth-1, depth, query_side, m) for b, m in boards]
	else:					# other lvel of recursions
		boards = [(create_new_board_with_move(board, move)) for move in board.legal_moves]
		result = [max_f(b, c_depth-1, depth, query_side, top_level_move) for b in boards]

	return min(result, key=lambda x: x[0])

# c_depth is the current depth
# depth is the search tree depth
def max_f(board, c_depth, depth, query_side, top_level_move=None):
	if board.is_game_over() or c_depth == 0:
		return w.evaluation(board, query_side), top_level_move
	elif c_depth == depth:	# first call
		boards = [(create_new_board_with_move(board, move), move) for move in board.legal_moves]
		result = [min_f(b, c_depth-1, depth, query_side, m) for b, m in boards]
	else:					# other lvel of recursions
		boards = [(create_new_board_with_move(board, move)) for move in board.legal_moves]
		result = [min_f(b, c_depth-1, depth, query_side, top_level_move) for b in boards]

	return max(result, key=lambda x: x[0])


if __name__ == '__main__':
	board = Board('rnb1kbnr/ppp2ppp/8/3P4/4p3/5P2/PPPQ2PP/RNB1KB1R b KQkq - 0 6')
	print(max_f(board, 5, 5, 'w'))
	print(min_f(board, 2, 2, 'w'))

