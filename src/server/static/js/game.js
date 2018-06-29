let WHITE = 'w';
let BLACK = 'b';
let HUMAN = 'HUMAN';
let AI = 'AI';

/*
Game class
*/
class Game {
    constructor(board, chess) {
        this.board = board;
        this.chess = chess;
        this.players = {
            'w': HUMAN,
            'b': AI
        }
        this.stepCount = 0;
    }

    newGame() {
        return true;
    }
}

/*
Helper functions
*/
function queryNextMove() {
    var chess = window.game.chess;
    var data = {
        'fen': chess.fen(),
        'w': window.game.players['w'],
        'b': window.game.players['b']
    };
    $.post("/next_move/" + window.game.stepCount.toString(), data, function(result){
    	var serverMove = {						// reformat the move so that the frontend code can understand
    		'from': result.substring(0,2),
    		'to': result.substring(2,result.length)
    	}
		window.game.chess.move(serverMove);		// make the move
  		console.log('the move returned from server is: ' + result);
		window.game.board.position(window.game.chess.fen());
  		updateStatus();
    });
}

var onDragStart = function(source, piece, position, orientation) {
    chess = window.game.chess;
    if ((chess.turn() === BLACK && piece.search(/^b/) === -1) || (chess.turn() === WHITE && piece.search(/^w/) === -1) || chess.game_over()) {
        return false;
    }
    return true;
};


var onDrop = function(source, target) {
  // see if the move is legal
  var move = window.game.chess.move({
    from: source,
    to: target,
    promotion: 'q' // NOTE: always promote to a queen for example simplicity
  });

  // illegal move
  if (move === null) return 'snapback';

  updateStatus();
};


var updateStatus = function() {
    var chess = window.game.chess;
    var status = '';
    var statusEl = $('#status');
    var fenEl = $('#fen');
    var pgnEl = $('#pgn');

    var moveColor = 'White';
    window.game.stepCount += 1;
    if (chess.turn() === 'b') {
        moveColor = 'Black';
    }

    // checkmate?
    if (chess.in_checkmate() === true) {
        status = 'Game over, ' + moveColor + ' is in checkmate.';
    }

    // draw?
    else if (chess.in_draw() === true) {
        status = 'Game over, drawn position';
    }

    // game still on
    else {
        status = moveColor + ' to move';

        // check?
        if (chess.in_check() === true) {
            status += ', ' + moveColor + ' is in check';
        }
    }

    statusEl.html(status);
    fenEl.html(chess.fen());
    pgnEl.html(chess.pgn());
};

// update the board position after the piece snap
// for castling, en passant, pawn promotion
var onSnapEnd = function() {
    window.game.board.position(window.game.chess.fen());
    if ((chess.turn() === BLACK && window.game.players['b'] == AI) || (chess.turn() === WHITE && window.game.players['w'] == AI))
        queryNextMove();
};

var init = function() {
    var cfg = {
        draggable: true,
        dropOffBoard: 'snapback', // this is the default
        position: 'start',
        onDragStart: onDragStart,
        onDrop: onDrop,
        onSnapEnd: onSnapEnd
    };
    if (window.game === undefined) {
        var chess = new Chess();
        var board = ChessBoard('board', cfg);
        window.game = new Game(board, chess);
    }
};
$(document).ready(init);