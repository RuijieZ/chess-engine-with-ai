from flask import Flask, request, jsonify, current_app, send_from_directory
from flask_cors import CORS
from chess import Board
import subprocess as s

# from ai.alpha_beta import min_f, max_f, min_f_root, max_f_root	# using the c version for performance
from ai.opening import opening_book_next_move

WHITE_TURN = True
BLACK_TURN = False


app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
	return current_app.send_static_file('index.html')

@app.route('/next_move/<count>', methods=['POST'])
def next_move(count):
	count = int(count) // 2
	fen = request.form['fen']
	if count <= 9:
		move = opening_book_next_move(fen, 'performance.bin')
		if move is not None:
			return move

	# use the c version one
	b = Board(fen)
	if b.turn:
		side = '0'	# white
	else:
		side = '1'
	result = s.run(['./ai/c_modules/main', fen ,side], stdout=s.PIPE)
	move = result.stdout.decode('utf-8').split("\n")[-2]

	# board = Board(fen)
	# move = min_f_root(board, -10001, 10001, 4)[1]		# black is the ai, so call min_f
	return move



@app.route('/<path:path>', methods=['GET'])
def serve_file(path):
	return send_from_directory('static', path)


if __name__ == "__main__":
    application.run(host='127.0.0.0', port='8080')
