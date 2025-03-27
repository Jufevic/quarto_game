"""Main game logic."""

from itertools import cycle, product
from random import choice, shuffle
from string import ascii_uppercase as alphabet

from board import Board
from piece import Piece
from player import HumanPlayer, Player, RandomRobotPlayer


def play_game(player1: Player, player2: Player):
    """Start a new game"""
    board = Board()
    finished = False
    winner = None
    # Randomly select the first player
    players = shuffle([player1, player2])
    for choosing_player, putting_player in cycle([players, reversed(players)]):
        if not board.available_pieces:
            finished = True
            break
        chosen_piece = choosing_player.choose_piece(board)
        chosen_position = putting_player.choose_position(chosen_piece, board)
        board.put_piece(chosen_piece, chosen_position)
        if board.is_game_finished():
            finished = True
            winner = putting_player
            break


def play_against_machine():
    """Start a new game with a human vs a machine."""
    player1 = HumanPlayer(name="player 1")
    player2 = RandomRobotPlayer(name="stupid robot")
    play_game(player1, player2)


if __name__ == "__main__":
    board = Board()
    finished = False
    winner = None
    your_turn = True
    while not finished:
        board.display()
        if your_turn:
            if not board.available_pieces:
                finished = True
                break
            print("\nYour turn")
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
                    print("Piece is already on the board.")
                    chosen = None
            print(f"Chosen piece: {chosen:04b}")

            # Put the piece to a random valid location on the grid
            empties = {
                (row, col)
                for row, col in product(range(4), repeat=2)
                if board.grid[row][col] < 0
            }
            row, col = choice(tuple(empties))
            print(f"Chosen position: {alphabet[row]}{col}")
            board.put_piece(chosen, (row, col))
            if board.is_game_finished():
                finished = True
                winner = "your opponent"
                break

        # Opponent's turn
        else:
            if not board.available_pieces:
                finished = True
                break
            print("\nOpponent's turn")
            chosen = choice(tuple(board.available_pieces))
            print(f"Chosen piece: {chosen:04b}")

            # Put the piece to a valid location on the grid
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
            board.put_piece(chosen, (row, col))
            if board.is_game_finished():
                finished = True
                winner = "you"
                break
        your_turn = not your_turn

    # Game is finished, declare who is the winner and why
    board.display()
    print("Game finished!")
    if winner == "you":
        print("Congratulations! You won! 😁")
    elif winner == "your opponent":
        print("You loose! Booh ☹️")
    elif winner is None:
        print("Tie!")
