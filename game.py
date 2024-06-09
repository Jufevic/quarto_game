"""Main game logic."""

from itertools import product, chain
from functools import reduce
from operator import and_
from random import choice
from string import ascii_uppercase as alphabet

from piece import Piece


def display():
    print("    0    1    2    3  \n  +----+----+----+----+")
    for row in range(4):
        print(f"{alphabet[row]} |", end="")
        elements = [f"{item:04b}" if item >= 0 else "    " for item in grid[row]]
        print("|".join(elements) + "|")
        print("  +----+----+----+----+")

def game_finished():
    diagonal = [grid[x][x] for x in range(4)]
    antidiagonal = [grid[x][3 - x] for x in range(4)]
    for row in chain(grid, zip(*grid), [diagonal], [antidiagonal]):
        if (all(item >= 0 for item in row)
                and (reduce(and_, row, 15)
                or reduce(lambda x, y: x & (15 - y), row, 15))):
            return True
    return False


if __name__ == "__main__":
    finished = False
    winner = None
    available = {Piece(i) for i in range(16)}
    grid = [[-1] * 4 for _ in range(4)]
    your_turn = True
    while not finished:
        display()
        if your_turn:
            if not available:
                finished = True
                break
            print("\nYour turn")
            # Choose a piece to give to the opponent
            chosen = None
            while chosen is None:
                pieces = ", ".join(f"{piece:04b}" for piece in available)
                print(f"Available pieces: {pieces}")
                user_input = input("Choose a number from the available numbers: ")
                try:
                    chosen = Piece(int(user_input, 2))
                except ValueError:
                    chosen = None
                    print("Invalid choice.")
                if isinstance(chosen, Piece) and chosen not in available:
                    print("Piece is already on the board.")
                    chosen = None
            available.remove(chosen)
            print(f"Chosen piece: {chosen:04b}")

            # Put the piece to a random valid location on the grid
            empties = {(row, col) for row, col in product(range(4), repeat=2)
                if grid[row][col] < 0}
            row, col = choice(tuple(empties))
            print(f"Chosen position: {alphabet[row]}{col}")
            grid[row][col] = chosen
            if game_finished():
                finished = True
                winner = "your opponent"
                break
        
        # Opponent's turn
        else:
            if not available:
                finished = True
                break
            print("\nOpponent's turn")
            chosen = choice(tuple(available))
            available.remove(chosen)
            print(f"Chosen piece: {chosen:04b}")
            
            # Put the piece to a valid location on the grid
            row, col = None, None
            while row is None or col is None:
                empties = [f"{alphabet[r]}{c}" 
                    for r, c in product(range(4), repeat=2) if grid[r][c] < 0]
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
            grid[row][col] = chosen
            if game_finished():
                finished = True
                winner = "you"
                break
        your_turn = not your_turn
    
    # Game is finished, declare who is the winner and why
    display()
    print("Game finished!")
    if winner == "you":
        print("Congratulations! You won! 😁")
    elif winner == "your opponent":
        print("You loose! Booh ☹")
    elif winner is None:
        print("Tie!")