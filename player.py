"""Possible game-player interactions."""

from abc import ABC, abstractmethod

from board import Board
from piece import Piece


class Player(ABC):
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
        pass

    def choose_position(board):
        pass


class RobotPlayer(Player):
    def choose_piece(board):
        pass

    def choose_position(board):
        pass
