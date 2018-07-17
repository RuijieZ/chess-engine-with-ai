#include <stdio.h>
#include <stdlib.h>     /* qsort */
#include "defs.h"
#include "uthash.h"		// dictionary implementation

int BRANCH_REDUCE_FACTOR = 6;

struct board_result {
    U64 id;            			/* we'll use this field as the key */
    int depth;					/* depth of the last search */
    int s_score;
    UT_hash_handle hh; 			/* makes this structure hashable */
};

struct board_result *d= NULL;	// default value

void add_score(struct board_result *s) {
    HASH_ADD_INT(d, id, s);
}

struct board_result *find_score(int user_id) {
    struct board_result *s;

    HASH_FIND_INT( d, &user_id, s);
    return s;
}

static int IsRepetition(const S_BOARD *pos) {
	int index = 0;
	for(index = pos->hisPly - pos->fiftyMove; index < pos->hisPly-1; ++index) {	
		ASSERT(index >= 0 && index < MAXGAMEMOVES);
		if(pos->posKey == pos->history[index].posKey) {
			return TRUE;
		}
	}	
	return FALSE;
}

int AlphaBetaMin(S_BOARD *pos, int alpha, int beta, int depth);
int AlphaBetaMax(S_BOARD *pos, int alpha, int beta, int depth);
// char *AlphaBetaRoot(S_BOARD *pos, int alpha, int beta, int depth, int isMax, S_MOVELIST* moves);


static void PickNextMove(int moveNum, S_MOVELIST *list) {
	S_MOVE temp;
	int index = 0;
	int bestScore = 0;
	int bestNum = moveNum;

	for (index = moveNum; index < list->count; ++index) {
		if (list->moves[index].score > bestScore) {
			bestScore = list->moves[index].score;
			bestNum = index;
		}
	}

	ASSERT(moveNum>=0 && moveNum<list->count);
	ASSERT(bestNum>=0 && bestNum<list->count);
	ASSERT(bestNum>=moveNum);

	temp = list->moves[moveNum];
	list->moves[moveNum] = list->moves[bestNum];
	list->moves[bestNum] = temp;
}

// char *AlphaBetaRoot(S_BOARD *pos, int alpha, int beta, int depth, int isMax, S_MOVELIST* moves) {
// 	int legalMovesCount = 0;
// 	int move;
// 	int bestScore = isMax ? BLACK_WIN_SCORE-1 : WHITE_WIN_SCORE+1;	// make sure that this will be updated
// 	int bestMove = 0;
// 	int curScore;

// 	// base case
// 	if (depth == 0)
// 		return NULL;

// 	for (int i = 0; i < moves->count; ++i) {
// 		PickNextMove(i, moves);
// 		move = moves->moves[i].move;
// 		if (!MakeMove(pos, move)) {
// 			// moves->moves[i].score = NOMOVE;
// 			continue;
// 		}

// 		if (isMax == TRUE) {	// calling max function
// 			curScore = AlphaBetaMin(pos, alpha, beta, depth-1);
// 			TakeMove(pos);
// 			if (curScore > bestScore) {
// 				bestScore = curScore;
// 				bestMove = move;
// 			}

// 			if(bestScore > alpha) {
// 				alpha = bestScore;
// 			}

// 			if (alpha >= beta) {
// 				break;
// 			}
// 		} else {				// calling min function
// 			curScore = AlphaBetaMax(pos, alpha, beta, depth-1);
// 			TakeMove(pos);
// 			if (curScore < bestScore) {
// 				bestScore = curScore;
// 				bestMove = move;
// 			}

// 			if(bestScore < beta) {
// 				beta = bestScore;
// 			}

// 			if (alpha >= beta) {
// 				break;
// 			}
// 		}
// 		// moves->moves[i].score = bestScore;
// 		legalMovesCount += 1;

// 	}

// 	if (legalMovesCount == 0) {
// 		return NULL;	// no moves to make
// 	} else {
// 		return PrMove(bestMove);
// 	}
// }

int AlphaBetaMax(S_BOARD *pos, int alpha, int beta, int depth) {
	S_MOVELIST moves[1];


	if(IsRepetition(pos)) {
		return 0;
	}

	// base case
	if (depth <= 0)
		return evaluation(pos, moves);

	// struct board_result *br= find_score(pos->posKey);	// default value
	// if (br != NULL) {
	// 	if (br->depth >= depth) {
	// 		return br->s_score;
	// 	}
	// }

	int legalMovesCount = 0;
	int move;
	int bestScore = BLACK_WIN_SCORE - 1;		// make sure that this will be updated
	int bestMove = 0;
	int curScore;
	GenerateAllMoves(pos, moves);

	// use pv move to help
	int PvMove = ProbePvTable(pos);
	if( PvMove != NOMOVE) {
		for(int MoveNum = 0; MoveNum < moves->count; ++MoveNum) {
			if( moves->moves[MoveNum].move == PvMove) {
				moves->moves[MoveNum].score = 2000000;
				//printf("Pv move found \n");
				break;
			}
		}
	}



	int OldAlpha = alpha;
	for (int i = 0; i < moves->count; ++i) {
		// move = moves->moves[i].move;
		PickNextMove(i, moves);
		move = moves->moves[i].move;

		if (!MakeMove(pos, move)) {
			continue;
		}


		// calling min function
		if (legalMovesCount <= moves->count / BRANCH_REDUCE_FACTOR){
			curScore = AlphaBetaMin(pos, alpha, beta, depth-1);	// only search the first two moves to full depth
		}
		else {
			curScore = AlphaBetaMin(pos, alpha, beta, depth-4);
		}
		legalMovesCount += 1;

		TakeMove(pos);
		if (curScore > bestScore) {
			bestScore = curScore;
			bestMove = move;

		}
		if(bestScore > alpha)
			alpha = bestScore;
		if (alpha >= beta)	 { // beta is lower than alpha, meaning that min player will choose another path for sure
			bestScore = beta;
			break;
		}

	}

	if (legalMovesCount == 0) {
		int InCheck = SqAttacked(pos->KingSq[pos->side], pos->side ^ 1, pos);
		if (InCheck == TRUE) {	// checkmate
			bestScore = pos->side == WHITE ? BLACK_WIN_SCORE : WHITE_WIN_SCORE;
		} else {				// stalemate, draw
			bestScore = DRAW_SCORE;
		}
	}

	// // store the result we computed
	// // free(br);	// get rid of the old one, if it is NULL, no action occurs
	// if (br == NULL) {
	// 	br = malloc(sizeof(struct board_result));
	// 	br->s_score = bestScore;
	// 	br->id = pos->posKey;
	// 	br->depth = depth;
	// } else {
	// 	br->s_score =bestScore;
	// 	br->depth = depth;
	// }
	// add_score(br);
	if(alpha != OldAlpha) {
		StorePvMove(pos, bestMove);
	}

	return bestScore;

}


int AlphaBetaMin(S_BOARD *pos, int alpha, int beta, int depth) {

	S_MOVELIST moves[1];

	if(IsRepetition(pos)) {
		return 0;
	}
	// base case
	if (depth <= 0)
		return evaluation(pos, moves);
	// struct board_result *br= find_score(pos->posKey);	// default value
	// if (br != NULL) {
	// 	if (br->depth >= depth) {
	// 		return br->s_score;
	// 	}
	// }

	int legalMovesCount = 0;
	int move;
	int bestScore = WHITE_WIN_SCORE + 1;		// make sure that this will be updated
	int bestMove = 0;
	int curScore;
	GenerateAllMoves(pos, moves);

	int PvMove = ProbePvTable(pos);
	if( PvMove != NOMOVE) {
		for(int MoveNum = 0; MoveNum < moves->count; ++MoveNum) {
			if( moves->moves[MoveNum].move == PvMove) {
				moves->moves[MoveNum].score = 2000000;
				//printf("Pv move found \n");
				break;
			}
		}
	}



	int OldBeta = beta;
	for (int i = 0; i < moves->count; ++i) {
		// move = moves->moves[i].move;
		PickNextMove(i, moves);
		move = moves->moves[i].move;
		if (!MakeMove(pos, move)) {
			continue;
		}

		// calling min function
		if (legalMovesCount <= moves->count / BRANCH_REDUCE_FACTOR) {
			curScore = AlphaBetaMax(pos, alpha, beta, depth-1);
		}
		else {
			curScore = AlphaBetaMax(pos, alpha, beta, depth-4);
		}
		legalMovesCount += 1;
		TakeMove(pos);
		if (curScore < bestScore) {
			bestScore = curScore;
			bestMove = move;
		}
		if(bestScore < beta)
			beta = bestScore;
		if (alpha >= beta){// beta is lower than alpha, meaning that max player will choose another path for sure
			bestScore = alpha;
			break;
		}

	}

	if (legalMovesCount == 0) {
		int InCheck = SqAttacked(pos->KingSq[pos->side], pos->side ^ 1, pos);
		if (InCheck == TRUE) {	// checkmate
			bestScore = pos->side == WHITE ? BLACK_WIN_SCORE: WHITE_WIN_SCORE;
		} else {				// stalemate, draw
			bestScore = DRAW_SCORE;
		}
	}

	// free(br);	// get rid of the old one, if it is NULL, no action occurs
	// if (br == NULL) {
	// 	br = malloc(sizeof(struct board_result));
	// 	br->s_score = bestScore;
	// 	br->id = pos->posKey;
	// 	br->depth = depth;
	// } else {
	// 	br->s_score =bestScore;
	// 	br->depth = depth;
	// }
	// add_score(br);

	if(beta != OldBeta) {
		StorePvMove(pos, bestMove);
	}

	return bestScore;
}


int compareMoveMax (const void * a, const void * b) {
  return ((S_MOVE*)a)->score  - ((S_MOVE*)b)->score;
}

int compareMoveMin(const void * a, const void * b) {
  return ((S_MOVE*)b)->score  - ((S_MOVE*)a)->score;
}

// char* IterativeDeepning(S_BOARD *pos, int alpha, int beta, int depth, int isMax) {
// 	S_MOVELIST moves[1];
// 	GenerateAllMoves(pos, moves);
// 	char *bestMove;
// 	if (isMax) {
// 		for (int d = 1; d <= depth; ++d) {
// 			bestMove = AlphaBetaRoot(pos, alpha, beta, d, isMax, moves);
// 			qsort(moves->moves, moves->count, sizeof(S_MOVE), compareMoveMax);
// 		}
// 	} else {
// 		for (int d = 1; d <= depth; ++d) {
// 			bestMove = AlphaBetaRoot(pos, alpha, beta, d, isMax, moves);
// 			qsort(moves->moves, moves->count, sizeof(S_MOVE), compareMoveMin);
// 		}
// 	}

// 	return bestMove;
// }



// #define python_wrapper

#ifdef python_wrapper
#include <Python.h>

PyObject * next_move(PyObject *self, PyObject *args) {
	char *game_fen, *next_move;
	int depth;

	if(!PyArg_ParseTuple(args, "si", &game_fen, &depth))
		return NULL;

	AllInit();
	S_BOARD board[1];
	InitPvTable(board->PvTable);
	ParseFen(game_fen, board);

	// next_move = IterativeDeepning(board, BLACK_WIN_SCORE-1, WHITE_WIN_SCORE+1, 6, FALSE);
	for (int i=1; i <= depth; i++) {
		printf("%d\n", AlphaBetaMin(board, BLACK_WIN_SCORE-1, WHITE_WIN_SCORE+1, i));
	}
	next_move = PrMove(ProbePvTable(board));
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
	ParseFen(fen, board);
	InitPvTable(board->PvTable);
	for (int i=1; i <= 10; i++) {
		printf("%d\n", AlphaBetaMin(board, BLACK_WIN_SCORE-1, WHITE_WIN_SCORE+1, i));
	}
	// printf("%s", IterativeDeepning(board, BLACK_WIN_SCORE-1, WHITE_WIN_SCORE+1, 6, FALSE));
	printf("%s\n", PrMove(ProbePvTable(board)));

	// ASSERT(CheckBoard(board));


	return 0;
}



#endif