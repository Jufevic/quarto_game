from game import play_game
from player import get_robot_player

if __name__ == "__main__":
    wins = 0
    losses = 0
    ties = 0
    games = 10000
    for game_number in range(games):
        player1 = get_robot_player(level=1)
        player1.name = "First robot"
        player2 = get_robot_player(level=0)
        player2.name = "Second robot"
        winner = play_game(player1, player2)
        if winner is None:
            ties += 1
        if winner == player1:
            wins += 1
        elif winner == player2:
            losses += 1
    print(
        f"{games} games played for level 1 player vs level 0 player, {wins} wins,"
        f" {losses} losses and {ties} ties."
    )
