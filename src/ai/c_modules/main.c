#include <stdio.h>
#include <stdlib.h>     /* qsort */
#include "defs.h"

char *AlphaBetaRoot(S_BOARD *pos, int alpha, int beta, int depth, int isMax, S_MOVELIST* moves) {
	int legalMovesCount = 0;
	int move;
	int bestScore = isMax ? BLACK_WIN_SCORE-1 : WHITE_WIN_SCORE+1;	// make sure that this will be updated
	int bestMove = 0;
	int curScore;

	// base case
	if (depth == 0)
		return NULL;

	for (int i = 0; i < moves->count; ++i) {
		move = moves->moves[i].move;

		if (!MakeMove(pos, move)) {
			moves->moves[i].score = NOMOVE;
			continue;
		}

		if (isMax == TRUE) {	// calling max function
			curScore = AlphaBetaMin(pos, alpha, beta, depth-1);
			if (curScore > bestScore) {
				bestScore = curScore;
				bestMove = move;
				if(bestScore > alpha) {
					alpha = bestScore;
					// break;
				}

			}
			if (alpha >= beta) {
				TakeMove(pos);
				break;
			}
		} else {				// calling min function
			curScore = AlphaBetaMax(pos, alpha, beta, depth-1);
			if (curScore < bestScore) {
				bestScore = curScore;
				bestMove = move;
				if(bestScore < beta) {
					beta = bestScore;
					// break;
				}
			}
			if (alpha >= beta) {
				TakeMove(pos);
				break;
			}
		}
		moves->moves[i].score = bestScore;
		legalMovesCount += 1;

	}

	if (legalMovesCount == 0) {
		TakeMove(pos);
		return NULL;	// no moves to make
	} else {
		TakeMove(pos);
		return PrMove(bestMove);
	}
}

int AlphaBetaMax(S_BOARD *pos, int alpha, int beta, int depth) {
	S_MOVELIST moves[1];
	int legalMovesCount = 0;
	int move;
	int bestScore = BLACK_WIN_SCORE - 1;		// make sure that this will be updated
	int bestMove = 0;
	int curScore;
	GenerateAllMoves(pos, moves);

	// base case
	if (depth == 0)
		return evaluation(pos, moves);

	for (int i = 0; i < moves->count; ++i) {
		move = moves->moves[i].move;

		if (!MakeMove(pos, move)) {
			continue;
		}

		// calling min function
		curScore = AlphaBetaMin(pos, alpha, beta, depth-1);
		if (curScore > bestScore) {
			bestScore = curScore;
			bestMove = move;
			if(bestScore > alpha)
				alpha = bestScore;
			if (alpha > beta)	 { // beta is lower than alpha, meaning that min player will choose another path for sure
				TakeMove(pos);
				break;
			}
		}

		TakeMove(pos);
		legalMovesCount += 1;
	}

	if (legalMovesCount == 0) {
		int InCheck = SqAttacked(pos->KingSq[pos->side], pos->side ^ 1, pos);
		if (InCheck == TRUE) {	// checkmate
			return pos->side == WHITE ? WHITE_WIN_SCORE : BLACK_WIN_SCORE;
		} else {				// stalemate, draw
			return DRAW_SCORE;
		}
	} else {
		return bestScore;
	}
}


int AlphaBetaMin(S_BOARD *pos, int alpha, int beta, int depth) {
	S_MOVELIST moves[1];
	int legalMovesCount = 0;
	int move;
	int bestScore = WHITE_WIN_SCORE + 1;		// make sure that this will be updated
	int bestMove = 0;
	int curScore;
	GenerateAllMoves(pos, moves);

	// base case
	if (depth == 0)
		return evaluation(pos, moves);

	for (int i = 0; i < moves->count; ++i) {
		move = moves->moves[i].move;

		if (!MakeMove(pos, move)) {
			continue;
		}

		// calling min function
		curScore = AlphaBetaMax(pos, alpha, beta, depth-1);
		if (curScore < bestScore) {
			bestScore = curScore;
			bestMove = move;
			if(bestScore < beta)
				beta = bestScore;
			if (alpha > beta){// beta is lower than alpha, meaning that max player will choose another path for sure
				TakeMove(pos);
				break;
			}

		}

		TakeMove(pos);
		legalMovesCount += 1;
	}

	if (legalMovesCount == 0) {
		int InCheck = SqAttacked(pos->KingSq[pos->side], pos->side ^ 1, pos);
		if (InCheck == TRUE) {	// checkmate
			return pos->side == WHITE ? WHITE_WIN_SCORE : BLACK_WIN_SCORE;
		} else {				// stalemate, draw
			return DRAW_SCORE;
		}
	} else {
		return bestScore;
	}
}


int compareMoveMax (const void * a, const void * b) {
  return ((S_MOVE*)a)->score  - ((S_MOVE*)b)->score;
}

int compareMoveMin(const void * a, const void * b) {
  return ((S_MOVE*)b)->score  - ((S_MOVE*)a)->score;
}

char* IterativeDeepning(S_BOARD *pos, int alpha, int beta, int depth, int isMax) {
	S_MOVELIST moves[1];
	GenerateAllMoves(pos, moves);
	char *bestMove;
	if (isMax) {
		for (int d = 1; d <= depth; ++d) {
			bestMove = AlphaBetaRoot(pos, alpha, beta, d, isMax, moves);
			qsort(moves->moves, moves->count, sizeof(S_MOVE), compareMoveMax);
		}
	} else {
		for (int d = 1; d <= depth; ++d) {
			bestMove = AlphaBetaRoot(pos, alpha, beta, d, isMax, moves);
			qsort(moves->moves, moves->count, sizeof(S_MOVE), compareMoveMin);
		}
	}

	return bestMove;
}



// #define python_wrapper

#ifdef python_wrapper
#include <Python.h>

PyObject * next_move(PyObject *self, PyObject *args) {
	char *game_fen, *next_move;

	if(!PyArg_ParseTuple(args, "s", &game_fen))
		return NULL;

	AllInit();
	S_BOARD board[1];
	ParseFen(game_fen, board);
	next_move = IterativeDeepning(board, BLACK_WIN_SCORE-1, WHITE_WIN_SCORE+1, 6, FALSE);
	return Py_BuildValue("s", next_move);

}

//Method definition object for this extension, these argumens mean:
//ml_name: The name of the method
//ml_meth: Function pointer to the method implementation
//ml_flags: Flags indicating special features of this method, such as
//          accepting arguments, accepting keyword arguments, being a
//          class method, or being a static method of a class.
//ml_doc:  Contents of this method's docstring
static PyMethodDef chess_methods[] = {
    {
        "next_move",
        next_move,
        METH_VARARGS,
        "evaluate a chess board position from fen string"
    },
    {NULL, NULL, 0, NULL}
};


//Module definition
//The arguments of this structure tell Python what to call your extension,
//what it's methods are and where to look for it's method definitions
static struct PyModuleDef chess_definition = {
    PyModuleDef_HEAD_INIT,
    "evaluation",
    "A Python module that provides next move string given a fen",
    -1,
    chess_methods
};

//Module initialization
//Python calls this function when importing your extension. It is important
//that this function is named PyInit_[[your_module_name]] exactly, and matches
//the name keyword argument in setup.py's setup() call.
PyMODINIT_FUNC PyInit_chess_in_c(void)
{
    Py_Initialize();
    return PyModule_Create(&chess_definition);
}

#else

int main(int argc, char const *argv[])
{
	/* code */
	AllInit();

	S_BOARD board[1];
	const char* fen = argv[1];
	// ParseFen(START_FEN, board);
	ParseFen(fen, board);
	S_MOVELIST moves[1];
	GenerateAllMoves(board, moves);
	printf("%s", AlphaBetaRoot(board, BLACK_WIN_SCORE-1, WHITE_WIN_SCORE+1, 6, FALSE, moves));
	// printf("%s", IterativeDeepning(board, BLACK_WIN_SCORE-1, WHITE_WIN_SCORE+1, 6, FALSE));

	// ASSERT(CheckBoard(board));


	return 0;
}



#endif