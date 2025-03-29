from game import play_game
from player import get_robot_player


def benchmark_robot(first_level=1, second_level=0, games=1000):
    """Benchmark to know on average how many games are won by a robot of
    the first level vs a robot of the second level."""
    wins = 0
    losses = 0
    ties = 0
    for game_number in range(games):
        player1 = get_robot_player(level=first_level)
        player1.name = "First robot"
        player2 = get_robot_player(level=second_level)
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


if __name__ == "__main__":
    benchmark_robot(first_level=2, second_level=0)
