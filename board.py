"""Implement board logic."""

from functools import reduce
from itertools import chain, product
from operator import and_
from string import ascii_uppercase as alphabet

from piece import Piece


class Board:
    """Quarto board class."""

    def __init__(self):
        self.grid = [[-1] * 4 for _ in range(4)]
        self.empty_positions = {(r, c) for r, c in product(range(4), repeat=2)}
        self.available_pieces = {Piece(i) for i in range(16)}

    def display(self):
        """Print the board state."""
        print("    0    1    2    3  \n  +----+----+----+----+")
        for row in range(4):
            print(f"{alphabet[row]} |", end="")
            elements = [
                f"{item:04b}" if item >= 0 else "    " for item in self.grid[row]
            ]
            print("|".join(elements) + "|")
            print("  +----+----+----+----+")

    def is_game_finished(self):
        """Check if the game is finished."""
        diagonal = [self.grid[x][x] for x in range(4)]
        antidiagonal = [self.grid[x][3 - x] for x in range(4)]
        for row in chain(self.grid, zip(*self.grid), [diagonal], [antidiagonal]):
            if all(item >= 0 for item in row) and (
                reduce(and_, row, 15) or reduce(lambda x, y: x & (15 - y), row, 15)
            ):
                return True
        return False

    def put_piece(self, piece: Piece, position: tuple[int, int]):
        """Put the given piece at the given position on the board."""
        row, col = position
        self.available_pieces.remove(piece)
        self.empty_positions.remove((row, col))
        self.grid[row][col] = piece
