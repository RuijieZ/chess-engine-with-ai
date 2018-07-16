import chess
from chess import Board

# from evaluation import evaluation
from evaluation_p import evaluation

moves_pickle = '/Users/ruijiezhang/Desktop/projects/chess/src/ai/moves_pickle'

BLACK_WIN_SCORE = -10000
WHITE_WIN_SCORE = 10000
DRAW_SCORE = 0

previous_result_dict = {}		# key: board_fen+min/max+depth, value: score
pv_table_dict = {}				# key: board_fen+min/max, value: move
move_cutoff_table = {}			# key: board_fen+min/max. value: move
move_ordering_cache = {}		# key: board_fen+min/max, value: move

file_map = {
	'a': 0,
	'b': 1,
	'c': 2,
	'd': 3,
	'e': 4,
	'f': 5,
	'g': 6,
	'h': 7,
}

rank_map = {
	'1': 0,
	'2': 1,
	'3': 2,
	'4': 3,
	'5': 4,
	'6': 5,
	'7': 6,
	'8': 7,
}

piece_type_map = {
	1: 1,
	2: 2,
	3: 2,
	4: 4,
	5: 5,
	6: 6,
	None: 1
}

# for i in range(1,9):
# 	for idx, j in enumerate('abcdefgh'):
# 		pos = (i-1) * 8 + (7-idx)
# 		print("\'" + j + str(i) + "\'" + ": " + str(pos) + ",")

def calculate_cap_move_score(board, move):
	uci = move.uci()
	from_sq, to_sq = chess.square(file_map[uci[0]], rank_map[uci[1]]) , chess.square(file_map[uci[2]], rank_map[uci[3]])
	source, victim = piece_type_map[board.piece_type_at(from_sq)], piece_type_map[board.piece_type_at(to_sq)]
	return source  - victim    # the smaller the better the cap move



def order_capture_moves(board, capture_moves):
	capture_moves.sort(key=lambda m: calculate_cap_move_score(board, m))
	return capture_moves


def move_ordering(board, is_max, key, s_move):
	# try to get basic moves
	try:
		moves = move_ordering_cache[key]
	except KeyError as e:
		capture_moves = order_capture_moves(board, list(board.generate_legal_captures()))
		# capture_moves = list(board.generate_legal_captures())
		all_moves = list(board.legal_moves)
		rest_moves = list(set(all_moves) - set(capture_moves))
		moves = capture_moves + rest_moves			# make capture moves in the front
		move_ordering_cache[key] = moves

	# idx = 0
	# length = len(moves)

	if s_move:
		for i, move in enumerate(moves):
			if move == s_move:
				moves[i], moves[0] = moves[0], moves[i]
				break


	# try:
	# 	cutoff_move = move_cutoff_table[key]
	# except:
	# 	cutoff_move = None

	# if cutoff_move:
	# 	for i, move in enumerate(moves):
	# 		if idx >= length:
	# 			break
	# 		if move == cutoff_move:
	# 			moves[idx], moves[i] = moves[i], moves[idx]
	# 			idx += 1
	# 			break
	return moves




def min_f(board, alpha, beta, depth):
	pos_id = board.board_fen()+'_min'
	s_move = None
	try:
		score, s_depth, s_move = previous_result_dict[pos_id]
		if s_depth >= depth:
			return score
	except KeyError:
		pass

	if board.is_checkmate():
		previous_result_dict[pos_id] = (WHITE_WIN_SCORE, depth, None)
		return WHITE_WIN_SCORE

	if board.is_stalemate():
		previous_result_dict[pos_id] = (DRAW_SCORE, depth, None)
		return DRAW_SCORE

	if depth == 0:
		# return evaluation(board.board_fen(), len(board.board_fen()))
		return evaluation(board)
	else:
		best_value = 10001
		best_move = None
		moves = move_ordering(board, False, pos_id, s_move)

		for move in moves:
			board.push(move)	# make that move to make a new board
			v = max_f(board, alpha, beta, depth-1)
			board.pop() 		# unmake that move

			if v < best_value:
				best_value = v
				best_move = move
			beta = min(beta, v)

			if alpha >= beta:		# the max player would not choose this path
				break


	previous_result_dict[pos_id] = (best_value, depth, best_move)
	# last_best_move_table[board.board_fen() + '_min'] = best_move
	return best_value


def max_f(board, alpha, beta, depth):
	pos_id = board.board_fen()+'_max'
	s_move = None
	try:
		score, s_depth, s_move = previous_result_dict[pos_id]
		if s_depth >= depth:
			return score
	except KeyError:
		pass

	if board.is_checkmate():
		previous_result_dict[pos_id] = (BLACK_WIN_SCORE, depth, None)
		return BLACK_WIN_SCORE

	if board.is_stalemate():
		previous_result_dict[pos_id] = (DRAW_SCORE, depth, None)
		return DRAW_SCORE

	if depth == 0:
		# return evaluation(board.board_fen(), len(board.board_fen()))
		return evaluation(board)
	else:
		best_value = -10001
		best_move = None
		moves = move_ordering(board, True, pos_id, s_move)

		for move in moves:
			board.push(move)	# make that move to create a new board
			v = min_f(board, alpha, beta, depth-1)
			board.pop()			# unmake that move

			if v > best_value:
				best_value = v
				best_move = move
			alpha = max(alpha, v)
			if beta <= alpha:
				break

	previous_result_dict[pos_id] = (best_value, depth, best_move)
	# last_best_move_table[board.board_fen() + '_max'] = best_move
	return best_value


# def iterative_deepening(board, alpha, beta, depth, is_max):
# 	legal_moves = move_ordering(board, is_max)
# 	for d in range(1, depth+1):
# 		if d == 1:
# 			r = min_f_root(board, alpha, beta, d, legal_moves)
# 		else:
# 			r = min_f_root(board, alpha, beta, d, r)
# 		r.sort(key=lambda x: x[0], reverse=is_max)
# 		# is_max = not is_max
# 		# print(r[0])



if __name__ == '__main__':
	b_str = 'rnb1kbnr/ppp2ppp/8/3P4/4p3/5P2/PPPQ2PP/RNB1KB1R b KQkq - 0 6'
	board = Board(b_str)
	# print(min_f(board, -10001, 10001, 4))
	# print(pv_table_dict[board.board_fen()+'_min'])

	for i in range(8):
		min_f(board, -10001, 10001, i)
	print(previous_result_dict[board.board_fen()+'_min'])

	# print(iterative_deepening(board, -10001, 10001, 5 ,False))
	# print(min_f(board, 2, 2))

