"""Implement board logic."""

from functools import reduce
from itertools import chain
from operator import and_
from string import ascii_uppercase as alphabet


class Board:
    """Quarto board class."""

    def __init__(self, grid=None):
        if grid is None:
            grid = [[-1] * 4 for _ in range(4)]
        self.grid = grid

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
        diagonal = [self.grid[x][x] for x in range(4)]
        antidiagonal = [self.grid[x][3 - x] for x in range(4)]
        for row in chain(self.grid, zip(*self.grid), [diagonal], [antidiagonal]):
            if all(item >= 0 for item in row) and (
                reduce(and_, row, 15) or reduce(lambda x, y: x & (15 - y), row, 15)
            ):
                return True
        return False
