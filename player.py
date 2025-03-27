"""Possible game-player interactions."""

from abc import ABC, abstractmethod
from random import choice

from board import Board
from piece import Piece


class Player(ABC):
    def __init__(self, name="default name"):
        super().__init__(name=name)

    @abstractmethod
    def choose_piece(board: Board) -> Piece:
        """Choose a piece from the set of available pieces to give to the opponent."""
        pass

    @abstractmethod
    def choose_position(piece: Piece, board: Board) -> tuple[int, int]:
        """Choose where to put a given piece on the board."""
        pass


class HumanPlayer(Player):
    def choose_piece(board):
        board.display()

    def choose_position(board):
        board.display()


class RobotPlayer(Player):
    pass


class RandomRobotPlayer(RobotPlayer):
    def choose_piece(board):
        return choice(tuple(board.available_pieces))

    def choose_position(board):
        return choice(tuple(board.empty_positions))
