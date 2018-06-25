from flask import Flask, request, jsonify, current_app, send_from_directory
from flask_cors import CORS
from chess import Board

from ai.evaluation import WeightScore
from ai.min_max import min_f, max_f


WHITE_TURN = True
BLACK_TURN = False

app = Flask(__name__)
CORS(app)
w = WeightScore()

@app.route('/')
def index():
    return current_app.send_static_file('index.html')

@app.route('/next_move', methods=['POST'])
def next_move():
	fen = request.form['fen']
	board = Board(fen)
	move = max_f(board, 3, 3, 'b')[1]
	return str(move)


@app.route('/<path:path>', methods=['GET'])
def serve_file(path):
	return send_from_directory('static', path)


