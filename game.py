"""Main game logic."""

from itertools import product
from random import choice
from string import ascii_uppercase as alphabet

from board import Board
from piece import Piece

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
            board.available_pieces.remove(chosen)
            print(f"Chosen piece: {chosen:04b}")

            # Put the piece to a random valid location on the grid
            empties = {
                (row, col)
                for row, col in product(range(4), repeat=2)
                if board.grid[row][col] < 0
            }
            row, col = choice(tuple(empties))
            print(f"Chosen position: {alphabet[row]}{col}")
            board.grid[row][col] = chosen
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
            board.available_pieces.remove(chosen)
            print(f"Chosen piece: {chosen:04b}")

            # Put the piece to a valid location on the grid
            row, col = None, None
            while row is None or col is None:
                empties = [
                    f"{alphabet[r]}{c}"
                    for r, c in product(range(4), repeat=2)
                    if board.grid[r][c] < 0
                ]
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
            board.grid[row][col] = chosen
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
        print("You loose! Booh ☹")
    elif winner is None:
        print("Tie!")
