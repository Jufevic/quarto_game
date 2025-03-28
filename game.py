"""Main game logic."""

from random import shuffle

from board import Board
from player import HumanPlayer, Player, RandomRobotPlayer


class IllegalMoveError(Exception):
    pass


def play_game(player1: Player, player2: Player):
    """Start a new game"""
    board = Board()
    winner = None
    # Randomly select the first player
    players = [player1, player2]
    shuffle(players)
    piece_chooser, position_chooser = players

    # Every turn is divided in two steps: a player chooses a piece, and its
    # opponent chooses wher to put it
    while board.available_pieces:
        # Choose a piece
        chosen_piece = piece_chooser.choose_piece(board)
        # Verify the chosen piece validity
        if chosen_piece not in board.available_pieces:
            raise IllegalMoveError(
                f"The requested piece {chosen_piece} is already on the board."
            )

        # Choose where to put the piece
        chosen_position = position_chooser.choose_position(chosen_piece, board)
        # Verify the chosen position validity
        if chosen_position not in board.empty_positions:
            raise IllegalMoveError(
                f"The requested position {chosen_position} is not empty."
            )

        # Put the piece and verify if the game is finished
        board.put_piece(chosen_piece, chosen_position)
        if board.is_game_finished():
            winner = position_chooser
            break

        # Swap piece choosing player and position choosing player
        piece_chooser, position_chooser = position_chooser, piece_chooser

    # Game is finished, declare who won
    alignment = board.find_alignment()
    board.display(alignment)
    print("Game finished")
    if winner is not None:
        print(f"The winner is {winner.name}!")
    else:
        print("Tie! No one wins this time...")


def play_against_machine():
    """Start a new game with a human vs a machine."""
    player1 = HumanPlayer(name="player 1")
    player2 = RandomRobotPlayer(name="stupid robot")
    play_game(player1, player2)


def play_machine_vs_machine():
    """Start a new game with a machine vs another machine."""
    player1 = RandomRobotPlayer(name="first robot")
    player2 = RandomRobotPlayer(name="second robot")
    play_game(player1, player2)


if __name__ == "__main__":
    # play_against_machine()
    play_machine_vs_machine()
