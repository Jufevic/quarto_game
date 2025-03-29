from game import play_game
from player import get_robot_player
from tqdm import tqdm


def benchmark_robot(first_level=1, second_level=0, games=1000):
    """Benchmark to know on average how many games are won by a robot of
    the first level vs a robot of the second level."""
    wins = 0
    losses = 0
    ties = 0
    for game_number in tqdm(range(games)):
        player1 = get_robot_player(level=first_level)
        player1.name = "First robot"
        player2 = get_robot_player(level=second_level)
        player2.name = "Second robot"
        winner = play_game(player1, player2, quiet=True)
        if winner is None:
            ties += 1
        if winner == player1:
            wins += 1
        elif winner == player2:
            losses += 1
    print(
        f"Out of {games} games played for level {first_level} player vs level "
        f"{second_level} player, {wins / games:.0%} win rate, "
        f"{losses / games:.0%} loss rate and {ties / games:.0%} tie rate."
    )


if __name__ == "__main__":
    for first_level, second_level in ((0, 0), (1, 0), (1, 1), (2, 0), (2, 1), (2, 2)):
        benchmark_robot(first_level=first_level, second_level=second_level, games=10000)
