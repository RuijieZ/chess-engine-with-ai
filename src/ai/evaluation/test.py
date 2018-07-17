#!/usr/bin/env python3
from chess import Board
import evaluation as e
from evaluation_p import WeightScore

w = WeightScore()
b = Board()
# test c_module correctness
'''
test_step = 50

for i in range(test_step):
	for move in b.legal_moves:
		b.push(move)
		print(b.board_fen())
		print(b.fen())
		print("python", w.evaluation(b))
		print("c module", e.evaluation(b.result(), b.board_fen(), len(b.board_fen())))
		assert(w.evaluation(b) == e.evaluation(b.result(), b.board_fen(), len(b.board_fen())))
		b.pop()

	b.push(move)

'''
'''
bug_fen = 'rnb1kbnr/2qppppp/8/ppp5/PPPP4/8/4PPPP/RNBQKBNR w KQkq - 1 5'
bug_board_fen = 'rnb1kbnr/2qppppp/8/ppp5/PPPP4/8/4PPPP/RNBQKBNR'

b = Board(bug_fen)
print(w.evaluation(b))
print(e.evaluation(b.result(), b.board_fen(), len(b.board_fen())))
'''

# test for speed
import time

loop_count = 10000
t0 = time.time()
for i in range(loop_count):
	w.evaluation(b)
t1 = time.time()
print('python code time: {}'.format(t1-t0))

t0 = time.time()
for i in range(loop_count):
	x = b.result()
	y = b.board_fen()
	z = len(y)
	e.evaluation(x, y, z)
t1 = time.time()
print('c code time: {}'.format(t1-t0))

t0 = time.time()
x = list(b.legal_moves)[0]
for i in range(loop_count):
	for j in range(30):
		b.push(x)
		b.pop()
t1 = time.time()
print('chess board legal_moves code time: {}'.format(t1-t0))





