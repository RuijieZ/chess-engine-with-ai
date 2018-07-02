#include <stdio.h>
#include "defs.h"


// void ShowSqAtBySide(const int side, const S_BOARD *pos) {
// 	int rank =0;
// 	int file =0;
// 	int sq = 0;

// 	printf("\n\n Squares attacked by:%c\n", SideChar[side]);
// 	for (rank = RANK_8; rank >= RANK_1; --rank) {
// 		for (file = FILE_A; file <= FILE_H; ++file) {
// 			sq = FR2SQ(file, rank);
// 			if (SqAttacked(sq, side, pos) == TRUE){
// 				printf("X");
// 			} else {
// 				printf("-");
// 			}
// 		}
// 		printf("\n");
// 	}
// }


int main(int argc, char const *argv[])
{
	/* code */
	AllInit();

	S_BOARD board[1];
	S_MOVELIST list[1];
	// char* fen ="rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1";
	ParseFen(START_FEN, board);
	PerftTest(7, board);



	// ASSERT(CheckBoard(board));


	return 0;
}
