"""Possible game-player interactions."""

from abc import ABC, abstractmethod
from random import choice
from string import ascii_uppercase as alphabet

from board import Board
from piece import Piece


class Player(ABC):
    def __init__(self, name="default name"):
        self.name = name

    @abstractmethod
    def choose_piece(self, board: Board) -> Piece:
        """Choose a piece from the set of available pieces to give to the opponent."""
        pass

    @abstractmethod
    def choose_position(self, piece: Piece, board: Board) -> tuple[int, int]:
        """Choose where to put a given piece on the board."""
        pass


class HumanPlayer(Player):
    def choose_piece(self, board):
        board.display()
        print(f"\n{self.name}'s turn")
        # Choose a piece to give to the opponent
        chosen = None
        while chosen is None:
            pieces = ", ".join(f"{piece:04b}" for piece in board.available_pieces)
            print(f"Available pieces: {pieces}")
            user_input = input("Choose a number from the available numbers: ")
            try:
                chosen = Piece(int(user_input, 2))
            except ValueError:
                chosen = None
                print("Invalid choice.")
            if isinstance(chosen, Piece) and chosen not in board.available_pieces:
                print(f"Piece {chosen:04b} is already on the board.")
                chosen = None
        print(f"Chosen piece: {chosen:04b}")
        return chosen

    def choose_position(self, piece, board):
        board.display()
        print(f"Piece chosen by your opponent: {piece:04b}")
        row, col = None, None
        while row is None or col is None:
            empties = [f"{alphabet[r]}{c}" for r, c in board.empty_positions]
            print(f"Available empty positions: {', '.join(empties)}")
            user_input = input("Choose a position from the available positions: ")
            try:
                row, col = alphabet.index(user_input[0]), int(user_input[1])
            except (ValueError, KeyError):
                row, col = None, None
                print("Invalid choice.")
            if user_input not in empties:
                row, col = None, None
        print(f"Chosen position: {alphabet[row]}{col}")
        return row, col


class RobotPlayer(Player):
    pass


class RandomRobotPlayer(RobotPlayer):
    def choose_piece(self, board):
        return choice(tuple(board.available_pieces))

    def choose_position(self, piece, board):
        return choice(tuple(board.empty_positions))
