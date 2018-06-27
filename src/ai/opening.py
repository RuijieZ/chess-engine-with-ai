import chess.pgn as pgn
import pickle
import random

pgn_file_path = '/Users/ruijiezhang/Desktop/projects/chess/src/openings/modern.pgn'
pgn_pickle_path = '/Users/ruijiezhang/Desktop/projects/chess/src/openings/modern_opening.p'


def save_pgn_in_list():
	result = []
	with open(pgn_file_path) as f:
		while 1:
			try:
				game = pgn.read_game(f)
				if game is None:
					break

				moves = list(game.main_line())
				result.append(moves)
			except Exception as e:
				continue
	pickle.dump(result, open(pgn_pickle_path, 'wb'))

def open_pgn_list():
	with open(pgn_pickle_path, 'rb') as f:
		pgn_list = pickle.load(f)
		return pgn_list


# find an opening moves
def find_opening_moves(pgn_list, side='b'):
	moves = random.choice(pgn_list)
	if side == 'b':
		return moves[1], moves[3], moves[5]
	elif side == 'w':
		return moves[0], moves[2], moves[4]


