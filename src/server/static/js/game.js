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
            WHITE: HUMAN,
            BLACK: AI
        }
    }

    newGame() {
        return true;
    }
}

/*
Helper functions
*/
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

// update the board position after the piece snap
// for castling, en passant, pawn promotion
var onSnapEnd = function() {
    board.position(window.game.chess.fen());
};


var updateStatus = function() {
    var chess = window.game.chess;
    var status = '';
    var statusEl = $('#status');
    var fenEl = $('#fen');
    var pgnEl = $('#pgn');

    var moveColor = 'White';
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
    var board = ChessBoard('board', cfg);
    var chess = new Chess();
    window.game = new Game(board, chess);
};
$(document).ready(init);