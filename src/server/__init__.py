from flask import Flask, request, jsonify, current_app, send_from_directory
from flask_cors import CORS
from chess import Board

from ai.evaluation import WeightScore
from ai.alpha_beta import min_f, max_f
from ai.opening import open_pgn_list, find_opening_moves

WHITE_TURN = True
BLACK_TURN = False

pgn_list = open_pgn_list()
opening_moves = find_opening_moves(pgn_list)
print(opening_moves)
app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return current_app.send_static_file('index.html')

@app.route('/next_move/<count>', methods=['POST'])
def next_move(count):
	count = int(count) // 2
	if count <= 2:
		return str(opening_moves[count])
	fen = request.form['fen']
	board = Board(fen)
	move = min_f(board, -1001, 1001, 4, 4, {})[1]		# black is the ai, so call min_f
	return str(move)


@app.route('/<path:path>', methods=['GET'])
def serve_file(path):
	return send_from_directory('static', path)


