#include <Python.h>
#include <string.h>
#include <stdio.h>
#include "evaluation.h"


int BLACK_WIN_SCORE = -10000;
int WHITE_WIN_SCORE = 10000;
int DRAW_SCORE = 0;
char WHITE_WINNING_SYMBOL[] = "1-0";
char BLACK_WINNING_SYMBOL[] = "0-1";
char GAME_UNDERTERMINED[] = "*";
char GAME_TIED[] = "1/2-1/2";

int pawn_eval_white[64] = {
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10,  -20, -20,  10,  10,  5,
    5, -5,-10,  0,  0, -10, -5,  5,
    0,  0,  0,  20,  20,  0,  0,  0,
    5,  5, 10,  25,  25,  10,  5,  5,
    10, 10, 20,  30,  30,  20,  10,  10,
    50, 50,  50,  50,  50,  50,  50,  50,
    0,  0,  0,  0,  0,  0,  0,  0
};

int pawn_eval_black[64] = {
	0, 0, 0, 0, 0, 0, 0, 0,
	-50, -50, -50, -50, -50, -50, -50, -50,
	-10, -10, -20, -30, -30, -20, -10, -10,
	-5, -5, -10, -25, -25, -10, -5, -5,
	0, 0, 0, -20, -20, 0, 0, 0,
	-5,  5,  10, 0, 0,  10,  5, -5,
	-5, -10, -10,  20,  20, -10, -10, -5,
	0, 0, 0, 0, 0, 0, 0, 0
};

int knight_eval_white[64] = {
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20,  0,  0,  0,  0, -20, -40,
    -30,  0,  10,  15,  15,  10,  0, -30,
    -30,  5,  15,  20,  20,  15,  5, -30,
    -30,  0,  15,  20,  20,  15,  0, -30,
    -30,  5,  10,  15,  15,  10,  5, -30,
    -40, -20,  0,  5,  5,  0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50
};

int knight_eval_black[64] = {
	50,  40,  30,  30,  30,  30,  40,  50,
	40,  20, 0, -5, -5, 0,  20,  40,
	30, -5, -10, -15, -15, -10, -5,  30,
	30, 0, -15, -20, -20, -15, 0,  30,
	30, -5, -15, -20, -20, -15, -5,  30,
	30, 0, -10, -15, -15, -10, 0,  30,
	40,  20, 0, 0, 0, 0,  20,  40,
	50,  40,  30,  30,  30,  30,  40,  50
};

int bishop_eval_white[64] = {
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10,  5,  0,  0,  0,  0,  5, -10,
    -10,  10,  10,  10,  10,  10,  10, -10,
    -10,  0,  10,  10,  10,  10,  0, -10,
    -10,  5,  5,  10,  10,  5,  5, -10,
    -10,  0,  5,  10,  10,  5,  0, -10,
    -10,  0,  0,  0,  0,  0,  0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20
};

int bishop_eval_black[64] = {
	 20,  10,  10,  10,  10,  10,  10, 20,
	 10, 0, 0, 0, 0, 0, 0, 10,
	 10, 0, -5, -10, -10, -5, 0, 10,
	 10, -5, -5, -10, -10, -5, -5, 10,
	 10, 0, -10, -10, -10, -10, 0, 10,
	 10, -10, -10, -10, -10, -10, -10, 10,
	 10, -5, 0, 0, 0, 0, -5, 10,
	 20,  10,  10,  10,  10,  10,  10, 20
};

int rook_eval_white[64] = {
    0,  0,  0,  0,  0,  0,  0,  0,
   -5,  0,  0,  0,  0,  0,  0, -5,
   -5,  0,  0,  0,  0,  0,  0, -5,
   -5,  0,  0,  0,  0,  0,  0, -5,
   -5,  0,  0,  0,  0,  0,  0, -5,
   -5,  0,  0,  0,  0,  0,  0, -5,
    5,  10,  10,  10,  10,  10,  10,  5,
    0,   0, 0,  5,  5,  0,  0,  0
};

int rook_eval_black[64] = {
   0, 0, 0, -5, -5, 0, 0, 0,
   -5, -10, -10, -10, -10, -10, -10, -5,
    5, 0, 0, 0, 0, 0, 0,  5,
    5, 0, 0, 0, 0, 0, 0,  5,
    5, 0, 0, 0, 0, 0, 0,  5,
    5, 0, 0, 0, 0, 0, 0,  5,
    5, 0, 0, 0, 0, 0, 0,  5,
    0, 0, 0, 0,0,0, 0,  0
};

int eval_queen_white[64] = {
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10,  0,  0,  0,  0,  0,  0, -10,
    -10,  0,  5,  5,  5,  5,  0, -10,
    -5,  0,  5,  5,  5,  5,  0, -5,
     -5,  0,  5,  5,  5,  5,  0, -5,
    -10,  0,  5,  5,  5,  5,  0, -10,
    -10,  0,  0,  0,  0,  0,  0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20
};

int eval_queen_black[64] = {
	20,  10,  10,  5,  5,  10,  10, 20,
	10, 0, 0, 0, 0, 0, 0, 10,
	10, 0, -5, -5, -5, -5, 0, 10,
	5, 0, -5, -5, -5, -5, 0, 5,
    5, 0, -5, -5, -5, -5, 0, 5,
	10, 0, -5, -5, -5, -5, 0, 10,
	10, 0, 0, 0, 0, 0, 0, 10,
	20,  10,  10,  5,  5,  10,  10, 20
};

int king_eval_white[64] = {
     20,  30,  10,  0,  0,  10,  30,  20,
     20,  20,  0,  0,  0,  0,  20,  20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30
};

int king_eval_black[64] = {
	30,  40, 40,  50,   50,  40,  40,  30,
	30,  40, 40,  50,   50,  40,  40,  30,
	30,  40, 40,  50,   50,  40,  40,  30,
	30,  40, 40,  50,   50,  40,  40,  30,
	20,  30, 30,  40,   40,  30,  30,  20,
	10,  20, 20,  20,   20,  20,  20,  10,
   -20, -20, 0, 0, 0, 0, -20, -20,
   -20, -30, -10, 0, 0, -10, -30, -20
};


PyObject * evaluation(PyObject *self, PyObject *args) {
	char *game_result, *board_fen;
	int len;

	if(!PyArg_ParseTuple(args, "ssi", &game_result, &board_fen, &len))
		return NULL;

	if (strcmp(game_result, WHITE_WINNING_SYMBOL) == 0)
		return Py_BuildValue("i", WHITE_WIN_SCORE);

	if (strcmp(game_result, BLACK_WINNING_SYMBOL) == 0)
		return Py_BuildValue("i", BLACK_WIN_SCORE);

	if (strcmp(game_result, GAME_TIED) == 0)
		return Py_BuildValue("i", 0);

	if (strcmp(game_result, GAME_UNDERTERMINED) != 0)		// All above check failed, means this has to true, other wise something wrong
		return NULL;


	// parse the board_fen
	int idx = 0, score=0;
	for (int i=len-1; i >= 0; --i) {  // read from the back because the fen string is reversed
		switch(board_fen[i]) {
		   	case '1':
		      	idx += 1;
		      	break;
		    case '2':
		      	idx += 2;
		     	break;
		   	case '3':
		      	idx += 3;
		      	break;
		    case '4':
		      	idx += 4;
		     	break;
		   	case '5':
		      	idx += 5;
		      	break;
		    case '6':
		      	idx += 6;
		     	break;
		   	case '7':
		      	idx += 7;
		      	break;
		    case '8':
		      	idx += 8;
		     	break;

		    // handle strings
		    case '/':
		      	break;

		    // black pieces
		    case 'n':
		    	score += (-300 + knight_eval_black[idx]) ;
		      	idx += 1;
		     	break;
		   	case 'b':
		   		score += (-300 + bishop_eval_black[idx]);
		      	idx += 1;
		      	break;
		    case 'r':
		      	score += (-500 + rook_eval_black[idx]);
		      	idx += 1;
		     	break;
		   	case 'q':
		   		score += (-900 + eval_queen_black[idx]);
		      	idx += 1;
		      	break;
		    case 'p':
		    	score += (-100 + pawn_eval_black[idx]);
		      	idx += 1;
		     	break;
		   	case 'k':
		   		score += (-1000 + king_eval_black[idx]);
		      	idx += 1;
		      	break;

		    // white pieces
		    case 'N':
		    	score += (300 + knight_eval_white[idx]);
		      	idx += 1;
		     	break;
		   	case 'B':
		   		score += (300 + bishop_eval_white[idx]);
		      	idx += 1;
		      	break;
		    case 'R':
		      	score += (500 + rook_eval_white[idx]);
		      	idx += 1;
		     	break;
		   	case 'Q':
		   		score += (900 + eval_queen_white[idx]);
		      	idx += 1;
		      	break;
		    case 'P':
		    	score += (100 + pawn_eval_white[idx]);
		      	idx += 1;
		     	break;
		   	case 'K':
		   		score += (1000 + king_eval_white[idx]);
		      	idx += 1;
		      	break;
		}
	}
	return Py_BuildValue("i", score);
}

//Method definition object for this extension, these argumens mean:
//ml_name: The name of the method
//ml_meth: Function pointer to the method implementation
//ml_flags: Flags indicating special features of this method, such as
//          accepting arguments, accepting keyword arguments, being a
//          class method, or being a static method of a class.
//ml_doc:  Contents of this method's docstring
static PyMethodDef evaluation_methods[] = {
    {
        "evaluation",
        evaluation,
        METH_VARARGS,
        "evaluate a chess board position from fen string"
    },
    {NULL, NULL, 0, NULL}
};


//Module definition
//The arguments of this structure tell Python what to call your extension,
//what it's methods are and where to look for it's method definitions
static struct PyModuleDef evaluation_definition = {
    PyModuleDef_HEAD_INIT,
    "evaluation",
    "A Python module that evaluates chess board fen string from C code, gives a score of that ocde",
    -1,
    evaluation_methods
};

//Module initialization
//Python calls this function when importing your extension. It is important
//that this function is named PyInit_[[your_module_name]] exactly, and matches
//the name keyword argument in setup.py's setup() call.
PyMODINIT_FUNC PyInit_evaluation(void)
{
    Py_Initialize();
    return PyModule_Create(&evaluation_definition);
}


