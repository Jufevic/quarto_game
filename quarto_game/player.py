"""Possible game-player interactions."""

from abc import ABC, abstractmethod
from random import choice
from string import ascii_uppercase as alphabet

from quarto_game.board import Board
from quarto_game.piece import Piece
from quarto_game.strategy import is_winning_piece, is_winning_position


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


class Level0RobotPlayer(RobotPlayer):
    def choose_piece(self, board):
        return choice(tuple(board.available_pieces))

    def choose_position(self, piece, board):
        return choice(tuple(board.empty_positions))


class Level1RobotPlayer(Level0RobotPlayer):
    """A robot player that won't miss an opportunity to win if given a winning
    piece. But still give its opponent random pieces."""

    def choose_piece(self, board):
        """Give a randomly chosen piece."""
        return super().choose_piece(board)

    def choose_position(self, piece, board):
        """Put a given piece at a winning position if possible, else at a
        random position."""
        # Try to put the piece here and check if it's a winning position.
        for position in board.empty_positions:
            if is_winning_position(piece, board, position):
                return position

        # As a fallback, return a random position.
        return super().choose_position(piece, board)


class Level2RobotPlayer(Level1RobotPlayer):
    """A robot player that won't miss an opportunity to win if given a winning
    piece and will avoid giving its opponent winning pieces."""

    def choose_piece(self, board: Board):
        """Give a non winning piece."""
        possible_choices = board.available_pieces.copy()
        for piece in board.available_pieces:
            if is_winning_piece(piece, board):
                possible_choices.remove(piece)
        if possible_choices:
            return choice(tuple(possible_choices))

        # If the game is lost anyway, give a random piece
        return super().choose_piece(board)

    def choose_position(self, piece: Piece, board: Board):
        """Put a given piece at a winning position if possible, else at a
        random position."""
        return super().choose_position(piece, board)


class Level3RobotPlayer(Level2RobotPlayer):
    """A robot player that won't miss an opportunity to win if given a winning
    piece, will avoid giving its opponent winning pieces, and will try to force
    the opponent to give you a winning piece."""

    def choose_piece(self, board: Board):
        """Give a non winning piece."""
        return super().choose_piece(board)

    def choose_position(self, piece: Piece, board: Board):
        """Put a given piece at a winning position if possible, else at a
        random position."""
        for position in board.empty_positions:
            if is_winning_position(piece, board, position):
                return position

        return super().choose_position(piece, board)


def get_robot_player(level=0):
    """Get a robot player with the given level."""
    match level:
        case 0:
            return Level0RobotPlayer(name="stupid robot")
        case 1:
            return Level1RobotPlayer(name="simple robot")
        case 2:
            return Level2RobotPlayer(name="simple robot")
