// #include <Python.h>
#include <string.h>
#include <stdio.h>

#include "defs.h"
#include "stdio.h"

const int pawn_eval_white[64] = {
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10,  -20, -20,  10,  10,  5,
    5, -5,-10,  0,  0, -10, -5,  5,
    0,  0,  0,  20,  20,  0,  0,  0,
    5,  5, 10,  25,  25,  10,  5,  5,
    10, 10, 20,  30,  30,  20,  10,  10,
    50, 50,  50,  50,  50,  50,  50,  50,
    0,  0,  0,  0,  0,  0,  0,  0
};

const int pawn_eval_black[64] = {
	0, 0, 0, 0, 0, 0, 0, 0,
	-50, -50, -50, -50, -50, -50, -50, -50,
	-10, -10, -20, -30, -30, -20, -10, -10,
	-5, -5, -10, -25, -25, -10, -5, -5,
	0, 0, 0, -20, -20, 0, 0, 0,
	-5,  5,  10, 0, 0,  10,  5, -5,
	-5, -10, -10,  20,  20, -10, -10, -5,
	0, 0, 0, 0, 0, 0, 0, 0
};

const int knight_eval_white[64] = {
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20,  0,  0,  0,  0, -20, -40,
    -30,  0,  10,  15,  15,  10,  0, -30,
    -30,  5,  15,  20,  20,  15,  5, -30,
    -30,  0,  15,  20,  20,  15,  0, -30,
    -30,  5,  10,  15,  15,  10,  5, -30,
    -40, -20,  0,  5,  5,  0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
};

const int knight_eval_black[64] = {
	50,  40,  30,  30,  30,  30,  40,  50,
	40,  20, 0, -5, -5, 0,  20,  40,
	30, -5, -10, -15, -15, -10, -5,  30,
	30, 0, -15, -20, -20, -15, 0,  30,
	30, -5, -15, -20, -20, -15, -5,  30,
	30, 0, -10, -15, -15, -10, 0,  30,
	40,  20, 0, 0, 0, 0,  20,  40,
	50,  40,  30,  30,  30,  30,  40,  50
};

const int bishop_eval_white[64] = {
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10,  5,  0,  0,  0,  0,  5, -10,
    -10,  10,  10,  10,  10,  10,  10, -10,
    -10,  0,  10,  10,  10,  10,  0, -10,
    -10,  5,  5,  10,  10,  5,  5, -10,
    -10,  0,  5,  10,  10,  5,  0, -10,
    -10,  0,  0,  0,  0,  0,  0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
};

const int bishop_eval_black[64] = {
	 20,  10,  10,  10,  10,  10,  10, 20,
	 10, 0, 0, 0, 0, 0, 0, 10,
	 10, 0, -5, -10, -10, -5, 0, 10,
	 10, -5, -5, -10, -10, -5, -5, 10,
	 10, 0, -10, -10, -10, -10, 0, 10,
	 10, -10, -10, -10, -10, -10, -10, 10,
	 10, -5, 0, 0, 0, 0, -5, 10,
	 20,  10,  10,  10,  10,  10,  10, 20
};

const int rook_eval_white[64] = {
    0,  0,  0,  0,  0,  0,  0,  0,
   -5,  0,  0,  0,  0,  0,  0, -5,
   -5,  0,  0,  0,  0,  0,  0, -5,
   -5,  0,  0,  0,  0,  0,  0, -5,
   -5,  0,  0,  0,  0,  0,  0, -5,
   -5,  0,  0,  0,  0,  0,  0, -5,
    5,  10,  10,  10,  10,  10,  10,  5,
    0,   0, 0,  5,  5,  0,  0,  0
};

const int rook_eval_black[64] = {
   0, 0, 0, -5, -5, 0, 0, 0,
   -5, -10, -10, -10, -10, -10, -10, -5,
    5, 0, 0, 0, 0, 0, 0,  5,
    5, 0, 0, 0, 0, 0, 0,  5,
    5, 0, 0, 0, 0, 0, 0,  5,
    5, 0, 0, 0, 0, 0, 0,  5,
    5, 0, 0, 0, 0, 0, 0,  5,
    0, 0, 0, 0,0,0, 0,  0
};

const int eval_queen_white[64] = {
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10,  0,  0,  0,  0,  0,  0, -10,
    -10,  0,  5,  5,  5,  5,  0, -10,
    -5,  0,  5,  5,  5,  5,  0, -5,
     -5,  0,  5,  5,  5,  5,  0, -5,
    -10,  0,  5,  5,  5,  5,  0, -10,
    -10,  0,  0,  0,  0,  0,  0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20
};

const int eval_queen_black[64] = {
	20,  10,  10,  5,  5,  10,  10, 20,
	10, 0, 0, 0, 0, 0, 0, 10,
	10, 0, -5, -5, -5, -5, 0, 10,
	5, 0, -5, -5, -5, -5, 0, 5,
    5, 0, -5, -5, -5, -5, 0, 5,
	10, 0, -5, -5, -5, -5, 0, 10,
	10, 0, 0, 0, 0, 0, 0, 10,
	20,  10,  10,  5,  5,  10,  10, 20
};

const int king_eval_white[64] = {
     20,  30,  10,  0,  0,  10,  30,  20,
     20,  20,  0,  0,  0,  0,  20,  20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30
};

const int king_eval_black[64] = {
	30,  40, 40,  50,   50,  40,  40,  30,
	30,  40, 40,  50,   50,  40,  40,  30,
	30,  40, 40,  50,   50,  40,  40,  30,
	30,  40, 40,  50,   50,  40,  40,  30,
	20,  30, 30,  40,   40,  30,  30,  20,
	10,  20, 20,  20,   20,  20,  20,  10,
   -20, -20, 0, 0, 0, 0, -20, -20,
   -20, -30, -10, 0, 0, -10, -30, -20
};


int evaluation(S_BOARD* pos, S_MOVELIST* moves) {
	int pceNum;
	int pce;
	int sq;

	// if(!pos->pceNum[wP] && !pos->pceNum[bP] && MaterialDraw(pos) == TRUE)
	// 	return DRAW_SCORE;

	/*
		for (int i = 0; i < moves->count; ++i) {
			move = moves->moves[i].move;

			if (!MakeMove(pos, move)) {
				continue;
			}
			TakeMove(pos);
			legalMovesCount += 1;
		}

		if (legalMovesCount == 0) {
			int InCheck = SqAttacked(pos->KingSq[pos->side], pos->side ^ 1, pos);
			if (InCheck == TRUE) {	// checkmate
				return pos->side == WHITE ? WHITE_WIN_SCORE : BLACK_WIN_SCORE;
			} else {	// stalemate, draw
				return DRAW_SCORE;
			}
		}
	*/

	// NOT a game ending situation, evalute the situation
	int score = pos->material[WHITE] - pos->material[BLACK];
	// printf("initial score is %5d\n", score);

	// white pawn
	pce = wP;
	for(pceNum = 0; pceNum < pos->pceNum[pce]; ++pceNum) {
		sq = pos->pList[pce][pceNum];
		ASSERT(SqOnBoard(sq));

		// printf("         sqr: %d\n", SQ64(sq));
		// printf("		 score:%d\n", pawn_eval_white[SQ64(sq)]);
		score += pawn_eval_white[SQ64(sq)];

		// if((IsolatedMask[SQ64(sq)] & pos->pawns[WHITE]) == 0)
		// 	score += PawnIsolated;

		// if((WhitePassedMask[SQ64(sq)] & pos->pawns[BLACK]) == 0)
		// 	score += PawnPassed[RanksBrd[sq]];
	}

	// printf("black pawn:\n");

	// black pawn
	pce = bP;
	for(pceNum = 0; pceNum < pos->pceNum[pce]; ++pceNum) {
		sq = pos->pList[pce][pceNum];
		ASSERT(SqOnBoard(sq));

		// printf("         sqr: %d\n", SQ64(sq));
		// printf("		 score:%d\n", pawn_eval_black[SQ64(sq)]);
		score += pawn_eval_black[SQ64(sq)];


		// if((IsolatedMask[SQ64(sq)] & pos->pawns[BLACK]) == 0)
		// 	score -= PawnIsolated;

		// if((BlackPassedMask[SQ64(sq)] & pos->pawns[WHITE]) == 0)
		// 	score -= PawnPassed[7 - RanksBrd[sq]];
	}

	// printf("current score is %d\n", score);

	// printf("white knight:\n");
	pce = wN;
	for(pceNum = 0; pceNum < pos->pceNum[pce]; ++pceNum) {
		sq = pos->pList[pce][pceNum];
		ASSERT(SqOnBoard(sq));
		// printf("         sqr: %d\n", SQ64(sq));
		// printf("		 score:%d\n", knight_eval_white[SQ64(sq)]);
		score += knight_eval_white[SQ64(sq)];
	}

	// printf("black knight:\n");

	pce = bN;
	for(pceNum = 0; pceNum < pos->pceNum[pce]; ++pceNum) {
		sq = pos->pList[pce][pceNum];
		ASSERT(SqOnBoard(sq));
		// printf("         sqr: %d\n", SQ64(sq));
		// printf("		 score:%d\n", knight_eval_white[SQ64(sq)]);
		score += knight_eval_black[SQ64(sq)];
	}

	pce = wB;
	for(pceNum = 0; pceNum < pos->pceNum[pce]; ++pceNum) {
		sq = pos->pList[pce][pceNum];
		ASSERT(SqOnBoard(sq));
		score += bishop_eval_white[SQ64(sq)];
	}

	pce = bB;
	for(pceNum = 0; pceNum < pos->pceNum[pce]; ++pceNum) {
		sq = pos->pList[pce][pceNum];
		ASSERT(SqOnBoard(sq));
		score += bishop_eval_black[SQ64(sq)];
	}

	pce = wR;
	for(pceNum = 0; pceNum < pos->pceNum[pce]; ++pceNum) {
		sq = pos->pList[pce][pceNum];
		ASSERT(SqOnBoard(sq));
		score += rook_eval_white[SQ64(sq)];

		// if(!(pos->pawns[BOTH] & FileBBMask[FilesBrd[sq]])) {
		// 	score += RookOpenFile;
		// } else if(!(pos->pawns[WHITE] & FileBBMask[FilesBrd[sq]])) {
		// 	score += RookSemiOpenFile;
		// }
	}

	pce = bR;
	for(pceNum = 0; pceNum < pos->pceNum[pce]; ++pceNum) {
		sq = pos->pList[pce][pceNum];
		ASSERT(SqOnBoard(sq));
		score += rook_eval_black[SQ64(sq)];

		// if(!(pos->pawns[BOTH] & FileBBMask[FilesBrd[sq]])) {
		// 	score -= RookOpenFile;
		// } else if(!(pos->pawns[BLACK] & FileBBMask[FilesBrd[sq]])) {
		// 	score -= RookSemiOpenFile;
		// }
	}

	pce = wQ;
	for(pceNum = 0; pceNum < pos->pceNum[pce]; ++pceNum) {
		sq = pos->pList[pce][pceNum];
		ASSERT(SqOnBoard(sq));
		score += eval_queen_white[SQ64(sq)];
		// if(!(pos->pawns[BOTH] & FileBBMask[FilesBrd[sq]])) {
		// 	score += QueenOpenFile;
		// } else if(!(pos->pawns[WHITE] & FileBBMask[FilesBrd[sq]])) {
		// 	score += QueenSemiOpenFile;
		// }
	}

	pce = bQ;
	for(pceNum = 0; pceNum < pos->pceNum[pce]; ++pceNum) {
		sq = pos->pList[pce][pceNum];
		ASSERT(SqOnBoard(sq));
		score += eval_queen_black[SQ64(sq)];
		// if(!(pos->pawns[BOTH] & FileBBMask[FilesBrd[sq]])) {
		// 	score -= QueenOpenFile;
		// } else if(!(pos->pawns[BLACK] & FileBBMask[FilesBrd[sq]])) {
		// 	score -= QueenSemiOpenFile;
		// }
	}

	pce = wK;
	sq = pos->pList[pce][0];
	score += king_eval_white[SQ64(sq)];
	// if(pos->material[BLACK] <= ENDGAME_MAT) {
	// 	score += KingE[SQ64(sq)];
	// } else {
	// 	score += KingO[SQ64(sq)];
	// }

	pce = bK;
	sq = pos->pList[pce][0];
	score += king_eval_black[SQ64(sq)];
	// if(pos->material[WHITE] <= ENDGAME_MAT) {
	// 	score -= KingE[MIRROR64(SQ64(sq))];
	// } else {
	// 	score -= KingO[MIRROR64(SQ64(sq))];
	// }

	// if(pos->pceNum[wB] >= 2) score += BishopPair;
	// if(pos->pceNum[bB] >= 2) score -= BishopPair;

	// if(pos->side == WHITE) {
	// 	return score;
	// } else {
	// 	return -score;
	// }

	return score;
}