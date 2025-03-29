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

    def display(self, highlighted_positions=[]):
        """Print the board state."""
        print("    0    1    2    3  \n  +----+----+----+----+")
        for row in range(4):
            print(f"{alphabet[row]} |", end="")
            elements = []
            for col, item in enumerate(self.grid[row]):
                if item >= 0:
                    if (row, col) in highlighted_positions:
                        elements.append(f"\033[93m{item:04b}\033[0m")
                    else:
                        elements.append(f"{item:04b}")
                else:
                    elements.append("    ")
            print("|".join(elements) + "|")
            print("  +----+----+----+----+")

    def put_piece(self, piece: Piece, position: tuple[int, int]):
        """Put the given piece at the given position on the board."""
        row, col = position
        self.available_pieces.remove(piece)
        self.empty_positions.remove((row, col))
        self.grid[row][col] = piece

    def find_alignment(self):
        """Try to find a winning alignment in the board.
        If found, return a set of positions."""
        diagonal = {(x, x) for x in range(4)}
        antidiagonal = {(x, 3 - x) for x in range(4)}
        rows = [{(row, col) for col in range(4)} for row in range(4)]
        cols = [{(row, col) for row in range(4)} for col in range(4)]
        for line in chain(rows, cols, [diagonal], [antidiagonal]):
            items = {self.grid[row][col] for row, col in line}
            if all(item >= 0 for item in items) and (
                reduce(and_, items, 15) or reduce(lambda x, y: x & (15 - y), items, 15)
            ):
                return line

    def is_game_finished(self):
        """Check if the game is finished."""
        alignment = self.find_alignment()
        return alignment is not None
