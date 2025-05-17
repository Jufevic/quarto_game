"""Implement board logic."""

from collections import defaultdict
from functools import reduce
from itertools import product
from operator import and_
from string import ascii_uppercase as alphabet

from quarto_game.piece import Piece


class Board:
    """Quarto board class."""

    def __init__(self):
        self.grid = [[-1] * 4 for _ in range(4)]
        self.empty_positions = {(r, c) for r, c in product(range(4), repeat=2)}
        self.available_pieces = {Piece(i) for i in range(16)}
        self.game_finished = False
        self.critical_positions = defaultdict(list)
        self.winning_alignment = None

    def _update_critical_positions(self, position: tuple[int, int]):
        """Update critical positions (those which complete an alignment of 4)."""
        self.critical_positions.pop(position, None)
        row, col = position
        # Only update relevant alignments: current row, current column, diagonal
        # and antidiagonal
        alignments = [
            {(row, col) for col in range(4)},
            {(row, col) for row in range(4)},
        ]
        if row == col:
            alignments.append({(i, i) for i in range(4)})
        elif row == 3 - col:
            alignments.append({(i, 3 - i) for i in range(4)})
        for align in alignments:
            empties = align & self.empty_positions
            if len(empties) == 1:
                (element,) = empties
                self.critical_positions[element].append(align)

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
        self.grid[row][col] = piece
        # Check if this move finishes the game
        self._check_if_game_finished(position)
        self.available_pieces.remove(piece)
        # Update caches to improve performance
        self.empty_positions.remove((row, col))
        self._update_critical_positions(position)

    def _check_if_game_finished(self, position):
        """Check if the game just finished by putting the piece at the given position

        :param position: Position to check
        """
        for alignment in self.critical_positions[position]:
            if self.is_winning_alignment(alignment):
                self.game_finished = True
                self.winning_alignment = alignment
                break
        else:
            self.game_finished = False

    def is_winning_alignment(self, alignment):
        """Check if the given alignment is winning

        :param alignment: a set of 4 pieces positions
        """
        items = {self.grid[row][col] for row, col in alignment}
        return all(item >= 0 for item in items) and (
            reduce(and_, items, 15) or reduce(lambda x, y: x & (15 - y), items, 15)
        )
