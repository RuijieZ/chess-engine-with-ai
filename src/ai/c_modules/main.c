#include <stdio.h>
#include "defs.h"


char *AlphaBetaRoot(S_BOARD *pos, int alpha, int beta, int depth, int isMax) {
	S_MOVELIST moves[1];
	int legalMovesCount = 0;
	int move;
	int bestScore = isMax ? BLACK_WIN_SCORE-1 : WHITE_WIN_SCORE+1;	// make sure that this will be updated
	int bestMove = 0;
	int curScore;
	GenerateAllMoves(pos, moves);

	// base case
	if (depth == 0)
		return NULL;

	for (int i = 0; i < moves->count; ++i) {
		move = moves->moves[i].move;

		if (!MakeMove(pos, move)) {
			continue;
		}

		if (isMax == TRUE) {	// calling max function
			curScore = AlphaBetaMin(pos, alpha, beta, depth-1);
			if (curScore > bestScore) {
				bestScore = curScore;
				bestMove = move;
				if(bestScore > alpha)
					alpha = bestScore;
			}
		} else {				// calling min function
			curScore = AlphaBetaMax(pos, alpha, beta, depth-1);
			if (curScore < bestScore) {
				bestScore = curScore;
				bestMove = move;
				if(bestScore < beta)
					beta = bestScore;
			}
		}

		TakeMove(pos);
		legalMovesCount += 1;

	}

	if (legalMovesCount == 0) {
		return NULL;	// no moves to make
	} else {
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



int main(int argc, char const *argv[])
{
	/* code */
	AllInit();

	S_BOARD board[1];

	ParseFen(START_FEN, board);

	printf("%s", AlphaBetaRoot(board, BLACK_WIN_SCORE-1, WHITE_WIN_SCORE+1, 8, TRUE));

	ASSERT(CheckBoard(board));


	return 0;
}
