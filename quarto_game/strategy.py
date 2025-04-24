"""Implement various game strategies."""

from functools import reduce
from operator import and_

from quarto_game.board import Board
from quarto_game.piece import Piece


def is_winning_position(piece: Piece, board: Board, position) -> bool:
    """Check if putting the piece on the board at the given position would
    finish the game."""
    row, col = position
    # Verify that the position is empty
    assert board.grid[row][col] == -1
    alignments = []
    # Check current row
    alignments.append({(row, c) for c in range(4)})
    # Check current column
    alignments.append({(r, col) for r in range(4)})
    # Check diagonal (if position is in the diagonal)
    if row == col:
        alignments.append({(d, d) for d in range(4)})
    # Check antidiagonal (if position is in the antidiagonal)
    elif row == 3 - col:
        alignments.append({(d, 3 - d) for d in range(4)})

    # Check all alignments, pretending that the piece is at the given position
    for alignment in alignments:
        pieces = {
            board.grid[r][c] if (r, c) != (row, col) else piece for (r, c) in alignment
        }
        # Check there are 4 pieces in the alignment
        if sum(piece >= 0 for piece in pieces) < 4:
            continue
        # Check if this is a winning alignment
        if reduce(and_, pieces, 15) or reduce(lambda x, y: x & (15 - y), pieces, 15):
            return True

    return False


def is_winning_piece(piece: Piece, board: Board):
    """Check if a given piece would lead to a winning game."""
    return any(
        is_winning_position(piece, board, position)
        for position in board.empty_positions
    )
