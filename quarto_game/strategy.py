"""Implement various game strategies."""

from functools import reduce
from operator import and_

from quarto_game.board import Board
from quarto_game.piece import Piece


def is_winning_position(piece: Piece, board: Board, position) -> bool:
    """Check if putting the piece on the board at the given position would
    finish the game."""
    alignments = board.critical_positions[position]

    # Check all alignments, pretending that the piece is at the given position
    for alignment in alignments:
        pieces = {board.grid[r][c] for (r, c) in alignment}
        pieces.remove(-1)
        pieces.add(piece)
        # Check if this is a winning alignment
        if reduce(and_, pieces, 15) or reduce(lambda x, y: x & (15 - y), pieces, 15):
            return True

    return False


def is_winning_piece(piece: Piece, board: Board):
    """Check if a given piece would lead to a winning game

    Optimised with the set of critical_positions.
    """
    return any(
        is_winning_position(piece, board, position)
        for position in board.critical_positions
    )
